from abc import ABC, abstractmethod
import uuid

class Item(ABC):
    def __init__(self, weight: float, count: int, containerID: uuid.UUID):
        self.id = uuid.uuid4()
        self.weight = weight
        self.count = count
        self.containerID = containerID

    @abstractmethod
    def get_total_weight(self):
        pass

class ItemFactory(ABC):
    @abstractmethod
    def create_item(self, weight: float, count: int, containerID: uuid.UUID) -> Item:
        pass

class BasicItem(Item):
    def get_total_weight(self):
        return self.weight * 1.5

class HeavyItem(Item):
    def get_total_weight(self):
        return self.weight * 3.0

class RefrigeratedItem(Item):
    def get_total_weight(self):
        return self.weight * 4.0

class LiquidItem(Item):
    def get_total_weight(self):
        return self.weight * 5.0

class BasicItemFactory(ItemFactory):
    def create_item(self, weight: float, count: int, containerID: uuid.UUID) -> Item:
        return BasicItem(weight, count, containerID)

class HeavyItemFactory(ItemFactory):
    def create_item(self, weight: float, count: int, containerID: uuid.UUID) -> Item:
        return HeavyItem(weight, count, containerID)

class RefrigeratedItemFactory(ItemFactory):
    def create_item(self, weight: float, count: int, containerID: uuid.UUID) -> Item:
        return RefrigeratedItem(weight, count, containerID)

class LiquidItemFactory(ItemFactory):
    def create_item(self, weight: float, count: int, containerID: uuid.UUID) -> Item:
        return LiquidItem(weight, count, containerID)

