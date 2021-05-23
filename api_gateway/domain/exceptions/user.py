class ExistingUserError(Exception):

    def __init__(self):
        super().__init__('The user you are trying to create already exists')
