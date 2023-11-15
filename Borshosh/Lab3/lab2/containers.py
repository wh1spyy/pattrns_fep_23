from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from typing import TYPE_CHECKING, List


@dataclass(kw_only=True)
class Container(ABC):
    container_id: int
    weight: int
    type: str

    @abstractmethod
    def consumption(self) -> float:
        pass

    def to_dict(self) -> dict:
        return {
            "container_id": self.container_id,
            "weight": self.weight,
            "type": self.type
        }

    def __eq__(self, other) -> bool:
        id_check = self.container_id == other.id
        weight_check = self.weight == other.weight
        type_check = self.__class__ == other.__class__
        if id_check and weight_check and type_check:
            return True
        else:
            return False


@dataclass(kw_only=True)
class BasicContainer(Container):

    def consumption(self) -> float:
        return self.weight * 2.5

    def to_dict(self) -> dict:
        return {
            "container_id": self.container_id,
            "weight": self.weight,
        }


@dataclass(kw_only=True)
class HeavyContainer(Container):

    def consumption(self) -> float:
        return self.weight * 3.0

    def to_dict(self) -> dict:
        return {
            "container_id": self.container_id,
            "weight": self.weight,
        }


@dataclass(kw_only=True)
class RefrigeratedContainer(HeavyContainer):
    def consumption(self) -> float:
        return self.weight * 5.0

    def to_dict(self) -> dict:
        return {
            "container_id": self.container_id,
            "weight": self.weight,
        }


@dataclass(kw_only=True)
class LiquidContainer(HeavyContainer):

    def consumption(self) -> float:
        return self.weight * 4.0

    def to_dict(self) -> dict:
        return {
            "container_id": self.container_id,
            "weight": self.weight,
        }