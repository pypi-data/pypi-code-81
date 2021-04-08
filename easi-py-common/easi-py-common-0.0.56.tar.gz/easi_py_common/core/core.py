import base64
from functools import wraps
from pydantic.generics import GenericModel
from typing import Optional, Callable, TypeVar, Any, Union, Iterable, Type, List, Generic, Tuple

from flask import request, jsonify, make_response, Response, current_app
from pydantic import ValidationError, Field
from typing import Type

from pydantic import BaseModel
from werkzeug.datastructures import ImmutableMultiDict

from easi_py_common.core.error import (
    InvalidIterableOfModelsException,
    ManyModelValidationError,
    JsonBodyParsingError,
)

try:
    from flask_restful import original_flask_make_response as make_response
except ImportError:
    pass

InputParams = TypeVar("InputParams")
DataT = TypeVar('DataT')


def decode_list_start_key(start_key):
    if not start_key:
        return None
    return base64.b64decode(start_key.encode('utf-8')).decode('ascii')


def encode_list_next_key(next_key):
    if not next_key:
        return None
    return base64.b64encode(next_key.encode('utf-8')).decode('ascii')


class ListQueryRequestDTO(BaseModel):
    limit: Optional[int] = Field(description='分页的每页条数', default=20, ge=1, le=100)
    start_key: Optional[str] = Field(description='用于分页，使用返回值的next_key')

    def decode_start_key(self):
        if not self.start_key:
            return None
        return decode_list_start_key(self.start_key)

    def decode_start_key_to_int(self):
        decode_start_key = self.decode_start_key()
        if not decode_start_key:
            return None
        try:
            return int(decode_start_key)
        except Exception:
            return None


class RespWap(GenericModel, Generic[DataT]):
    code: int = 0
    data: Optional[DataT] = {}

    @classmethod
    def __concrete_name__(cls: Type[Any], params: Tuple[Type[Any], ...]) -> str:
        return f'{params[0].__name__.title()}Response'


class RespWaps(GenericModel, Generic[DataT]):
    code: int = 0
    data: List[DataT]

    @classmethod
    def __concrete_name__(cls: Type[Any], params: Tuple[Type[Any], ...]) -> str:
        return f'{params[0].__name__.title()}Response'


class Ok(RespWap, Generic[DataT]):
    # data: Optional[DataT]
    def __init__(self, data: Any = None):
        super(Ok, self).__init__(data=data)


class Oks(RespWap, Generic[DataT]):
    data: List[DataT]

    def __init__(self, data: Any = None):
        super(Oks, self).__init__(data=data)


class OkNext(GenericModel, Generic[DataT]):
    code: int = 0
    data: List[DataT] = []
    next_key: Optional[str]

    def __init__(self, data: Any = None, next_key: str = None):
        super(OkNext, self).__init__(data=data)
        self.next_key = next_key

    @classmethod
    def __concrete_name__(cls: Type[Any], params: Tuple[Type[Any], ...]) -> str:
        return f'{params[0].__name__.title()}NextResponse'

    @staticmethod
    def build_not_data():
        return OkNext(
            data=[],
            next_key=None
        )

    @staticmethod
    def build_encode_next_key(data: List[DataT], next_key: str):
        return OkNext(
            data=data,
            next_key=encode_list_next_key(next_key)
        )

    @staticmethod
    def build_encode_next_key_int(data: List[DataT], next_key: int):
        return OkNext(
            data=data,
            next_key=encode_list_next_key(str(next_key))
        )


def make_json_response(
        content: Union[BaseModel, Iterable[BaseModel]],
        status_code: int,
        by_alias: bool,
        exclude_none: bool = False,
        many: bool = False,
) -> Response:
    """serializes model, creates JSON response with given status code"""
    if many:
        js = f"[{', '.join([model.json(exclude_none=exclude_none, by_alias=by_alias) for model in content])}]"
    else:
        js = content.json(exclude_none=exclude_none, by_alias=by_alias)
    response = make_response(js, status_code)
    response.mimetype = "application/json"
    return response


def unsupported_media_type_response(request_cont_type: str) -> Response:
    body = {
        "detail": f"Unsupported media type '{request_cont_type}' in request. "
                  "'application/json' is required."
    }
    return make_response(jsonify(body), 415)


def is_iterable_of_models(content: Any) -> bool:
    try:
        return all(isinstance(obj, BaseModel) for obj in content)
    except TypeError:
        return False


def validate_many_models(model: Type[BaseModel], content: Any) -> List[BaseModel]:
    try:
        return [model(**fields) for fields in content]
    except TypeError:
        # iteration through `content` fails
        err = [
            {
                "loc": ["root"],
                "msg": "is not an array of objects",
                "type": "type_error.array",
            }
        ]
        raise ManyModelValidationError(err)
    except ValidationError as ve:
        raise ManyModelValidationError(ve.errors())


def api_json(
        body: Optional[Type[BaseModel]] = None,
        query: Optional[Type[BaseModel]] = None,
        on_success_status: int = 200,
        exclude_none: bool = False,
        request_body_many: bool = False,
        response_by_alias: bool = False,
):
    """
    Decorator for route methods which will validate query and body parameters
    as well as serialize the response (if it derives from pydantic's BaseModel
    class).

    Request parameters are accessible via flask's `request` variable:
        - request.query_params
        - request.body_params

    Or directly as `kwargs`, if you define them in the decorated function.

    `exclude_none` whether to remove None fields from response
    `response_many` whether content of response consists of many objects
        (e. g. List[BaseModel]). Resulting response will be an array of serialized
        models.
    `request_body_many` whether response body contains array of given model
        (request.body_params then contains list of models i. e. List[BaseModel])

    example::

        from flask import request
        from flask_pydantic import validate
        from pydantic import BaseModel

        class Query(BaseModel):
            query: str

        class Body(BaseModel):
            color: str

        class MyModel(BaseModel):
            id: int
            color: str
            description: str

        ...

        @app.route("/")
        @validate(query=Query, body=Body)
        def test_route():
            query = request.query_params.query
            color = request.body_params.query

            return MyModel(...)

        @app.route("/kwargs")
        @validate()
        def test_route_kwargs(query:Query, body:Body):

            return MyModel(...)

    -> that will render JSON response with serialized MyModel instance
    """

    def decorate(func: Callable[[InputParams], Any]) -> Callable[[InputParams], Any]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            q, b, err = None, None, {}
            query_in_kwargs = func.__annotations__.get("query")
            query_model = query_in_kwargs or query
            if query_model:
                query_params = convert_query_params(request.args, query_model)
                try:
                    q = query_model(**query_params)
                except ValidationError as ve:
                    err["query_params"] = ve.errors()
            body_in_kwargs = func.__annotations__.get("body")
            body_model = body_in_kwargs or body
            if body_model:
                body_params = request.get_json()
                if request_body_many:
                    try:
                        b = validate_many_models(body_model, body_params)
                    except ManyModelValidationError as e:
                        err["body_params"] = e.errors()
                else:
                    try:
                        b = body_model(**body_params)
                    except TypeError:
                        content_type = request.headers.get("Content-Type", "").lower()
                        if content_type != "application/json":
                            return unsupported_media_type_response(content_type)
                        else:
                            raise JsonBodyParsingError()
                    except ValidationError as ve:
                        err["body_params"] = ve.errors()
            request.query_params = q
            request.body_params = b
            if query_in_kwargs:
                kwargs["query"] = q
            if body_in_kwargs:
                kwargs["body"] = b

            if err:
                status_code = current_app.config.get(
                    "FLASK_PYDANTIC_VALIDATION_ERROR_STATUS_CODE", 200
                )
                return make_response(jsonify({'code': 100, 'message': "validation error",
                                              "validation_error": err}), status_code)
            res = func(*args, **kwargs)

            if isinstance(res, list) or isinstance(res, tuple):
                if is_iterable_of_models(res):
                    return make_json_response(
                        res,
                        on_success_status,
                        by_alias=response_by_alias,
                        exclude_none=exclude_none,
                        many=True,
                    )
                else:
                    raise InvalidIterableOfModelsException(res)

            if isinstance(res, BaseModel):
                return make_json_response(
                    res,
                    on_success_status,
                    exclude_none=exclude_none,
                    by_alias=response_by_alias,
                )

            if (
                    isinstance(res, tuple)
                    and len(res) == 2
                    and isinstance(res[0], BaseModel)
            ):
                return make_json_response(
                    res[0],
                    res[1],
                    exclude_none=exclude_none,
                    by_alias=response_by_alias,
                )

            return res

        return wrapper

    return decorate


def convert_query_params(
        query_params: ImmutableMultiDict, model: Type[BaseModel]
) -> dict:
    """
    group query parameters into lists if model defines them

    :param query_params: flasks request.args
    :param model: query parameter's model
    :return: resulting parameters
    """
    return {
        **query_params,
        **{
            key: value
            for key, value in query_params.to_dict(flat=False).items()
            if key in model.__fields__ and model.__fields__[key].is_complex()
        },
    }
