"use client";

import clsx from "clsx";

export default function LiveIndicator({
  lastScrape,
}: {
  lastScrape?: string | null;
}) {
  let status: "live" | "delayed" | "stale" = "stale";
  let label = "STALE";
  let dotColor = "bg-accent-red";

  if (lastScrape) {
    const diff = (Date.now() - new Date(lastScrape).getTime()) / 60000;
    if (diff < 5) {
      status = "live";
      label = "LIVE";
      dotColor = "bg-accent-green";
    } else if (diff < 30) {
      status = "delayed";
      label = "DELAYED";
      dotColor = "bg-accent-amber";
    }
  }

  return (
    <div className="flex items-center gap-1.5">
      <span
        className={clsx(
          "w-2 h-2 rounded-full",
          dotColor,
          status === "live" && "animate-pulse-dot"
        )}
      />
      <span
        className={clsx(
          "text-[10px] font-bold tracking-wider",
          status === "live" && "text-accent-green",
          status === "delayed" && "text-accent-amber",
          status === "stale" && "text-accent-red"
        )}
      >
        {label}
      </span>
    </div>
  );
}
