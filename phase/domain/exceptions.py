class CompetitionAlreadyStarted(Exception):

    def __init__(self, *args):
        super().__init__(*args)


class FinalPhaseAlreadyCreated(Exception):

    def __init__(self, *args):
        super().__init__(*args)


class InvalidNumberOfWinners(Exception):

    def __init__(self, *args):
        super().__init__(*args)


class NotExistentCompetitionError(Exception):

    def __init__(self, *args):
        super().__init__(*args)
