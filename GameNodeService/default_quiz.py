

class DefaultQuiz:
    def __init__(self, quiz_options: dict, question_options: dict):
        self.round = 0
        self.timer = 0
        self.phase = 0
        self.quiz_in_pause = False

        self.quiz_options = quiz_options

    def update(self) -> list:
        if self.phase != 0 and not self.quiz_in_pause:
            self.timer += 1

        if self.phase == 1:
            # Send new question

            self.timer = 0
            self.phase = 2
        elif self.phase == 2 and self.timer > self.quiz_options['question_time']:
            # Send results

            self.timer = 0
            self.phase = 3

        elif self.phase == 3 and self.timer > self.quiz_options['answer_time']:
            self.timer = 0
            if self.round < self.quiz_options['round_count']:
                self.round += 1
                self.phase = 1
            else:
                self.round = 0
                self.phase = 0

    def start_quiz(self):
        self.phase = 1

    def stop_quiz(self):
        pass

    def resume_quiz(self):
        pass
