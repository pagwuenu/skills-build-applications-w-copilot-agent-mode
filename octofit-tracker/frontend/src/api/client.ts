const codespaceName = import.meta.env.REACT_APP_CODESPACE_NAME;

// Relative /api paths use the Vite proxy locally; Codespaces exposes port 8000 over HTTPS.
export const apiBaseUrl = import.meta.env.VITE_API_BASE_URL
  || (codespaceName ? `https://${codespaceName}-8000.app.github.dev` : '');

export type ApiRecord = Record<string, unknown>;

export function collectionFromResponse(payload: unknown, collectionName: string): ApiRecord[] {
  let value = payload;
  if (value !== null && typeof value === 'object' && !Array.isArray(value)) {
    const response = value as Record<string, unknown>;
    value = Array.isArray(response.results) ? response.results : response[collectionName];
  }
  return Array.isArray(value)
    ? value.filter((item): item is ApiRecord => item !== null && typeof item === 'object' && !Array.isArray(item))
    : [];
}

export async function getCollection(path: string, collectionName: string): Promise<ApiRecord[]> {
  const endpoint = `${apiBaseUrl}${path}`;
  console.log('Fetching REST API endpoint:', endpoint);
  const response = await fetch(endpoint);
  if (!response.ok) throw new Error(`Request failed with ${response.status}`);
  const payload: unknown = await response.json();
  console.log('Fetched REST API data:', payload);
  return collectionFromResponse(payload, collectionName);
}
