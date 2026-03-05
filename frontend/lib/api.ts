const API_BASE = "/api";

export const fetcher = (url: string) =>
  fetch(`${API_BASE}${url.startsWith("/api") ? url.slice(4) : url}`).then(
    (res) => {
      if (!res.ok) throw new Error("API request failed");
      return res.json();
    }
  );

export async function triggerScrape() {
  const res = await fetch(`${API_BASE}/scrape/trigger`, { method: "POST" });
  return res.json();
}

export async function generateInsight() {
  const res = await fetch(`${API_BASE}/insights/generate`, { method: "POST" });
  return res.json();
}
