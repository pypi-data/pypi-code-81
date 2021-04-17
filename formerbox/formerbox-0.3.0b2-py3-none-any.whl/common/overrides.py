import dis
import inspect
from abc import ABCMeta
from inspect import FrameInfo
from typing import Any, Callable, Dict, List, Tuple, Type, TypeVar

FuncType = TypeVar("FuncType", bound=Callable)


class EnforceOverridesMeta(ABCMeta):
    OVERRIDE_ERROR = "Method `%s` overrides but does not have `@override` decorator"
    FINALIZED_ERROR = "Method `%s` is finalized in `%s`, it cannot be overridden"

    def __new__(
        cls,
        name: str,
        bases: Tuple[type, ...],
        namespace: Dict[str, Any],
        **kwargs: Any
    ) -> type:
        obj = super().__new__(cls, name, bases, namespace, **kwargs)

        for item_name, item_value in namespace.items():
            # Actually checking the direct parent should be enough,
            # otherwise the error would have emerged during the parent class checking
            if item_name.startswith("__"):
                continue

            value = cls.handle_special_value(item_value)
            is_override = getattr(value, "__override__", False)
            for base in bases:
                base_class_method = getattr(base, item_name, False)
                if not base_class_method or not callable(base_class_method):
                    continue

                # `__finalized__` is added by `@final` decorator
                is_finalized = getattr(base_class_method, "__finalized__", False)

                # check if `@override` decorator added
                assert is_override, cls.OVERRIDE_ERROR % item_name
                # check if current method is not finalized
                assert not is_finalized, cls.FINALIZED_ERROR % (base_class_method, base)

        return obj

    @staticmethod
    def handle_special_value(value: Any) -> Any:
        if isinstance(value, (classmethod, staticmethod)):
            value = value.__get__(None, dict)
        elif isinstance(value, property):
            value = value.fget
        return value


# pylint: disable=too-few-public-methods
class EnforceOverrides(metaclass=EnforceOverridesMeta):
    """Use this as the parent class for your custom classes"""


def override(func: FuncType) -> FuncType:
    """Decorator to indicate that the decorated method overrides a method in
    superclass.
    The decorator code is executed while loading class. Using this method
    should have minimal runtime performance implications.

    This is based on my idea about how to do this and fwc:s highly improved
    algorithm for the implementation fwc:s
    algorithm : http://stackoverflow.com/a/14631397/308189
    my answer : http://stackoverflow.com/a/8313042/308189

    How to use:
    ```
    from overrides import override

    class SuperClass(object):
        def method(self):
          return 2

    class SubClass(SuperClass):
        @override
        def method(self):
            return 1
    ```

    :raises  `AssertionError` if no match in super classes for the method name
    :return  original method with possibly added (if the method doesn't have one)
        docstring from super class
    """
    setattr(func, "__override__", True)

    func_stack = inspect.stack(context=2)
    func_frame = func_stack[2]
    func_namespace = func.__globals__

    for super_class in _get_base_classes(func_frame, func_namespace):
        if hasattr(super_class, func.__name__):
            super_method = getattr(super_class, func.__name__)
            if hasattr(super_method, "__finalized__"):
                finalized = getattr(super_method, "__finalized__")
                if finalized:
                    raise AssertionError('Method "%s" is finalized' % func.__name__)
            if not func.__doc__:
                func.__doc__ = super_method.__doc__
            return func

    raise AssertionError('No super class method found for "%s"' % func.__name__)


def final(func: FuncType) -> FuncType:
    """Decorator to indicate that the decorated method is finalized and cannot be overridden.
    The decorator code is executed while loading class. Using this method
    should have minimal runtime performance implications.
    Currently, only methods with `@override` are checked.

    How to use:
    ```
    from overrides import final

    class SuperClass(object):
        @final
        def method(self):
          return 2

    class SubClass(SuperClass):
        @overrides
        def method(self): #causes an error
            return 1
    ```

    :raises  `AssertionError` if there exists a match in sub classes for the method name
    :return  original method
    """
    setattr(func, "__finalized__", True)
    return func


def _get_base_classes(
    frame_info: FrameInfo, namespace: Dict[str, Any]
) -> List[Type[Any]]:
    base_classes: List[Type] = []
    for class_name_components in _get_base_class_names(frame_info):
        base_class = _get_base_class(class_name_components, namespace)
        base_classes.append(base_class)
    return base_classes  # type: ignore


def _get_base_class(components: List[str], namespace: Dict[str, Any]) -> Type[Any]:
    try:
        obj = namespace[components[0]]
    except KeyError:
        builtins = namespace["__builtins__"]
        if isinstance(builtins, dict):
            obj = builtins[components[0]]
        else:
            obj = getattr(builtins, components[0])

    for component in components[1:]:
        if hasattr(obj, component):
            obj = getattr(obj, component)

    return obj


# pylint: disable=too-many-branches
def _get_base_class_names(frame_info: FrameInfo) -> List[List[str]]:
    frame = frame_info.frame
    frame_args: List[Tuple[str, str]] = []

    # retrieve top arg values for names & attrs
    # basically, these values are base class names
    add_last_step = False
    for instr in dis.Bytecode(frame.f_code):
        if instr.opcode not in dis.hasname:
            continue
        if instr.opcode == dis.EXTENDED_ARG:
            continue
        if instr.offset > frame.f_lasti:
            continue

        if not add_last_step:
            frame_args = []
        if instr.opname == "LOAD_NAME":
            frame_args.append(("name", instr.argval))
            add_last_step = True
        elif instr.opname == "LOAD_ATTR":
            frame_args.append(("attr", instr.argval))
            add_last_step = True
        elif instr.opname == "LOAD_GLOBAL":
            frame_args.append(("name", instr.argval))
            add_last_step = True
        else:
            add_last_step = False

    # map retrieved values into components
    # for further dynamic type resolving
    items: List[List[str]] = []
    items_prev: List[str] = []
    for argname, argval in frame_args:
        if argname == "name":
            if items_prev:
                items.append(items_prev)
            items_prev = [argval]
        else:
            items_prev += [argval]

    if items_prev:
        items.append(items_prev)

    return items
