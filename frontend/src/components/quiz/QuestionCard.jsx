import AnswerOption from "./AnswerOption";

export default function QuestionCard({ question, selectedKey, onSelect }) {
  return (
    <div className="quiz-card">
      <h2 className="quiz-question-text">{question.text}</h2>
      <div className="quiz-options">
        {question.choices.map((choice, i) => (
          <AnswerOption
            key={choice.key}
            choice={choice}
            selected={selectedKey === choice.key}
            onSelect={() => onSelect(question.id, choice.key)}
            label={String.fromCharCode(65 + i)}
          />
        ))}
      </div>
    </div>
  );
}
