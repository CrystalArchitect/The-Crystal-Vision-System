// SPDX-License-Identifier: MIT

interface Props {
  value: number;
  onChange: (v: number) => void;
  size?: "sm" | "md";
}

export default function RatingStars({ value, onChange, size = "sm" }: Props) {
  const cls = size === "sm" ? "text-sm" : "text-lg";
  return (
    <span className={`inline-flex ${cls} leading-none`} onClick={(e) => e.stopPropagation()}>
      {[1, 2, 3, 4, 5].map((n) => (
        <button
          key={n}
          type="button"
          aria-label={`${n} stars`}
          onClick={() => onChange(n === value ? 0 : n)}
          className={n <= value ? "text-accent" : "text-ink-700 hover:text-neutral-400"}
        >
          ★
        </button>
      ))}
    </span>
  );
}
