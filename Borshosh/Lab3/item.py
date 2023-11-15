from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Union


@dataclass(kw_only=True)
class Item(ABC):
    item_id: int
    weight: float
    count: int
    container_id: int
    type: str

    @abstractmethod
    def getTotalWeight(self):
        pass

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "weight": self.weight,
            "count": self.count,
            "container_id": self.container_id,
            "type": self.type,
            "total_weight": self.getTotalWeight()
        }


@dataclass(kw_only=True)
class Small(Item):
    specific_attribute: str

    def getTotalWeight(self):
        return self.weight * self.count


@dataclass(kw_only=True)
class Heavy(Item):
    specific_attribute: str

    def getTotalWeight(self):
        return self.weight * self.count


@dataclass(kw_only=True)
class Refrigerated(Item):
    specific_attribute: str

    def getTotalWeight(self):
        return self.weight * self.count


@dataclass(kw_only=True)
class Liquid(Item):
    specific_attribute: str

    def getTotalWeight(self):
        return self.weight * self.count


# Функція для створення об'єктів Item з даних конфігурації
def create_item(item_type: str, config: Dict[str, Union[int, float, str]]) -> Item:
    if item_type == 'Small':
        return Small(**config)
    elif item_type == 'Heavy':
        return Heavy(**config)
    elif item_type == 'Refrigerated':
        return Refrigerated(**config)
    elif item_type == 'Liquid':
        return Liquid(**config)
    else:
        raise ValueError(f"Unknown item type: {item_type}")