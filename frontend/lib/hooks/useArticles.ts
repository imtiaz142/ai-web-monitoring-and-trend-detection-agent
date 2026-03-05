import useSWR from "swr";
import { fetcher } from "@/lib/api";

export function useArticles() {
  return useSWR("/api/articles/latest", fetcher, { refreshInterval: 120_000 });
}
