import Wordmark from "./Wordmark";

/**
 * Brand lockup — Wordmark only.
 * layout="horizontal" — inline (navbar)
 * layout="stacked"    — block (landing hero)
 */
export default function Logo({
  layout = "horizontal",
  wordmarkSize,
  className = "",
}) {
  const isStacked = layout === "stacked";
  const textSize = wordmarkSize || (isStacked ? "lg" : "md");

  return (
    <span className={`brand-logo ${className}`}>
      <Wordmark size={textSize} />
    </span>
  );
}
