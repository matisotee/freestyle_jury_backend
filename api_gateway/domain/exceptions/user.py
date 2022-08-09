class ExistingUserError(Exception):

    def __init__(self):
        super().__init__('The user you are trying to create already exists')


class NotExistentUserError(Exception):

    def __init__(self):
        super().__init__('You need to be registered to execute this action')
