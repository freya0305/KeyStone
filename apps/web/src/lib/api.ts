export const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface RequestOptions {
  method?: string;
  body?: unknown;
  headers?: Record<string, string>;
}

// Clerk getToken - works in both client component and API route contexts
async function getClerkToken(): Promise<string | null> {
  try {
    const { getToken } = await import('@clerk/nextjs');
    return await getToken();
  } catch {
    return null;
  }
}

export async function apiRequest<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
  const { method = 'GET', body, headers = {} } = options;

  // Get Clerk session token client-side
  let authHeaders: Record<string, string> = {};
  const token = await getClerkToken();
  if (token) {
    authHeaders = { Authorization: `Bearer ${token}` };
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...authHeaders,
      ...headers,
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

export async function apiDownload(endpoint: string, options: RequestOptions = {}): Promise<Blob> {
  const { method = 'POST', body, headers = {} } = options;

  // Get Clerk session token client-side
  const token = await getClerkToken();
  const authHeaders: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {};

  const response = await fetch(`${API_BASE}${endpoint}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...authHeaders,
      ...headers,
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.blob();
}
