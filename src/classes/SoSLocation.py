class SoSLocation:
    def __init__(self, location):
        self._id = location[0]
        self._location = location[1]
        self._address = location[2]
        self._zip = location[3]

    def get_id(self):
        return self._id

    def get_location(self):
        return self._location

    def get_address(self):
        return self._address

    def get_zip(self):
        return self._zip
