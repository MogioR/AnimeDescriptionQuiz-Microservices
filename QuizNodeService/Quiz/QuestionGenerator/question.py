class Question:
    def __init__(self, source: dict, lang: int, difficulty: float, question_type: int, answers_ids: list,
                 answer_data: dict, question_raw):
        self.lang = lang
        self.difficulty = difficulty
        self.question_type = question_type
        self.question_source = source['question']
        self.answer_sources = source['answer']
        self.question_raw = question_raw

        self.answers_ids = answers_ids
        self.answer_data = answer_data

    def question_message_data(self):
        return {
            'question_type': self.question_type,
            'question_sources': self.question_source
        }

    def true_answer_message_data(self):
        return {
            'answer_sources': self.answer_sources,
            'answer_title':  self.answer_data
        }
