"use client";

import { useTrend, useTrendHistory } from "@/lib/hooks/useTrends";
import Badge from "@/components/ui/Badge";
import { ArrowLeft, ExternalLink } from "lucide-react";
import Link from "next/link";
import { formatDistanceToNow } from "date-fns";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
export default function TrendDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const { id } = params;
  const { data: trendData, isLoading } = useTrend(id);
  const { data: historyData } = useTrendHistory(id);

  const trend = trendData?.data;
  const history = historyData?.data ?? [];

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="h-8 w-48 bg-bg-card animate-pulse rounded" />
        <div className="h-64 bg-bg-card animate-pulse rounded" />
      </div>
    );
  }

  if (!trend) {
    return (
      <div className="text-center py-20">
        <p className="text-text-muted">Trend not found</p>
        <Link href="/" className="text-accent-cyan text-sm mt-2 inline-block">
          Back to dashboard
        </Link>
      </div>
    );
  }

  const chartData = history.map((s: any) => ({
    time: new Date(s.snapshot_at).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    }),
    velocity: s.velocity_score,
    mentions: s.mention_count,
  }));

  return (
    <div className="space-y-6">
      <Link
        href="/"
        className="inline-flex items-center gap-1.5 text-text-muted hover:text-text-primary text-sm transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to dashboard
      </Link>

      <div className="bg-bg-card border border-border rounded-lg p-6">
        <div className="flex items-center gap-4 mb-2">
          <h1 className="font-heading text-2xl font-bold">{trend.keyword}</h1>
          <Badge status={trend.trend_status} />
        </div>
        <div className="flex gap-6 text-sm text-text-muted">
          <span>
            Velocity:{" "}
            <span className="text-accent-cyan font-mono">
              {trend.velocity_score.toFixed(2)}
            </span>
          </span>
          <span>
            Mentions:{" "}
            <span className="text-text-primary font-mono">
              {trend.mention_count}
            </span>
          </span>
          <span>
            Articles:{" "}
            <span className="text-text-primary font-mono">
              {trend.article_count}
            </span>
          </span>
          {trend.first_seen_at && (
            <span>
              First seen:{" "}
              {formatDistanceToNow(new Date(trend.first_seen_at), {
                addSuffix: true,
              })}
            </span>
          )}
        </div>

        {trend.related_keywords && trend.related_keywords.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-4">
            {trend.related_keywords.map((kw: string, i: number) => (
              <span
                key={i}
                className="text-xs bg-accent-cyan/10 text-accent-cyan px-2 py-1 rounded-md"
              >
                {kw}
              </span>
            ))}
          </div>
        )}
      </div>

      {chartData.length > 0 && (
        <div className="bg-bg-card border border-border rounded-lg p-6">
          <h3 className="font-heading text-sm font-semibold text-text-muted uppercase tracking-wider mb-4">
            Velocity History
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="velGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#00d4ff" stopOpacity={0.3} />
                  <stop offset="100%" stopColor="#00d4ff" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2d45" />
              <XAxis
                dataKey="time"
                tick={{ fill: "#64748b", fontSize: 11 }}
                axisLine={{ stroke: "#1f2d45" }}
              />
              <YAxis
                tick={{ fill: "#64748b", fontSize: 11 }}
                axisLine={{ stroke: "#1f2d45" }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#111827",
                  border: "1px solid #1f2d45",
                  borderRadius: "8px",
                }}
              />
              <Area
                type="monotone"
                dataKey="velocity"
                stroke="#00d4ff"
                fill="url(#velGrad)"
                strokeWidth={2}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}

      {trend.articles && trend.articles.length > 0 && (
        <div className="bg-bg-card border border-border rounded-lg p-6">
          <h3 className="font-heading text-sm font-semibold text-text-muted uppercase tracking-wider mb-4">
            Related Articles
          </h3>
          <div className="space-y-3">
            {trend.articles.map((article: any) => (
              <a
                key={article.id}
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-between p-3 rounded-lg border border-border/50 hover:border-accent-cyan/30 transition-all group"
              >
                <div>
                  <span className="text-[10px] text-accent-cyan uppercase tracking-wider">
                    {article.source_name}
                  </span>
                  <h4 className="text-sm group-hover:text-accent-cyan transition-colors">
                    {article.title}
                  </h4>
                  {article.published_at && (
                    <span className="text-[10px] text-text-muted">
                      {formatDistanceToNow(new Date(article.published_at), {
                        addSuffix: true,
                      })}
                    </span>
                  )}
                </div>
                <ExternalLink className="w-3.5 h-3.5 text-text-muted opacity-0 group-hover:opacity-100" />
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
