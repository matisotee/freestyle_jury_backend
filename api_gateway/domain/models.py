from bson import ObjectId


class User:

    def __init__(self, provider_id, name, last_name, email, phone_number=None, aka='', _id=None):
        self._id = _id if type(_id) != str else ObjectId(_id)
        self.provider_id = provider_id
        self.name = name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.aka = aka

    def to_dict(self):
        dict_data = {
            'provider_id': self.provider_id,
            'name': self.name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'aka': self.aka
        }
        if self._id is not None:
            dict_data['_id':] = self._id

        return dict_data
