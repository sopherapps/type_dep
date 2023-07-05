"""The module containing the core functionality of the package"""
from abc import abstractmethod
from inspect import signature, Parameter
from typing import Callable, Any, Type, Optional, Union, List, Tuple, Dict

_global_context: Optional["Context"] = None


def dependencyinjected(func: Callable[..., Any]):
    """
    decorator to make any function's or method's type annotated arguments injectable
    """
    parameters = list(signature(func).parameters.items())
    param_annotation_map = {name: _get_name(param.annotation) for name, param in parameters}
    cached_kwargs = {name: param.default for name, param in parameters if param.default is not param.empty}
    context_arg_name = _get_context_arg_name(parameters)
    func_name = _get_name(func)

    def new_func(*args, **kw):
        # move args to kwargs
        kwargs = {parameters[index][1].name: arg for index, arg in enumerate(args)}

        # initialize context
        context = _get_context(context_arg_name, {**cached_kwargs, **kw, **kwargs})
        context.register_dependencies()
        context.set_cached_kwargs_if_empty(func_name, new_kwargs=cached_kwargs)

        # add the rest of the kwargs. Initialize any dependency that needs initialization.
        for p, _ in parameters[len(args): len(parameters)]:
            if p == context_arg_name:
                kwargs[p] = context
            else:
                kwargs[p] = kw.get(p, context.get_cached_kwarg(func_name, p))

                if kwargs[p] is None:
                    kwargs[p] = _initialize_dependency(context, param_annotation_map[p])
                    context.set_cached_kwarg(func_name, p, kwargs[p])

        # return new function, passing in the kwargs
        return func(**kwargs)

    return new_func


class Context(dict):
    """A context class to pass to a function"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_kwargs = {}

    def register_dependencies(self):
        """Registers dependencies"""
        for subclass in Dependency.__subclasses__():
            self[_get_name(subclass)] = subclass.instantiate

    def set_cached_kwargs_if_empty(self, func_name: str, new_kwargs: Dict[str, Any]):
        """Sets the cached kwargs for given function if none are available"""
        if func_name not in self._cached_kwargs:
            self._cached_kwargs[func_name] = {**new_kwargs}

    def get_cached_kwarg(self, func_name: str, key: str) -> Optional[Any]:
        """Gets the cached kwarg for a given function"""
        return self._cached_kwargs[func_name].get(key, None)

    def set_cached_kwarg(self, func_name: str, key: str, value: Any):
        """Sets the cached kwarg for a given function"""
        self._cached_kwargs[func_name][key] = value


class Dependency:
    """The base class for all dependencies that can be injected. Ensure instantiate() is implemented"""
    @classmethod
    @abstractmethod
    def instantiate(cls) -> Any:
        raise NotImplementedError("instantiate() is required to return an instance of the class")


def _get_name(cls: Union[Type[Any], Callable]) -> str:
    """returns the full name of the class or callable"""
    if cls.__module__ is None:
        return cls.__name__

    return f"{cls.__module__}.{cls.__name__}"


def _get_context_arg_name(parameters: List[Tuple[str, Parameter]]) -> Optional[str]:
    """Returns the name of the argument that is a Context"""
    arg_name = None
    for name, param in parameters:
        if param.annotation == Context:
            arg_name = name

    return arg_name


def _get_context(context_arg_name: Optional[str], kwargs: Dict[str, Any]) -> "Context":
    """Gets the context given the context arg name and kwargs"""
    if context_arg_name is None:
        global _global_context

        # initialize global context if not yet initialized
        if _global_context is None:
            _global_context = Context()

        return _global_context
    else:
        # if no context arg is passed, a new one is created
        return kwargs.get(context_arg_name, Context())


def _initialize_dependency(context: "Context", dep_cls: Type[Dependency]) -> Optional[Dependency]:
    """Initializes the given dependency on the given context"""
    dep_initializer = context.get(dep_cls, None)
    if dep_initializer is not None:
        return dep_initializer()
