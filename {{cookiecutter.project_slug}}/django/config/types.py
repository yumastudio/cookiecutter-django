from graphene.types.json import JSONString


class CustomJSON(JSONString):
    @staticmethod
    def serialize(json):
        return json
