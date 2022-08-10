from .question import Question


class BaseQuestionGenerator:
    def get_questions(self, questions_count: int):
        pass

    def get_question(self) -> Question:
        pass

    def check_question(self, question: Question, answer: str) -> bool:
        pass
