export default function AnswerOption({ choice, selected, onSelect, label }) {
  return (
    <button
      type="button"
      className={`quiz-option${selected ? " quiz-option-selected" : ""}`}
      onClick={onSelect}
    >
      <span className="quiz-option-marker">{label}</span>
      <span className="quiz-option-label">{choice.text}</span>
    </button>
  );
}
