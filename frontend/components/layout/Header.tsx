"use client";

import { useStats } from "@/lib/hooks/useStats";
import LiveIndicator from "@/components/ui/LiveIndicator";
import { RefreshCw } from "lucide-react";
import { triggerScrape } from "@/lib/api";
import { useState } from "react";
import clsx from "clsx";

export default function Header() {
  const { data, mutate } = useStats();
  const [scraping, setScraping] = useState(false);
  const stats = data?.data;

  const handleScrape = async () => {
    setScraping(true);
    try {
      await triggerScrape();
      await mutate();
    } finally {
      setScraping(false);
    }
  };

  return (
    <header className="h-14 bg-bg-secondary border-b border-border flex items-center justify-between px-6">
      <div className="flex items-center gap-4">
        <h2 className="font-heading text-sm font-semibold uppercase tracking-wider text-text-muted">
          Intelligence Dashboard
        </h2>
        <LiveIndicator lastScrape={stats?.last_scrape_at} />
      </div>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <span
            className={clsx(
              "w-2 h-2 rounded-full",
              stats?.ai_status?.status === "online" || stats?.ai_status?.status === "configured"
                ? "bg-accent-green"
                : "bg-accent-red"
            )}
          />
          <span className="text-xs text-text-muted">
            {stats?.ai_status?.provider
              ? `${stats.ai_status.provider} ${stats.ai_status.status}`
              : "AI ..."}
          </span>
        </div>
        <button
          onClick={handleScrape}
          disabled={scraping}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-accent-cyan/10 text-accent-cyan text-xs hover:bg-accent-cyan/20 transition-colors disabled:opacity-50"
        >
          <RefreshCw className={clsx("w-3 h-3", scraping && "animate-spin")} />
          {scraping ? "Scraping..." : "Scrape Now"}
        </button>
      </div>
    </header>
  );
}
