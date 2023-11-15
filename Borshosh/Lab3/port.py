"""Holds details about port objects"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import haversine as hs
from containers import Container
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ship import Ship


@dataclass(kw_only=True)
class IPort(ABC):

    @abstractmethod
    def incoming_ship(self, ship: Ship):
        pass

    @abstractmethod
    def outgoing_ship(self, ship: Ship):
        pass


@dataclass(kw_only=True)
class Port(IPort):
    """Implements port logic"""

    port_id: int
    latitude: float
    longitude: float
    containers: List[Container] = field(default=list)
    ship_history: List[Ship] = field(default=list)
    current_ships: List[Ship] = field(default=list)

    def to_dict(self):
        return {
            "port_id": self.port_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "containers": [container.__dict__ for container in self.containers],
            "ship_history": [ship.__dict__ for ship in self.ship_history],
            "current_ships": [ship.__dict__ for ship in self.current_ships]
        }

    def get_distance(self, port) -> float:
        dist = hs.haversine((self.latitude, self.longitude), (port.latitude, port.longitude))
        return dist

    def incoming_ship(self, ship: Ship) -> bool:
        if isinstance(ship, Ship) and ship not in self.current_ships:
            self.current_ships.append(ship)
            return True
        return False

    def outgoing_ship(self, ship: Ship) -> bool:
        if ship in self.current_ships and isinstance(ship, Ship):
            self.ship_history.append(ship)
            self.current_ships.remove(ship)
            return True
        return False
