from abc import ABC, abstractmethod
from uuid import uuid4
from item import BasicItem,HeavyItem,RefrigeratedItem,LiquidItem

class Container(ABC):
    def __init__(self, weight: float) -> None:
        self.id = uuid4()
        self.weight = weight
        self.items = []

    @abstractmethod
    def consumption(self) -> float:
        pass

    @abstractmethod
    def can_load_item(self, item):
        pass

    def load_items(self, items):
        for item in items:
            if self.can_load_item(item):
                self.items.append(item)

    def unload_items(self):
        unloaded_items = self.items[:]
        self.items = []
        return unloaded_items


    def __eq__(self, other) -> bool:
        id_check = self.id == other.id
        weight_check = self.weight == other.weight
        type_check = self.__class__ == other.__class__
        if id_check and weight_check and type_check:
            return True
        else:
            return False

class BasicContainer(Container):
    def __init__(self, weight: float) -> None:
        super().__init__(weight=weight)

    def can_load_item(self, item):
        return isinstance(item, BasicItem)

    def consumption(self) -> float:
        return self.weight * 2.5

class HeavyContainer(Container):
    def __init__(self, weight: float) -> None:
        super().__init__(weight=weight)

    def can_load_item(self, item):
        return isinstance(item, HeavyItem)

    def consumption(self) -> float:
        return self.weight * 3.0

class RefrigeratedContainer(HeavyContainer):
    def __init__(self, weight: float) -> None:
        super().__init__(weight=weight)


    def can_load_item(self, item):
        return isinstance(item, RefrigeratedItem)

    def consumption(self) -> float:
        return self.weight * 5.0

class LiquidContainer(HeavyContainer):
    def __init__(self, weight: float) -> None:
        super().__init__(weight=weight)

    def can_load_item(self, item):
        return isinstance(item, LiquidItem)

    def consumption(self) -> float:
        return self.weight * 4.0
