import useSWR from "swr";
import { fetcher } from "@/lib/api";

export function useStats() {
  return useSWR("/api/stats", fetcher, { refreshInterval: 30_000 });
}
