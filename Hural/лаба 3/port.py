from abc import ABC, abstractmethod
from uuid import uuid4
import haversine as hs

class IPort(ABC):
    @abstractmethod
    def incoming_ship(self, ship) -> bool:
        pass

    @abstractmethod
    def outgoing_ship(self, ship) -> bool:
        pass

class Port(IPort):
    def __init__(self, port_id: str, latitude: float, longitude: float) -> None:
        self.id = port_id
        self.containers = []
        self.ship_history = []
        self.current_ships = []
        self.latitude = latitude
        self.longitude = longitude

    def get_distance(self, port) -> float:
        dist = hs.haversine((self.latitude, self.longitude), (port.latitude, port.longitude))
        return dist

    def incoming_ship(self, ship) -> bool:
        if ship not in self.ship_history:
            return False
        for container in ship.containers:
            if container not in self.containers:
                return False
        self.current_ships.append(ship)
        return True

    def outgoing_ship(self, ship) -> bool:
        if ship not in self.ship_history:
            return False
        for container in ship.containers:
            if container not in self.containers:
                return False
        self.current_ships.remove(ship)
        self.ship_history.remove(ship)
        return True
