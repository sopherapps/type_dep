"""Tests for the core functionality of the package"""
import unittest
from typing import Dict, Any

from type_dep import dependencyinjected, Dependency


class A(Dependency):
    def __init__(self, name: str):
        self.name = name

    @classmethod
    def instantiate(cls):
        return A("Foo bar")


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

        expected = {
            "males": 9,
            "females": 8,
            "a.name": "Foo bar",
            "greeting": "kul",
            "b.name": "Foo bar",
        }
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

        expected = {"name": "Foo bar", "sex": "male"}
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
