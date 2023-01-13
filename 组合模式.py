from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Component(ABC):

    @property
    def parent(self) -> Component:
        return self._parent

    @parent.setter
    def parent(self, parent: Component):
        self._parent = parent

    def add(self, other: Component):
        pass

    def remove(self):
        pass

    def is_composite(self) -> bool:
        return False

    @abstractmethod
    def operator(self) -> str:
        pass


class Leaf(Component):

    def operator(self) -> str:
        return f'Leaf{id(self)}'


class Composite(Component):

    def __init__(self):
        self._children: List[Component] = []

    def add(self, other):
        self._children.append(other)

    def remove(self, other: Component) -> None:
        self._children.remove(other)
        other.parent = None

    def is_composite(self) -> bool:
        return True

    def operator(self) -> str:
        results = []
        for child in self._children:
            results.append(child.operator())
        return f"Branch({'+'.join(results)})"


def client_code(component: Component) -> None:
    """
    The client code works with all of the components via the base interface.
    """

    print(f"RESULT: {component.operator()}", end="")


def client_code2(component1: Component, component2: Component) -> None:
    """
    Thanks to the fact that the child-management operations are declared in the
    base Component class, the client code can work with any component, simple or
    complex, without depending on their concrete classes.
    """

    if component1.is_composite():
        component1.add(component2)

    print(f"RESULT: {component1.operator()}", end="")


if __name__ == "__main__":
    # This way the client code can support the simple leaf components...
    simple = Leaf()
    print("Client: I've got a simple component:")
    client_code(simple)
    print("\n")

    # ...as well as the complex composites.
    tree = Composite()

    branch1 = Composite()
    branch1.add(Leaf())
    branch1.add(Leaf())

    branch2 = Composite()
    branch2.add(Leaf())

    tree.add(branch1)
    tree.add(branch2)

    print("Client: Now I've got a composite tree:")
    client_code(tree)
    print("\n")

    print("Client: I don't need to check the components classes even when managing the tree:")
    client_code2(tree, simple)
