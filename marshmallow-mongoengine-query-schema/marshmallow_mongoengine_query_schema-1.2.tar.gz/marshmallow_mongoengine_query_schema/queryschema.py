import re
import json
from marshmallow import ValidationError, post_load, validate
from marshmallow.fields import Field
from marshmallow.schema import Schema, SchemaOpts
from mongoengine.queryset.transform import MATCH_OPERATORS
from marshmallow import fields
from webargs import fields as webargs_fields


class QuerySchemaOpts(SchemaOpts):
    def __init__(self, meta, ordered: bool):
        super().__init__(meta, ordered=ordered)
        
        self.query_enable_filters: bool = getattr(meta, 'query_enable_filters', True)
        self.query_enable_only: bool = getattr(meta, 'query_enable_only', True)
        self.query_enable_order_by: bool = getattr(meta, 'query_enable_order_by', True)
        self.query_allowed_infixes: list[str] = getattr(meta, 'query_allowed_infixes', ['__', '_', '-', '.'])


class QuerySchema(Schema):
    """
    Schema for use in url query which checks for possible mongoengine query filters (as well as `only` and `order_by` args)
    and converts their types based on requirements for filters (eg. ints for number comparition operators)
    and fields themselves (eg. list inner type when using for example `list__0`)
    
    Supports all mongoengine filters except `Geo queries`
    For more info checkout: https://docs.mongoengine.org/guide/querying.html
    
    Example:
    >>> class SomeQuerySchema(QuerySchema):
            __query_fields__ = SomeSchema().declared_fields
            class Meta:  # optional settings
                query_enable_filters = False
                query_enable_only = True
                query_enable_order_by = False
                query_allowed_infixes = ['__']
    
    Usage in url:
    example.com/someendpoint?no_comments=5&name__startswith=b&list__size=2&list__0=somestring
    
    Every type is converted automatically but there's couple of things to point out:
        When list type is needed, comma delimited list is used in url: `?list=a,b,c,d`

        `match` operator and `__raw__` are expecting a dictionary(json): `?__raw__={"name": "hello"}`
    """
    OPTIONS_CLASS = QuerySchemaOpts
    
    @property
    def __query_fields__() -> dict[str, Field]:
        """
        Fields for which to generate mongoengine filters.
        
        Example:
        >>> class SomeQuerySchema(QuerySchema):
                __query_fields__ = SomeSchema().declared_fields
        """
        raise NotImplementedError
        
    @staticmethod
    def parse_dict(v):
        try:
            data = json.loads(v)
        except json.JSONDecodeError:
            raise ValidationError(message='Not a valid json or dict.')
        if isinstance(data, dict):
            return data
        else:
            raise ValidationError(message='Not a valid json or dict.')
    
    @post_load(pass_many=True)
    def parse_unknown_fields(self, data, **kwargs):
        for k, v in data.copy().items():
            if k == 'only' and self.opts.query_enable_only:
                data[k] = webargs_fields.DelimitedList(
                    fields.String(),
                    validate=(
                        validate.ContainsOnly(choices=self.__query_fields__),
                        validate.Length(min=1),
                    )
                ).deserialize(v)
                continue
            elif k == 'order_by' and self.opts.query_enable_order_by:
                choices = list(self.__query_fields__.keys())
                for field in self.__query_fields__:
                    choices.append(f'+{field}')
                    choices.append(f'-{field}')
                
                data[k] = webargs_fields.DelimitedList(
                    fields.String(),
                    validate=(
                        validate.ContainsOnly(choices=choices),
                        validate.Length(min=1),
                    )
                ).deserialize(v)
                continue
            
            if not self.opts.query_enable_filters:
                continue
            
            try:
                if k == "__raw__":
                    data[k] = self.parse_dict(v)
                    continue
                
                pattern = r"[^\W_]+(?P<infix>{})?(?:[^\W_]+(?P=infix))*[^\W_]+".format(
                    r'|'.join(map(re.escape, self.opts.query_allowed_infixes)))
                
                match = re.match(pattern, k)
                
                if match is None:
                    raise ValidationError(message=self.error_messages["unknown"])
                
                infix = match.group('infix')
                
                parts = [part for part in k.split(infix) if not part.isnumeric()]

                try:
                    field = self.__query_fields__[parts[0]]
                except KeyError:
                    raise ValidationError(message=self.error_messages["unknown"])

                operator = ''
                for part in parts:
                    if part == 'not' or part in MATCH_OPERATORS:
                        operator += part
                    elif isinstance(field, fields.List):
                        field = field.inner
                    elif isinstance(field, fields.Nested):
                        field = field.schema
                    elif isinstance(field, Schema):
                        field = field._declared_fields[part]
                
                if not operator:
                    if isinstance(field, fields.List):
                        data[k] = webargs_fields.DelimitedList(
                            field.inner).deserialize(v)
                    elif isinstance(field, fields.String):
                        v = field.deserialize(v)
                        if re.match(r'/.*/', v) is not None:
                            v = re.compile(r'{}'.format(v.removeprefix('/').removesuffix('/')))
                        data[k] = v
                    else:
                        data[k] = field.deserialize(v)
                elif operator in ("ne", "lt", "lte", "gt", "gte", "size"):
                    data[k] = fields.Number().deserialize(v)
                elif operator in (
                    "exact",
                    "iexact",
                    "contains",
                    "icontains",
                    "startswith",
                    "istartswith",
                    "endswith",
                    "iendswith",
                ):
                    data[k] = fields.String().deserialize(v)
                elif operator == "mod":
                    data[k] = webargs_fields.DelimitedList(
                        fields.Number, validate=(validate.Length(equal=2))
                    ).deserialize(v)
                elif operator in ("in", "nin", "all"):
                    data[k] = webargs_fields.DelimitedList(field).deserialize(v)
                elif operator == "slice":
                    data[k] = webargs_fields.DelimitedList(
                        fields.Number).deserialize(v)
                elif operator == "exists":
                    data[k] = fields.Bool().deserialize(v)
                elif operator == "match":
                    data[k] = self.parse_dict(v)
                else:
                    raise ValidationError(message=self.error_messages["unknown"])
                
                new_k = '__'.join(k.split(infix))
                v = data.pop(k)
                data[new_k] = v
                
            except ValidationError as e:
                raise ValidationError(field_name=k, message=e.messages)

        return data
