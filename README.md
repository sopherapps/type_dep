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
from type_dep import Dependency, dependencyinjected

class A(Dependency):
    def __init__(self, name: str):
        self.name = name
        
    @classmethod
    def instantiate(cls):
        return A(os.environ.get("NAME", "Foo bar"))

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
        NOTE: The type hints on the parameters are a must
        """
        return {"name": a.name, "sex": self.sex}

@dependencyinjected
def run(males: int, females: int, a: A, greeting: str, b: B):
    """
    Just some function that is dependency injected. 
    `a` and `b` will be instantiated and injected into the function at runtime
    NOTE: The type hints on the parameters are a must
    """
    print(f"males: {males}, females: {females}, greeting: {greeting}, a.name: {a.name}, b.sex: {b.sex}\n")
    print(b.get_detail())

if __name__ == '__main__':
    run(6, 56, greeting="hey")
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
