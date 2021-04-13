from pydantic.error_wrappers import ErrorWrapper, ValidationError


class DBValidator:
    __validations__ = []

    def __init__(self, pydantic_model, engine_connection):
        self.engine_connection = engine_connection
        __errors__ = []
        __pydantic_model__ = pydantic_model
        __values__ = pydantic_model.__dict__
        for name, validator in self.__validations__:
            if validator.root and validator.each_item:
                raise SyntaxError("Can't have root and each_item")
            if validator.each_item:
                if type(__values__[name]) is list:
                    for i, item in enumerate(__values__[name]):
                        try:
                            __values__[name][i] = validator.fn(self, item, __values__)
                        except Exception as e:
                            __errors__.append(ErrorWrapper(e, (name, item)))
                elif type(__values__[name]) is dict:
                    for item in __values__[name]:
                        try:
                            __values__[name][item] = validator.fn(self, __values__[name][item], __values__)
                        except Exception as e:
                            __errors__.append(ErrorWrapper(e, (name, item)))
                else:
                    raise SyntaxError("each_item only valid on dict or list")
            else:
                if validator.root:
                    try:
                        __values__ = validator.fn(self, __values__)
                    except Exception as e:
                        __errors__.append(ErrorWrapper(e, ('root',)))
                else:
                    try:
                        __values__[name] = validator.fn(self, __values__[name], __values__)
                    except Exception as e:
                        __errors__.append(ErrorWrapper(e, (name,)))
        if len(__errors__) > 0:
            raise ValidationError(__errors__, __pydantic_model__.__class__)


def check_field(*fields, each_item=False, root=False):
    class CheckField:
        def __init__(self, fn):
            self.fields = fields
            self.each_item = each_item
            self.root = root
            self.fn = fn

        def __set_name__(self, owner, name):
            self.fn.class_name = owner.__name__
            for field in fields:
                owner.__validations__.append((field, self))

        def __call__(self, *args, **kwargs):
            return self.fn(*args, **kwargs)

    return CheckField
