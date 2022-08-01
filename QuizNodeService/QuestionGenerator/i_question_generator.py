from question import Question


class IQuestionGenerator:
    def get_question(self) -> Question:
        pass

    def check_question(self, question: Question, answer: str) -> bool:
        pass
