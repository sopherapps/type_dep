# type_dep

type_dep is a dependency injection framework that uses type hints to inject dependencies (much like Angular, Dotnet and the like)

## Quick Start

- Install the package

```shell
pip install type_dep
```

- Inherit from the package's `Dependency` class to create an injectable dependency class.
- Use the `dependencyinjected` decorator to tag functions or methods that require dependency injection through their parameter type annotations.

```python
import os
from type_dep import Dependency, dependencyinjected, Context

counter = 0

class A(Dependency):
    def __init__(self, name: str):
        self.name = name

    @classmethod
    def instantiate(cls):
        global counter
        counter += 1
        return A(f"{counter}")

class B(Dependency):

    def __init__(self, sex: str):
        self.sex = sex

    @classmethod
    def instantiate(cls):
        return B(os.environ.get("SEX", "female"))

    @dependencyinjected
    def get_detail(self, a: A):
        """
        A method which uses dependency injection
        `a` will be instantiated and injected into this method at runtime.
        By default, these dependencies are stored in a global context.
        Subsequent method calls will use the instances of the dependencies that were
        instantiated on the first run.

        NOTE: The type hints on the parameters are a must
        """
        return {"name": a.name, "sex": self.sex}

    @dependencyinjected
    def scoped_get_detail(self, a: A, context: Context):
        """
        When a `Context` argument is passed,
        the dependencies are stored in a context that gets destroyed after every method call, unless
        an externally instantiated `Context` is passed to this function. For the later
        case, the `Context` object will be destroyed when it gets out of scope, as in normal python.

        NOTE: The type hints on the parameters are a must
        """
        return {"name": a.name, "sex": self.sex}

@dependencyinjected
def run(males: int, females: int, a: A, greeting: str, b: B):
    """
    Just some function that is dependency injected.
    `a` and `b` will be instantiated and injected into the function at runtime

    By default, these dependencies are stored in a global context.
    Subsequent method calls will use the instances of the dependencies that were
    instantiated on the first run.

    NOTE: The type hints on the parameters are a must
    """
    print(f"males: {males}, females: {females}, greeting: {greeting}, a.name: {a.name}, b.sex: {b.sex}")
    print(f'{b.get_detail()}\n')

@dependencyinjected
def scoped_run(males: int, females: int, a: A, greeting: str, b: B, context: Context):
    """
    Just some function that is dependency injected.
    `a` and `b` will be instantiated and injected into the function at runtime

    When a `Context` argument is passed,
    the dependencies are stored in a context that gets destroyed after every function call, unless
    an externally instantiated `Context` is passed to this function. For the later
    case, the `Context` object will be destroyed when it gets out of scope, as in normal python.

    NOTE: The type hints on the parameters are a must
    """
    print(f"scoped: males: {males}, females: {females}, greeting: {greeting}, a.name: {a.name}, b.sex: {b.sex}")
    print(f'scoped: {b.scoped_get_detail()}\n')

if __name__ == '__main__':
    counter = 0

    for _ in range(3):
        run(6, 56, greeting="hey")

    # males: 6, females: 56, greeting: hey, a.name: 1, b.sex: female
    # {'name': '2', 'sex': 'female'}
    # 
    # males: 6, females: 56, greeting: hey, a.name: 1, b.sex: female
    # {'name': '2', 'sex': 'female'}
    # 
    # males: 6, females: 56, greeting: hey, a.name: 1, b.sex: female
    # {'name': '2', 'sex': 'female'}

    for _ in range(3):
        scoped_run(6, 56, greeting="hey")

    # scoped: males: 6, females: 56, greeting: hey, a.name: 3, b.sex: female
    # scoped: {'name': '4', 'sex': 'female'}
    # 
    # scoped: males: 6, females: 56, greeting: hey, a.name: 5, b.sex: female
    # scoped: {'name': '6', 'sex': 'female'}
    # 
    # scoped: males: 6, females: 56, greeting: hey, a.name: 7, b.sex: female
    # scoped: {'name': '8', 'sex': 'female'}
```

## Why use type hints

Python type hints have matured alot. It is high time we used them to the maximum. 
Apart from helping us avoid some logical errors, wouldn't be nice if type hints helped inject dependencies.

- Very little extra code is needed if you are already using types
- It is intuitive

## How to test

- Clone the repository

```shell
git clone git@github.com:sopherapps/type_dep.git
cd type_dep
```

- Create and activate the virtual environment

```shell
python3 -m venv env
source env/bin/activate
```

- Run the test command

```shell
python -m unittest
```

## License

Copyright (c) 2022 [Martin Ahindura](https://github.com/Tinitto) Licensed under the [MIT License](./LICENSE)
