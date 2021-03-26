class OrganizerCreationError(Exception):

    def __init__(self, *args):
        super().__init__(*args)


class CompetitionCreationError(Exception):

    def __init__(self, *args):
        super().__init__(*args)


class CompetitionPastDateError(Exception):

    def __init__(self, *args):
        super().__init__(*args)
