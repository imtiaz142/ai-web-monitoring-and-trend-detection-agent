import useSWR from "swr";
import { fetcher } from "@/lib/api";

export function useTrends() {
  return useSWR("/api/trends", fetcher, { refreshInterval: 60_000 });
}

export function useEmergingTrends() {
  return useSWR("/api/trends/emerging", fetcher, { refreshInterval: 60_000 });
}

export function useTrend(id: string) {
  return useSWR(id ? `/api/trends/${id}` : null, fetcher);
}

export function useTrendHistory(id: string) {
  return useSWR(id ? `/api/trends/${id}/history` : null, fetcher);
}
