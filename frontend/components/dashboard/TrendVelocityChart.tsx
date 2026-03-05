"use client";

import { useTrends } from "@/lib/hooks/useTrends";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

const COLORS = ["#00d4ff", "#ffb300", "#00ff88", "#ff4d6d", "#a855f7"];

export default function TrendVelocityChart() {
  const { data, isLoading } = useTrends();
  const trends = data?.data?.slice(0, 5) ?? [];

  if (isLoading || trends.length === 0) {
    return (
      <div className="bg-bg-card border border-border rounded-lg p-4">
        <h3 className="font-heading text-sm font-semibold mb-4 text-text-muted uppercase tracking-wider">
          Trend Velocity
        </h3>
        <div className="h-64 flex items-center justify-center text-text-muted text-sm">
          {isLoading ? "Loading chart..." : "No trend data yet"}
        </div>
      </div>
    );
  }

  // Build chart data from trends
  const chartData = trends.map((t: any, i: number) => ({
    name: t.keyword.length > 15 ? t.keyword.slice(0, 15) + "..." : t.keyword,
    velocity: t.velocity_score,
    mentions: t.mention_count,
  }));

  return (
    <div className="bg-bg-card border border-border rounded-lg p-4">
      <h3 className="font-heading text-sm font-semibold mb-4 text-text-muted uppercase tracking-wider">
        Trend Velocity - Top 5
      </h3>
      <ResponsiveContainer width="100%" height={260}>
        <AreaChart data={chartData}>
          <defs>
            {COLORS.map((color, i) => (
              <linearGradient
                key={i}
                id={`gradient-${i}`}
                x1="0"
                y1="0"
                x2="0"
                y2="1"
              >
                <stop offset="0%" stopColor={color} stopOpacity={0.3} />
                <stop offset="100%" stopColor={color} stopOpacity={0} />
              </linearGradient>
            ))}
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#1f2d45" />
          <XAxis
            dataKey="name"
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
              fontSize: "12px",
            }}
          />
          <Area
            type="monotone"
            dataKey="velocity"
            stroke={COLORS[0]}
            fill={`url(#gradient-0)`}
            strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
