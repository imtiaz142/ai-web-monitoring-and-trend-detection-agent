"use client";

import StatsBar from "@/components/dashboard/StatsBar";
import ActiveKeywords from "@/components/dashboard/ActiveKeywords";
import TopTrendsPanel from "@/components/dashboard/TopTrendsPanel";
import TrendVelocityChart from "@/components/dashboard/TrendVelocityChart";
import ArticlesFeed from "@/components/dashboard/ArticlesFeed";
import InsightCard from "@/components/dashboard/InsightCard";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <StatsBar />
      <ActiveKeywords />
      <div className="grid grid-cols-2 gap-6">
        <TopTrendsPanel />
        <TrendVelocityChart />
      </div>
      <div className="grid grid-cols-2 gap-6">
        <ArticlesFeed />
        <InsightCard />
      </div>
    </div>
  );
}
