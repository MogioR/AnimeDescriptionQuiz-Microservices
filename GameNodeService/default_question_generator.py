class DefaultQuestionGenerator:
    def __init__(self, question_settings: dict, players_ids: list):
        self.question_settings = question_settings
        self.players_ids = players_ids

    def get_question(self):
        # TitlesModel.select().where(
        #     (TitlesModel.titles_has_description == True) & (TitlesModel.titles_rating >= 7.5)).order_by(
        #     fn.Random()).get()
        pass
