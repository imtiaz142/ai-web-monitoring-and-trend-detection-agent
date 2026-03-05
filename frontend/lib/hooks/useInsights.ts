import useSWR from "swr";
import { fetcher } from "@/lib/api";

export function useInsights() {
  return useSWR("/api/insights/latest", fetcher, { refreshInterval: 300_000 });
}

export function useAllInsights() {
  return useSWR("/api/insights", fetcher, { refreshInterval: 300_000 });
}
