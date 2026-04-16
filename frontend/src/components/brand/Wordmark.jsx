/**
 * "ExploringU" text wordmark. Sage accent on "U".
 */
export default function Wordmark({
  size = "md",
  className = "",
}) {
  const sizes = {
    sm: { fontSize: "0.9375rem", letterSpacing: "0.03em" },
    md: { fontSize: "1.125rem", letterSpacing: "0.03em" },
    lg: { fontSize: "1.5rem", letterSpacing: "0.02em" },
    xl: { fontSize: "2rem", letterSpacing: "0.01em" },
  };

  const s = sizes[size] || sizes.md;

  return (
    <span
      className={`brand-wordmark ${className}`}
      style={{
        fontFamily: "var(--font)",
        fontWeight: 600,
        fontSize: s.fontSize,
        letterSpacing: s.letterSpacing,
        lineHeight: 1,
        color: "var(--text)",
        whiteSpace: "nowrap",
      }}
    >
      Exploring
      <span style={{ color: "var(--color-identity)" }}>U</span>
    </span>
  );
}
