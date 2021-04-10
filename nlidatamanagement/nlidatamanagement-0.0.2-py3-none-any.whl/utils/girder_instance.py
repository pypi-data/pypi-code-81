import attr


@attr.s(kw_only=True, eq=False)
class GirderInstance:
    """Girder server instance."""
    name = attr.ib(validator=attr.validators.instance_of(str))
    host = attr.ib(validator=attr.validators.instance_of(str))
    api_key = attr.ib(validator=attr.validators.instance_of(str))

    def to_json(self):
        json_dict = {'name': self.name, 'host': self.host, 'api_key': self.api_key}
        return json_dict

    def __eq__(self, obj):
        return isinstance(obj, GirderInstance) and self.name == obj.name
