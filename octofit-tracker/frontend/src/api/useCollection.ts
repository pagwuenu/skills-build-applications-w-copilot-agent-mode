import { createElement, useEffect, useState } from 'react';
import { getCollection, type ApiRecord } from './client.js';

export function useCollection(path: string, collectionName: string, label: string) {
  const [records, setRecords] = useState<ApiRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError(null);
    getCollection(path, collectionName)
      .then((data) => {
        if (active) setRecords(data);
      })
      .catch((cause: unknown) => {
        if (active) setError(`Unable to load ${label.toLowerCase()}: ${cause instanceof Error ? cause.message : 'Unexpected error'}`);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [path, collectionName, label]);

  return { records, loading, error };
}

export function displayValue(record: ApiRecord, ...keys: string[]): string | null {
  for (const key of keys) {
    const value = record[key];
    if (typeof value === 'string' || typeof value === 'number') return String(value);
  }
  return null;
}

export function CollectionState({
  loading,
  error,
  empty,
  count,
}: {
  loading: boolean;
  error: string | null;
  empty: string;
  count: number;
}) {
  if (loading) return createElement('div', { className: 'alert alert-info status-message', role: 'status' }, 'Loading...');
  if (error) return createElement('div', { className: 'alert alert-danger status-message', role: 'alert' }, error);
  if (count === 0) return createElement('div', { className: 'alert alert-light border status-message', role: 'status' }, empty);
  return null;
}
