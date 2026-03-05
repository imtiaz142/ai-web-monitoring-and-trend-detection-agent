"use client";

import { useArticles } from "@/lib/hooks/useArticles";
import { formatDistanceToNow } from "date-fns";
import { ExternalLink } from "lucide-react";

export default function ArticlesFeed() {
  const { data, isLoading } = useArticles();
  const articles = data?.data ?? [];

  if (isLoading) {
    return (
      <div className="bg-bg-card border border-border rounded-lg p-4">
        <h3 className="font-heading text-sm font-semibold mb-4 text-text-muted uppercase tracking-wider">
          Latest Articles
        </h3>
        <div className="space-y-3">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="space-y-2">
              <div className="h-4 bg-bg-secondary rounded w-3/4 animate-pulse" />
              <div className="h-3 bg-bg-secondary rounded w-1/2 animate-pulse" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-bg-card border border-border rounded-lg p-4">
      <h3 className="font-heading text-sm font-semibold mb-4 text-text-muted uppercase tracking-wider">
        Latest Articles
      </h3>
      <div className="space-y-3 max-h-[500px] overflow-y-auto pr-1">
        {articles.map((article: any) => (
          <a
            key={article.id}
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="block p-3 rounded-lg border border-border/50 hover:border-accent-cyan/30 hover:bg-white/[0.02] transition-all group"
          >
            <div className="flex items-start justify-between gap-2">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-[10px] font-semibold uppercase tracking-wider text-accent-cyan bg-accent-cyan/10 px-1.5 py-0.5 rounded">
                    {article.source_name}
                  </span>
                  {article.published_at && (
                    <span className="text-text-muted text-[10px]">
                      {formatDistanceToNow(new Date(article.published_at), {
                        addSuffix: true,
                      })}
                    </span>
                  )}
                </div>
                <h4 className="text-sm font-medium leading-snug group-hover:text-accent-cyan transition-colors line-clamp-2">
                  {article.title}
                </h4>
                {article.keywords && article.keywords.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {article.keywords.slice(0, 3).map((kw: string, i: number) => (
                      <span
                        key={i}
                        className="text-[9px] text-text-muted bg-bg-secondary px-1.5 py-0.5 rounded"
                      >
                        {kw}
                      </span>
                    ))}
                  </div>
                )}
              </div>
              <ExternalLink className="w-3.5 h-3.5 text-text-muted opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0 mt-1" />
            </div>
          </a>
        ))}
        {articles.length === 0 && (
          <p className="text-text-muted text-sm text-center py-8">
            No articles yet. Waiting for first scrape...
          </p>
        )}
      </div>
    </div>
  );
}
