import type { Layout } from "$lib/types";
import { VERSION } from "$lib/version";
import { decodeLayout, encodeLayout } from "./share";

const BRIDGE_PROTOCOL = "rackula-bridge/v1";

type HostMessageType =
  | "rackula:hello"
  | "rackula:set-layout"
  | "rackula:get-layout";

type RackulaMessageType =
  | "rackula:ready"
  | "rackula:layout-changed"
  | "rackula:layout-response"
  | "rackula:layout-applied"
  | "rackula:error";

interface BridgeMessage<TPayload = unknown> {
  protocol: typeof BRIDGE_PROTOCOL;
  type: HostMessageType | RackulaMessageType;
  source: "host" | "rackula";
  requestId?: string;
  timestamp: string;
  payload?: TPayload;
}

interface SetLayoutPayload {
  encodedLayout?: string;
  siteId?: string;
  siteName?: string;
}

interface BridgeErrorPayload {
  code: string;
  message: string;
  details?: unknown;
}

interface BridgeConfig {
  getLayout: () => Layout;
  applyLayout: (layout: Layout) => void;
  onError?: (error: BridgeErrorPayload) => void;
}

export interface RackulaEmbedBridgeController {
  dispose: () => void;
  notifyLayoutChanged: (layout: Layout) => void;
}

const NOOP_CONTROLLER: RackulaEmbedBridgeController = {
  dispose: () => undefined,
  notifyLayoutChanged: () => undefined,
};

function isBridgeMessage(value: unknown): value is BridgeMessage<unknown> {
  if (!value || typeof value !== "object") {
    return false;
  }

  const candidate = value as Partial<BridgeMessage<unknown>>;
  return (
    candidate.protocol === BRIDGE_PROTOCOL &&
    typeof candidate.type === "string" &&
    typeof candidate.source === "string"
  );
}

function createMessage<TPayload>(
  type: HostMessageType | RackulaMessageType,
  payload?: TPayload,
  requestId?: string,
): BridgeMessage<TPayload> {
  return {
    protocol: BRIDGE_PROTOCOL,
    type,
    source: "rackula",
    timestamp: new Date().toISOString(),
    ...(requestId ? { requestId } : {}),
    ...(payload !== undefined ? { payload } : {}),
  };
}

function parseOrigin(value: string): string | null {
  if (!value) {
    return null;
  }

  try {
    return new URL(value).origin;
  } catch {
    return null;
  }
}

function getConfiguredOrigins(): Set<string> {
  const allowed = new Set<string>();
  const params = new URLSearchParams(window.location.search);
  const configured = params.get("bridgeParentOrigin");

  if (configured) {
    for (const segment of configured.split(",")) {
      const origin = parseOrigin(segment.trim());
      if (origin) {
        allowed.add(origin);
      }
    }
  }

  const referrerOrigin = parseOrigin(document.referrer);
  if (referrerOrigin) {
    allowed.add(referrerOrigin);
  }

  return allowed;
}

export function createEmbedBridge(
  config: BridgeConfig,
): RackulaEmbedBridgeController {
  if (typeof window === "undefined" || window.parent === window) {
    return NOOP_CONTROLLER;
  }

  const allowedOrigins = getConfiguredOrigins();
  let activeHostOrigin: string | null = [...allowedOrigins][0] ?? null;
  let disposed = false;
  let pendingHostDrivenChange = false;
  let lastBroadcast: string | null = null;
  let broadcastTimer: ReturnType<typeof setTimeout> | null = null;

  const post = (
    type: RackulaMessageType,
    payload?: unknown,
    requestId?: string,
  ): void => {
    const targetOrigin = activeHostOrigin;
    if (!targetOrigin || disposed) {
      return;
    }

    window.parent.postMessage(
      createMessage(type, payload, requestId),
      targetOrigin,
    );
  };

  const emitError = (
    code: string,
    message: string,
    details?: unknown,
    requestId?: string,
  ): void => {
    const payload: BridgeErrorPayload = {
      code,
      message,
      ...(details ? { details } : {}),
    };
    post("rackula:error", payload, requestId);
    config.onError?.(payload);
  };

  const emitReady = (): void => {
    post("rackula:ready", {
      app: "rackula",
      version: VERSION,
      capabilities: {
        setLayout: true,
        getLayout: true,
        emitLayoutChanged: true,
      },
    });
  };

  const emitLayoutChanged = (layout: Layout): void => {
    const encodedLayout = encodeLayout(layout);
    if (encodedLayout === lastBroadcast && !pendingHostDrivenChange) {
      return;
    }

    lastBroadcast = encodedLayout;

    post("rackula:layout-changed", {
      encodedLayout,
      layoutName: layout.name,
      rackCount: layout.racks.length,
      deviceCount: layout.racks.reduce(
        (count, rack) => count + rack.devices.length,
        0,
      ),
      source: pendingHostDrivenChange ? "host" : "user",
    });

    pendingHostDrivenChange = false;
  };

  const handleSetLayout = (
    payload: SetLayoutPayload | undefined,
    requestId?: string,
  ): void => {
    const encodedLayout = payload?.encodedLayout;
    if (!encodedLayout || typeof encodedLayout !== "string") {
      emitError(
        "INVALID_PAYLOAD",
        "set-layout requires encodedLayout",
        payload,
        requestId,
      );
      return;
    }

    const nextLayout = decodeLayout(encodedLayout);
    if (!nextLayout) {
      emitError(
        "DECODE_FAILED",
        "Could not decode Rackula layout payload",
        undefined,
        requestId,
      );
      return;
    }

    pendingHostDrivenChange = true;
    config.applyLayout(nextLayout);

    post(
      "rackula:layout-applied",
      {
        encodedLayout,
        layoutName: nextLayout.name,
        rackCount: nextLayout.racks.length,
        deviceCount: nextLayout.racks.reduce(
          (count, rack) => count + rack.devices.length,
          0,
        ),
        siteId: payload?.siteId,
        siteName: payload?.siteName,
      },
      requestId,
    );
  };

  const handleGetLayout = (requestId?: string): void => {
    const layout = config.getLayout();
    post(
      "rackula:layout-response",
      {
        encodedLayout: encodeLayout(layout),
        layoutName: layout.name,
        rackCount: layout.racks.length,
        deviceCount: layout.racks.reduce(
          (count, rack) => count + rack.devices.length,
          0,
        ),
      },
      requestId,
    );
  };

  const handleHostMessage = (event: MessageEvent): void => {
    if (disposed || event.source !== window.parent) {
      return;
    }

    if (!isBridgeMessage(event.data) || event.data.source !== "host") {
      return;
    }

    // If no origin was preconfigured, lock to the first sender and reject others.
    if (!activeHostOrigin) {
      activeHostOrigin = event.origin;
      allowedOrigins.add(event.origin);
    }

    if (!allowedOrigins.has(event.origin)) {
      return;
    }

    switch (event.data.type) {
      case "rackula:hello": {
        emitReady();
        handleGetLayout(event.data.requestId);
        break;
      }
      case "rackula:set-layout": {
        handleSetLayout(
          event.data.payload as SetLayoutPayload | undefined,
          event.data.requestId,
        );
        break;
      }
      case "rackula:get-layout": {
        handleGetLayout(event.data.requestId);
        break;
      }
      default:
        break;
    }
  };

  window.addEventListener("message", handleHostMessage);

  // If we already know a trusted parent origin, send readiness immediately.
  if (activeHostOrigin) {
    emitReady();
  }

  return {
    dispose: () => {
      if (disposed) {
        return;
      }
      disposed = true;
      window.removeEventListener("message", handleHostMessage);
      if (broadcastTimer) {
        clearTimeout(broadcastTimer);
        broadcastTimer = null;
      }
    },
    notifyLayoutChanged: (layout: Layout) => {
      if (disposed) {
        return;
      }

      if (broadcastTimer) {
        clearTimeout(broadcastTimer);
      }

      broadcastTimer = setTimeout(() => {
        emitLayoutChanged(layout);
        broadcastTimer = null;
      }, 250);
    },
  };
}
