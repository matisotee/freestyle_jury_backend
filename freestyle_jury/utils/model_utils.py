from freestyle_jury.exceptions.exceptions import FieldMissingException


def check_missing_required_fields(_object, _class):
    missing_field = []
    for field in _class.MANDATORY_FIELDS:
        if not getattr(_object, field, None):
            missing_field.append(field)
    if len(missing_field) > 0:
        raise FieldMissingException(missing_field)
