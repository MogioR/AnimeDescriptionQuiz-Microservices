import asyncio
from .QuestionGenerator import Question
from .QuestionGenerator import DefaultQuestionGenerator
from _Shared_modules._Models import TitleNameModel, UserStatsModel


MIN_MASK_SIZE = 3


class DefaultQuiz:
    def __init__(self, quiz_settings: dict, question_settings: dict, users: list):
        self.round = 0
        self.timer = 0
        self.phase = 0
        self.quiz_in_pause = False

        self.quiz_settings = quiz_settings
        self.question_generator = DefaultQuestionGenerator(question_settings, [a.user_id for a in users])

        self.users = {}
        self.users_answers = {}
        self.question = None

    async def update(self):
        if self.phase != 0 and not self.quiz_in_pause:
            self.timer += 1

        if self.phase == 1:
            # Send new question
            self.question = await self.question_generator.get_question()
            self.question.question_raw.question_made_up_times += len(self.users)
            self.question.question_raw.save()

            message_to_users = {
                'action': 'quiz',
                'type': 'new_question',
                'new_question': self.question.question_message_data()
            }
            for user in self.users.values():
                await user.socket.send(message_to_users)

            self.timer = 0
            self.phase = 2
        elif self.phase == 2 and self.timer > self.quiz_settings['question_time']:
            # Send results
            await self.check_answers()
            self.question.question_raw.question_guessed_times +=\
                len([u['correct'] for u in self.users_answers if u['correct']])
            self.question.question_raw.save()

            message_to_users = {
                'action': 'quiz',
                'type': 'results',
                'true_answer': self.question.true_answer_message_data(),
                'users_answers': self.users_answers
            }
            for user in self.users.values():
                await user.socket.send(message_to_users)

            self.timer = 0
            self.phase = 3

        elif self.phase == 3 and self.timer > self.quiz_settings['answer_time']:
            # New round
            if self.round < self.quiz_settings['round_count']:
                self.round += 1
                self.phase = 1
            else:
                self.round = 0
                self.phase = 0
            self.timer = 0

    async def start_quiz(self, users):
        self.users = {user.user_id: user for user in users}
        self.users_answers = {user.user_id: {
            'answer': '',
            'correct': False,
            'user_stats': UserStatsModel.select().where(UserStatsModel.user_stats_user_id == user.user_id).get()
        } for user in users}

        question_count = await self.question_generator.get_questions(self.quiz_settings['round_count'])
        if question_count > 0:
            self.phase = 1
        return question_count

    async def get_hints(self, user_id, answer: str):
        if len(answer) >= MIN_MASK_SIZE:
            hints = TitleNameModel.select().where(TitleNameModel.title_name_name.contains(answer))
            await self.users[user_id].socket.send({
                'action': 'quiz',
                'type': 'hints',
                'data': hints
            })

    async def set_answer(self, user_id: int, answer: str):
        self.users_answers[user_id] = answer

    async def check_answers(self):
        for user_id in self.users_answers.keys():
            try:
                title_id = (
                    TitleNameModel.select().where(
                        TitleNameModel.title_name_name == self.users_answers[user_id]['answer']
                    ).get().title_name_title_id)
            except Exception as e:
                title_id = None

            self.users_answers[user_id]['correct'] = title_id in self.question.answers_ids
            self.users_answers[user_id]['user_stats'].user_stats_exp += \
                1 if title_id in self.question.answers_ids else 0
            self.users_answers[user_id]['user_stats'].user_stats_made_up_times += 1
            self.users_answers[user_id]['user_stats'].user_stats_guessed_times += \
                1 if title_id in self.question.answers_ids else 0
            self.users_answers[user_id]['user_stats'].save()

    async def stop_quiz(self):
        pass

    async def resume_quiz(self):
        pass
