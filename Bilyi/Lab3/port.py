from abc import ABC, abstractmethod
from uuid import uuid4
import haversine as hs
from ship import Ship

if __name__ == "__main__" or __name__ == "port":
    from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ship import Ship

class IPort(ABC):

    @abstractmethod
    def incoming_ship(self, ship: 'Ship'):
        pass

    @abstractmethod
    def outgoing_ship(self, ship: 'Ship'):
        pass

class Port(IPort):
    """Implements port logic"""

    def __init__(self, port_id: str,latitude : float,longitude : float) -> None:
        self.id = port_id
        self.containers = []
        self.ship_history = []
        self.current_ships = []
        self.latitude=longitude
        self.longitude=latitude
        self.items = []

    def get_items_for_ship(self, ship_configs):
        items_to_load = []
        for item in self.items:
            if item.can_load_on_ship(ship_configs):
                items_to_load.append(item)
                self.items.remove(item)
        return items_to_load


    def unload_items(self, items_to_unload):
        for item in items_to_unload:
            self.items.remove(item)

    def receive_items(self, items):
        self.items.extend(items)


    def get_distance(self, port) -> float:
        dist = hs.haversine((self.latitude, self.longitude), (port.latitude, port.longitude))
        return dist

    def incoming_ship(self, ship: 'Ship') -> bool:
        if isinstance(ship, Ship) and ship not in self.current_ships:
            self.current_ships.append(ship)
            return True
        return False

    def outgoing_ship(self, ship: 'Ship') -> bool:
        if isinstance(ship, Ship) and ship in self.current_ships:
            self.current_ships.remove(ship)
            self.ship_history.append(ship)
            return True
        return False


