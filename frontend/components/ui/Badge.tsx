import clsx from "clsx";

const statusStyles: Record<string, string> = {
  emerging: "bg-accent-red/20 text-accent-red animate-pulse-dot",
  rising: "bg-accent-amber/20 text-accent-amber",
  stable: "bg-accent-cyan/20 text-accent-cyan",
  declining: "bg-gray-500/20 text-gray-400",
};

export default function Badge({ status }: { status: string }) {
  return (
    <span
      className={clsx(
        "px-2 py-0.5 rounded text-[10px] font-semibold uppercase tracking-wider",
        statusStyles[status] || statusStyles.stable
      )}
    >
      {status}
    </span>
  );
}
