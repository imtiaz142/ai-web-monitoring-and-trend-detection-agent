"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BarChart3, Brain, Home, Code2, ExternalLink } from "lucide-react";
import clsx from "clsx";

const navItems = [
  { href: "/", label: "Dashboard", icon: Home },
  { href: "/insights", label: "AI Insights", icon: Brain },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-60 bg-bg-secondary border-r border-border flex flex-col">
      <div className="p-5 border-b border-border">
        <div className="flex items-center gap-2">
          <BarChart3 className="w-6 h-6 text-accent-cyan" />
          <h1 className="font-heading text-lg font-bold tracking-tight">
            TREND AGENT
          </h1>
        </div>
        <p className="text-text-muted text-xs mt-1">AI Monitoring System</p>
      </div>
      <nav className="flex-1 p-3 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={clsx(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors",
                active
                  ? "bg-accent-cyan/10 text-accent-cyan"
                  : "text-text-muted hover:text-text-primary hover:bg-white/5"
              )}
            >
              <Icon className="w-4 h-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>
      <div className="p-4 border-t border-border space-y-3">
        <div>
          <div className="flex items-center gap-1.5 mb-1">
            <Code2 className="w-3.5 h-3.5 text-accent-cyan" />
            <span className="text-[10px] text-text-muted uppercase tracking-wider font-semibold">
              Developer
            </span>
          </div>
          <p className="text-sm font-medium text-text-primary">Imtiaz Ali</p>
          <a
            href="https://fullstackaiengineerpro.com/"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-xs text-accent-cyan hover:text-accent-cyan/80 transition-colors mt-0.5"
          >
            fullstackaiengineerpro.com
            <ExternalLink className="w-3 h-3" />
          </a>
        </div>
        <p className="text-text-muted text-[10px]">v1.0 | Local Mode</p>
      </div>
    </aside>
  );
}
