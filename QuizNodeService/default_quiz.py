from QuestionGenerator.default_question_generator import DefaultQuestionGenerator


class DefaultQuiz:
    def __init__(self, quiz_settings: dict, question_settings: dict, users: list):
        self.round = 0
        self.timer = 0
        self.phase = 0
        self.quiz_in_pause = False

        self.quiz_settings = quiz_settings
        self.question_generator = DefaultQuestionGenerator(question_settings, [a.user_id for a in users])
        self.users = users

        self.question = None
        self.users_answers = [{'user': user.user_id, 'answer': '', 'correct': False} for user in users]

    def update(self):
        if self.phase != 0 and not self.quiz_in_pause:
            self.timer += 1

        if self.phase == 1:
            # Send new question
            self.question = self.question_generator.get_question()
            message_to_users = {
                'action': 'quiz',
                'type': 'new_question',
                'new_question': self.question.question_message_data()
            }
            for user in self.users:
                user.socket.send(message_to_users)

            self.timer = 0
            self.phase = 2
        elif self.phase == 2 and self.timer > self.quiz_settings['question_time']:
            # Send results
            message_to_users = {
                'action': 'quiz',
                'type': 'results',
                'true_answer': self.question.true_answer_message_data(),
                'users_answers': self.users_answers
            }
            for user in self.users:
                user.socket.send(message_to_users)

            self.timer = 0
            self.phase = 3

        elif self.phase == 3 and self.timer > self.quiz_settings['answer_time']:
            self.timer = 0
            if self.round < self.quiz_settings['round_count']:
                self.round += 1
                self.phase = 1
            else:
                self.round = 0
                self.phase = 0

    def start_quiz(self, count_of_rounds: int):
        self.phase = 1
        self.question_generator.get_questions(count_of_rounds)

    def stop_quiz(self):
        pass

    def resume_quiz(self):
        pass