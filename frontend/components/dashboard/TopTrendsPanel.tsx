"use client";

import { useTrends } from "@/lib/hooks/useTrends";
import Badge from "@/components/ui/Badge";
import Link from "next/link";
import clsx from "clsx";

export default function TopTrendsPanel() {
  const { data, isLoading } = useTrends();
  const trends = data?.data?.slice(0, 15) ?? [];

  const maxVelocity = Math.max(...trends.map((t: any) => t.velocity_score), 1);

  if (isLoading) {
    return (
      <div className="bg-bg-card border border-border rounded-lg p-4">
        <h3 className="font-heading text-sm font-semibold mb-4 text-text-muted uppercase tracking-wider">
          Top Trends
        </h3>
        <div className="space-y-3">
          {[...Array(5)].map((_, i) => (
            <div
              key={i}
              className="h-10 bg-bg-secondary rounded animate-pulse"
            />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-bg-card border border-border rounded-lg p-4">
      <h3 className="font-heading text-sm font-semibold mb-4 text-text-muted uppercase tracking-wider">
        Top Trends
      </h3>
      <div className="space-y-2">
        {trends.map((trend: any, i: number) => (
          <Link
            key={trend.id}
            href={`/trends/${trend.id}`}
            className="flex items-center gap-3 p-2 rounded-lg hover:bg-white/5 transition-colors group"
          >
            <span className="text-text-muted text-xs w-5 text-right font-mono">
              {i + 1}
            </span>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium truncate group-hover:text-accent-cyan transition-colors">
                  {trend.keyword}
                </span>
                <Badge status={trend.trend_status} />
              </div>
              <div className="mt-1 h-1.5 bg-bg-secondary rounded-full overflow-hidden">
                <div
                  className={clsx(
                    "h-full rounded-full animate-velocity",
                    trend.trend_status === "emerging"
                      ? "bg-accent-red"
                      : trend.trend_status === "rising"
                      ? "bg-accent-amber"
                      : "bg-accent-cyan"
                  )}
                  style={{
                    width: `${(trend.velocity_score / maxVelocity) * 100}%`,
                  }}
                />
              </div>
            </div>
            <span className="text-text-muted text-xs font-mono">
              {trend.article_count} articles
            </span>
          </Link>
        ))}
        {trends.length === 0 && (
          <p className="text-text-muted text-sm text-center py-8">
            No trends detected yet. Waiting for first scrape...
          </p>
        )}
      </div>
    </div>
  );
}
