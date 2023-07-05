"""Tests for the core functionality of the package"""
import unittest
from typing import Dict, Any

from type_dep import dependencyinjected, Dependency
from type_dep import Context

counter = 0


class A(Dependency):
    def __init__(self, name: str):
        self.name = name

    @classmethod
    def instantiate(cls):
        global counter
        counter += 1
        return A(f"{counter}")


class TypeDep(unittest.TestCase):
    """Tests for the core functionality of the type_dep package"""

    def test_dependencyinjected_on_functions(self):
        """dependencyinjected decorator instantiates the required dependencies accordingly for functions"""

        @dependencyinjected
        def run(males: int, females: int, a: A, greeting: str, b: A) -> Dict[str, Any]:
            """Just some function that is dependency injected"""
            return {
                "males": males,
                "females": females,
                "a.name": a.name,
                "greeting": greeting,
                "b.name": b.name,
            }

        global counter
        counter = 0

        next_int = 1

        for _ in range(3):
            # it runs the instantiate only once
            expected = {
                "males": 9,
                "females": 8,
                "a.name": f"{next_int}",
                "greeting": "kul",
                "b.name": f"{next_int + 1}",
            }

            got = run(9, 8, greeting="kul")
            self.assertDictEqual(expected, got)

    def test_scoped_dependencyinjected_on_functions(self):
        """dependencyinjected decorator instantiates the required dependencies accordingly for functions in a temp context if context is an arg"""

        @dependencyinjected
        def run(males: int, females: int, a: A, greeting: str, b: A, ctxt: Context) -> Dict[str, Any]:
            """Just some function that is dependency injected"""
            return {
                "males": males,
                "females": females,
                "a.name": a.name,
                "greeting": greeting,
                "b.name": b.name,
            }

        global counter
        counter = 0

        next_int = 0

        for _ in range(3):
            # it will run the instantiate every time
            next_int += 1

            expected = {
                "males": 9,
                "females": 8,
                "a.name": f"{next_int}",
                "greeting": "kul",
                "b.name": f"{next_int + 1}",
            }

            next_int += 1

            got = run(9, 8, greeting="kul")
            self.assertDictEqual(expected, got)

    def test_dependencyinjected_on_methods(self):
        """dependencyinjected decorator instantiates the required dependencies accordingly for methods"""
        class B(Dependency):
            def __init__(self, sex: str):
                self.sex = sex

            @classmethod
            def instantiate(cls):
                return B("female")

            @dependencyinjected
            def get_detail(self, a: A):
                return {"name": a.name, "sex": self.sex}

        global counter
        counter = 0

        expected = {"name": "1", "sex": "male"}
        got = B("male").get_detail()

        self.assertDictEqual(expected, got)

        next_int = 1

        for _ in range(3):
            # it will run the instantiate once in the global context
            expected = {"name": f"{next_int}", "sex": "male"}
            got = B("male").get_detail()

            self.assertDictEqual(expected, got)

    def test_scoped_dependencyinjected_on_methods(self):
        """dependencyinjected decorator instantiates the required dependencies accordingly for methods in a temp context if context is an arg"""
        class B(Dependency):
            def __init__(self, sex: str):
                self.sex = sex

            @classmethod
            def instantiate(cls):
                return B("female")

            @dependencyinjected
            def get_detail(self, a: A, ctxt: Context):
                return {"name": a.name, "sex": self.sex}

        global counter
        counter = 0

        next_int = 0

        for _ in range(3):
            # it will run the instantiate every time
            next_int += 1

            expected = {"name": f"{next_int}", "sex": "male"}
            got = B("male").get_detail()

            self.assertDictEqual(expected, got)

    def test_instantiate_is_required(self):
        """instantiate() should be implemented"""
        class C(Dependency):
            pass

        @dependencyinjected
        def run(y: C):
            pass

        self.assertRaises(NotImplementedError, run)


if __name__ == '__main__':
    unittest.main()
