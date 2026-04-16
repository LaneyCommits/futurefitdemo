export default function ProgressBar({ current, total, answers, questions }) {
  return (
    <div className="seg-progress">
      {Array.from({ length: total }, (_, i) => {
        let cls = "seg-bar";
        if (i < current - 1 || (questions && answers && answers[questions[i]?.id])) {
          cls += " seg-bar-complete";
        } else if (i === current - 1) {
          cls += " seg-bar-active";
        }
        return (
          <div key={i} className={cls}>
            <div className="seg-bar-fill" />
          </div>
        );
      })}
    </div>
  );
}
