from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

from item import Item


@dataclass(kw_only=True)
class Container(ABC):
    container_id: int
    weight: int
    type: str
    items_ids: List[int]

    @abstractmethod
    def consumption(self) -> float:
        pass

    def to_dict(self) -> dict:
        container_info = {
            "container_id": self.container_id,
            "weight": self.weight,
            "type": self.type
        }
        if self.items_ids:
            container_info['items'] = [item.to_dict() for item in self.items_ids]
        return container_info

    def __eq__(self, other) -> bool:
        id_check = self.container_id == other.id
        weight_check = self.weight == other.weight
        type_check = self.__class__ == other.__class__
        if id_check and weight_check and type_check:
            return True
        else:
            return False

    def add_item(self, item: Item):
        self.items_ids.append(item.item_id)


@dataclass(kw_only=True)
class BasicContainer(Container):
    def consumption(self) -> float:
        return self.weight * 2.5


@dataclass(kw_only=True)
class HeavyContainer(Container):
    def consumption(self) -> float:
        return self.weight * 3.0


@dataclass(kw_only=True)
class RefrigeratedContainer(Container):
    def consumption(self) -> float:
        return self.weight * 5.0


@dataclass(kw_only=True)
class LiquidContainer(Container):
    def consumption(self) -> float:
        return self.weight * 4.0
