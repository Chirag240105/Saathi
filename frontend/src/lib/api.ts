import { API_BASE_URL } from "./constants";

export class ApiError extends Error {
  constructor(
    public code: string,
    message: string,
    public status: number,
  ) {
    super(message);
  }
}

type Options = { method?: string; body?: unknown; write?: boolean; signal?: AbortSignal };

/** Single entry point for REST calls. Write routes send the demo shared secret. */
export async function api<T>(path: string, opts: Options = {}): Promise<T> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  const secret = import.meta.env.VITE_SHARED_SECRET;
  if (opts.write && secret) headers["X-Saathi-Key"] = secret;

  let res: Response;
  try {
    res = await fetch(`${API_BASE_URL}${path}`, {
      method: opts.method ?? "GET",
      headers,
      body: opts.body === undefined ? undefined : JSON.stringify(opts.body),
      signal: opts.signal,
    });
  } catch {
    throw new ApiError("network", "Cannot reach the Saathi server. Is it running?", 0);
  }
  if (!res.ok) {
    const data = await res.json().catch(() => null);
    throw new ApiError(
      data?.error?.code ?? "http_error",
      data?.error?.message ?? `Request failed (${res.status})`,
      res.status,
    );
  }
  return res.status === 204 ? (undefined as T) : ((await res.json()) as T);
}
