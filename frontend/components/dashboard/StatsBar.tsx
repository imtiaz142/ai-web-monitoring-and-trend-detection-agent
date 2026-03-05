"use client";

import { useStats } from "@/lib/hooks/useStats";
import { Newspaper, TrendingUp, Flame, Clock } from "lucide-react";
import { formatDistanceToNow } from "date-fns";
import clsx from "clsx";

export default function StatsBar() {
  const { data, isLoading } = useStats();
  const stats = data?.data;

  const cards = [
    {
      label: "Articles Scanned",
      value: stats?.total_articles ?? "-",
      icon: Newspaper,
      color: "text-accent-cyan",
    },
    {
      label: "Active Trends",
      value: stats?.total_trends ?? "-",
      icon: TrendingUp,
      color: "text-accent-amber",
    },
    {
      label: "Emerging Trends",
      value: stats?.emerging_count ?? "-",
      icon: Flame,
      color: "text-accent-red",
      pulse: (stats?.emerging_count ?? 0) > 0,
    },
    {
      label: "Last Scrape",
      value: stats?.last_scrape_at
        ? formatDistanceToNow(new Date(stats.last_scrape_at), {
            addSuffix: true,
          })
        : "Never",
      icon: Clock,
      color: "text-accent-green",
    },
  ];

  if (isLoading) {
    return (
      <div className="grid grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => (
          <div
            key={i}
            className="bg-bg-card border border-border rounded-lg p-4 h-20 animate-pulse"
          />
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-4 gap-4">
      {cards.map((card) => {
        const Icon = card.icon;
        return (
          <div
            key={card.label}
            className="bg-bg-card border border-border rounded-lg p-4"
          >
            <div className="flex items-center justify-between">
              <span className="text-text-muted text-xs uppercase tracking-wider">
                {card.label}
              </span>
              <Icon className={clsx("w-4 h-4", card.color)} />
            </div>
            <p
              className={clsx(
                "text-2xl font-bold mt-2 font-mono",
                card.color,
                card.pulse && "animate-pulse-dot"
              )}
            >
              {card.value}
            </p>
          </div>
        );
      })}
    </div>
  );
}
