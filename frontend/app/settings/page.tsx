"use client";

import { useState, useEffect } from "react";
import useSWR from "swr";
import { fetcher } from "@/lib/api";
import {
  Brain,
  Check,
  Loader2,
  AlertCircle,
  Key,
  Server,
  Cpu,
} from "lucide-react";
import clsx from "clsx";

const PROVIDER_ICONS: Record<string, typeof Brain> = {
  ollama: Server,
  openai: Brain,
  gemini: Cpu,
  anthropic: Brain,
};

const PROVIDER_COLORS: Record<string, string> = {
  ollama: "border-accent-cyan/30 hover:border-accent-cyan",
  openai: "border-accent-green/30 hover:border-accent-green",
  gemini: "border-accent-amber/30 hover:border-accent-amber",
  anthropic: "border-accent-red/30 hover:border-accent-red",
};

const PROVIDER_ACTIVE_COLORS: Record<string, string> = {
  ollama: "border-accent-cyan bg-accent-cyan/10",
  openai: "border-accent-green bg-accent-green/10",
  gemini: "border-accent-amber bg-accent-amber/10",
  anthropic: "border-accent-red bg-accent-red/10",
};

const SUGGESTED_MODELS: Record<string, string[]> = {
  ollama: ["llama3", "llama3.1", "mistral", "codellama", "gemma2"],
  openai: ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
  gemini: ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
  anthropic: ["claude-sonnet-4-20250514", "claude-haiku-4-5-20251001", "claude-opus-4-20250514"],
};

export default function SettingsPage() {
  const { data, mutate } = useSWR("/api/ai-settings", fetcher);
  const [provider, setProvider] = useState("ollama");
  const [apiKey, setApiKey] = useState("");
  const [modelName, setModelName] = useState("");
  const [baseUrl, setBaseUrl] = useState("");
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);

  const settings = data?.data;
  const providers = data?.providers || {};

  useEffect(() => {
    if (settings) {
      setProvider(settings.provider);
      setModelName(settings.model_name || "");
      setBaseUrl(settings.base_url || "");
    }
  }, [settings]);

  const handleSave = async () => {
    setSaving(true);
    setMessage(null);
    try {
      const res = await fetch("/api/ai-settings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          provider,
          api_key: apiKey || null,
          model_name: modelName || null,
          base_url: baseUrl || null,
        }),
      });
      const result = await res.json();
      if (result.success) {
        setMessage({ type: "success", text: `Saved! Using ${result.data.model_name} via ${provider}` });
        setApiKey("");
        await mutate();
      } else {
        setMessage({ type: "error", text: result.error });
      }
    } catch (e: any) {
      setMessage({ type: "error", text: e.message });
    } finally {
      setSaving(false);
    }
  };

  const needsKey = providers[provider]?.needs_key;

  return (
    <div className="max-w-2xl space-y-6">
      <div>
        <h1 className="font-heading text-xl font-bold">AI Provider Settings</h1>
        <p className="text-text-muted text-sm mt-1">
          Choose your AI provider for trend insights. Use local Ollama for free
          or connect a cloud API.
        </p>
      </div>

      {/* Current Status */}
      {settings?.status && (
        <div className="bg-bg-card border border-border rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span
                className={clsx(
                  "w-2.5 h-2.5 rounded-full",
                  settings.status.status === "online" || settings.status.status === "configured"
                    ? "bg-accent-green"
                    : "bg-accent-red"
                )}
              />
              <span className="text-sm">
                <span className="text-text-muted">Active:</span>{" "}
                <span className="font-semibold capitalize">{settings.status.provider}</span>
                {" "}
                <span className="text-text-muted">({settings.status.model})</span>
              </span>
            </div>
            <span
              className={clsx(
                "text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded",
                settings.status.status === "online" || settings.status.status === "configured"
                  ? "bg-accent-green/10 text-accent-green"
                  : "bg-accent-red/10 text-accent-red"
              )}
            >
              {settings.status.status}
            </span>
          </div>
          {settings.api_key_set && (
            <p className="text-[11px] text-text-muted mt-2">
              <Key className="w-3 h-3 inline mr-1" />
              API key configured ({settings.api_key_preview})
            </p>
          )}
        </div>
      )}

      {/* Provider Selection */}
      <div>
        <label className="text-xs text-text-muted uppercase tracking-wider font-semibold block mb-3">
          Select Provider
        </label>
        <div className="grid grid-cols-2 gap-3">
          {Object.entries(providers).map(([key, info]: [string, any]) => {
            const Icon = PROVIDER_ICONS[key] || Brain;
            const isActive = provider === key;
            return (
              <button
                key={key}
                onClick={() => {
                  setProvider(key);
                  setModelName(info.default_model);
                  setApiKey("");
                  setBaseUrl("");
                }}
                className={clsx(
                  "flex items-center gap-3 p-4 rounded-lg border-2 transition-all text-left",
                  isActive
                    ? PROVIDER_ACTIVE_COLORS[key]
                    : `border-border ${PROVIDER_COLORS[key]}`
                )}
              >
                <Icon className="w-5 h-5 flex-shrink-0" />
                <div>
                  <p className="text-sm font-semibold">{info.label}</p>
                  <p className="text-[10px] text-text-muted">
                    {info.needs_key ? "Requires API key" : "Free, runs locally"}
                  </p>
                </div>
                {isActive && (
                  <Check className="w-4 h-4 ml-auto text-accent-green" />
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Configuration */}
      <div className="bg-bg-card border border-border rounded-lg p-5 space-y-4">
        <h3 className="font-heading text-sm font-semibold uppercase tracking-wider text-text-muted">
          Configuration
        </h3>

        {/* API Key */}
        {needsKey && (
          <div>
            <label className="text-xs text-text-muted block mb-1.5">
              API Key
            </label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder={
                settings?.api_key_set && settings?.provider === provider
                  ? "Leave blank to keep existing key"
                  : "Enter your API key..."
              }
              className="w-full bg-bg-secondary border border-border rounded-md px-3 py-2 text-sm text-text-primary placeholder:text-text-muted/50 focus:outline-none focus:border-accent-cyan"
            />
          </div>
        )}

        {/* Model */}
        <div>
          <label className="text-xs text-text-muted block mb-1.5">
            Model
          </label>
          <input
            type="text"
            value={modelName}
            onChange={(e) => setModelName(e.target.value)}
            placeholder="Model name..."
            className="w-full bg-bg-secondary border border-border rounded-md px-3 py-2 text-sm text-text-primary placeholder:text-text-muted/50 focus:outline-none focus:border-accent-cyan"
          />
          <div className="flex flex-wrap gap-1.5 mt-2">
            {(SUGGESTED_MODELS[provider] || []).map((m) => (
              <button
                key={m}
                onClick={() => setModelName(m)}
                className={clsx(
                  "text-[10px] px-2 py-0.5 rounded-md border transition-colors",
                  modelName === m
                    ? "border-accent-cyan bg-accent-cyan/10 text-accent-cyan"
                    : "border-border text-text-muted hover:text-text-primary hover:border-text-muted"
                )}
              >
                {m}
              </button>
            ))}
          </div>
        </div>

        {/* Base URL (optional) */}
        {(provider === "ollama" || provider === "openai") && (
          <div>
            <label className="text-xs text-text-muted block mb-1.5">
              Base URL <span className="opacity-50">(optional)</span>
            </label>
            <input
              type="text"
              value={baseUrl}
              onChange={(e) => setBaseUrl(e.target.value)}
              placeholder={
                provider === "ollama"
                  ? "http://localhost:11434"
                  : "https://api.openai.com/v1"
              }
              className="w-full bg-bg-secondary border border-border rounded-md px-3 py-2 text-sm text-text-primary placeholder:text-text-muted/50 focus:outline-none focus:border-accent-cyan"
            />
          </div>
        )}

        {/* Save */}
        <button
          onClick={handleSave}
          disabled={saving || (needsKey && !apiKey && !(settings?.api_key_set && settings?.provider === provider))}
          className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-accent-cyan/10 text-accent-cyan rounded-lg text-sm font-semibold hover:bg-accent-cyan/20 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {saving ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <Check className="w-4 h-4" />
          )}
          {saving ? "Saving..." : "Save Settings"}
        </button>

        {/* Message */}
        {message && (
          <div
            className={clsx(
              "flex items-center gap-2 p-3 rounded-lg text-sm",
              message.type === "success"
                ? "bg-accent-green/10 text-accent-green"
                : "bg-accent-red/10 text-accent-red"
            )}
          >
            {message.type === "success" ? (
              <Check className="w-4 h-4" />
            ) : (
              <AlertCircle className="w-4 h-4" />
            )}
            {message.text}
          </div>
        )}
      </div>
    </div>
  );
}
