"use client";

import { useTrends } from "@/lib/hooks/useTrends";
import Link from "next/link";
import clsx from "clsx";

const statusColors: Record<string, string> = {
  emerging: "bg-accent-red/15 text-accent-red border-accent-red/30 hover:bg-accent-red/25",
  rising: "bg-accent-amber/15 text-accent-amber border-accent-amber/30 hover:bg-accent-amber/25",
  stable: "bg-accent-cyan/15 text-accent-cyan border-accent-cyan/30 hover:bg-accent-cyan/25",
  declining: "bg-white/5 text-text-muted border-border hover:bg-white/10",
};

export default function ActiveKeywords() {
  const { data, isLoading } = useTrends();
  const trends = data?.data?.slice(0, 30) ?? [];

  if (isLoading) {
    return (
      <div className="bg-bg-card border border-border rounded-lg p-4">
        <h3 className="font-heading text-sm font-semibold mb-3 text-text-muted uppercase tracking-wider">
          Active Keywords
        </h3>
        <div className="flex flex-wrap gap-2">
          {[...Array(12)].map((_, i) => (
            <div
              key={i}
              className="h-7 bg-bg-secondary rounded-md animate-pulse"
              style={{ width: `${60 + Math.random() * 60}px` }}
            />
          ))}
        </div>
      </div>
    );
  }

  if (trends.length === 0) return null;

  return (
    <div className="bg-bg-card border border-border rounded-lg p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-heading text-sm font-semibold text-text-muted uppercase tracking-wider">
          Active Keywords
        </h3>
        <span className="text-[10px] text-text-muted font-mono">
          {trends.length} tracked
        </span>
      </div>
      <div className="flex flex-wrap gap-2">
        {trends.map((trend: any) => (
          <Link
            key={trend.id}
            href={`/trends/${trend.id}`}
            className={clsx(
              "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md border text-xs font-medium transition-colors",
              statusColors[trend.trend_status] || statusColors.stable
            )}
          >
            <span>{trend.keyword}</span>
            <span className="opacity-60 font-mono text-[10px]">
              {trend.mention_count}
            </span>
          </Link>
        ))}
      </div>
    </div>
  );
}
