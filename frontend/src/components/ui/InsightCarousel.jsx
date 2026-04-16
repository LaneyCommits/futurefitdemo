import useMediaQuery from "../../hooks/useMediaQuery";

const REFLECTIONS = [
  {
    quote: "It finally explained why I overthink group projects.",
    name: "Jordan M.",
    archetype: "Analytical Problem Solver",
  },
  {
    quote: "I didn\u2019t expect it to feel this accurate.",
    name: "Priya K.",
    archetype: "Creative Builder",
  },
  {
    quote: "It gave me clarity I didn\u2019t get from other career tests.",
    name: "Marcus T.",
    archetype: "Structured Systems Thinker",
  },
  {
    quote: "The results actually matched how I work, not how I wish I worked.",
    name: "Elena R.",
    archetype: "People-Oriented Strategist",
  },
  {
    quote: "It helped me understand what environments I struggle in.",
    name: "Sam W.",
    archetype: "Explorer / Adaptive Thinker",
  },
  {
    quote: "This felt more like self-reflection than a quiz.",
    name: "Ava L.",
    archetype: "Impact-Driven Visionary",
  },
];

function InsightCard({ quote, name, archetype }) {
  return (
    <div className="insight-card">
      <p className="insight-quote">{quote}</p>
      <div className="insight-footer">
        <span className="insight-name">{name}</span>
        <span className="insight-archetype">{archetype}</span>
      </div>
    </div>
  );
}

export default function InsightCarousel() {
  const isDesktop = useMediaQuery("(min-width: 768px)");
  const items = [...REFLECTIONS, ...REFLECTIONS];

  return (
    <section className="insight-section">
      <div className="insight-header">
        <h2 className="insight-section-title">User Reflections</h2>
        <p className="insight-section-sub">
          Real insights from people discovering their path
        </p>
      </div>

      <div className="insight-carousel-wrapper">
        <div className="insight-track insight-track-scroll">
          {items.map((item, i) => (
            <InsightCard key={`${item.name}-${i}`} {...item} />
          ))}
        </div>
      </div>
    </section>
  );
}
