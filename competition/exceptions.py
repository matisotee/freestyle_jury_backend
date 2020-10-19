
DUPLICATED_UNIQUE_FIELD_STRING = 'duplicate key error collection'


class OrganizerCreationError(Exception):

    def __init__(self, *args):
        super().__init__(*args)
