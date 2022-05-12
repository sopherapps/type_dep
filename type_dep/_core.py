"""The module containing the core functionality of the package"""
from abc import abstractmethod
from inspect import signature
from typing import Callable, Any, Type

_dependencies = {}
_is_initialized = False


def dependencyinjected(func: Callable[..., Any]):
    """
    decorator to make any function's or method's type annotated arguments injectable
    """
    parameters = list(signature(func).parameters.items())
    param_length = len(parameters)
    param_annotation_map = {name: __get_class_fullname(param.annotation) for name, param in parameters}
    cached_kwargs = {name: None if param.default is param.empty else param.default for name, param in parameters}

    def new_func(*args, **kw):
        kwargs = {}
        index = 0
        arg_length = len(args)

        # register the dependencies at runtime if not yet registered
        if not _is_initialized:
            for subclass in Dependency.__subclasses__():
                _dependencies[__get_class_fullname(subclass)] = subclass.instantiate

        # add arguments data in the right order
        while index < arg_length:
            _, param = parameters[index]
            kwargs[param.name] = args[index]
            index += 1

        # add the remaining parameters
        while index < param_length:
            p, _ = parameters[index]
            kwargs[p] = kw.get(p, cached_kwargs.get(p, None))

            if kwargs[p] is None:
                annotation_cls_name = param_annotation_map[p]
                dep = _dependencies.get(annotation_cls_name, None)
                if dep is not None:
                    kwargs[p] = cached_kwargs[p] = dep()

            index += 1

        return func(**kwargs)

    return new_func


class Dependency:
    """The base class for all dependencies that can be injected. Ensure instantiate() is implemented"""
    @classmethod
    @abstractmethod
    def instantiate(cls) -> Any:
        raise NotImplementedError("instantiate() is required to return an instance of the class")


def __get_class_fullname(cls: Type[Any]) -> str:
    """returns the full name of the class"""
    if cls.__module__ is None:
        return cls.__name__

    return f"{cls.__module__}.{cls.__name__}"
