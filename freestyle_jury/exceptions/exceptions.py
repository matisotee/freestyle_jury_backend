class FieldMissingException(Exception):

    def __init__(self, fields_arr):
        self.message = ', '.join(fields_arr)
