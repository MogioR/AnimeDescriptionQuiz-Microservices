class SmartDict:
    def __init__(self):
        self.value_key = dict()
        self.key_value = dict()

    def del_by_key(self, key):
        value = self.key_value[key]
        del self.value_key[value]
        del self.key_value[key]

    def del_by_value(self, value):
        key = self.value_key[value]
        del self.value_key[value]
        del self.key_value[key]

    def get_by_key(self, key):
        return self.key_value[key]

    def get_by_value(self, value):
        return self.value_key[value]

    def set(self, key, value):
        self.key_value[key] = value
        self.value_key[value] = key

    def keys(self):
        return self.key_value.keys()

    def values(self):
        return self.key_value.values()
