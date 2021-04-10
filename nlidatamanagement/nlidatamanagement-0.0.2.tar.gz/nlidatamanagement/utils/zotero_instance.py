import attr


@attr.s(kw_only=True, eq=False)
class ZoteroInstance:
    """Zotero server instance."""
    name = attr.ib(validator=attr.validators.instance_of(str))
    api_key = attr.ib(validator=attr.validators.instance_of(str))
    library_id = attr.ib(validator=attr.validators.instance_of(str))
    library_type = attr.ib(validator=attr.validators.instance_of(str))

    def to_json(self):
        json_dict = {'name': self.name,
                     'api_key': self.api_key,
                     'library_id': self.library_id,
                     'library_type': self.library_type}
        return json_dict

    def __eq__(self, obj):
        return isinstance(obj, ZoteroInstance) and self.name == obj.name
