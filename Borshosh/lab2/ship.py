from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List
from port import Port

from containers import Container


@dataclass(kw_only=True)
class ConfigShip:
    ship_id: int
    destination_port_id: int
    total_weight_capacity: int
    max_number_of_all_containers: int
    max_number_of_heavy_containers: int
    max_number_of_refrigerated_containers: int
    max_number_of_liquid_containers: int
    fuel_consumption_per_km: float
    container_ids: List[int]


@dataclass(kw_only=True)
class IShip(ABC):

    @abstractmethod
    def sail_to(self, port: Port) -> bool:
        pass

    @abstractmethod
    def refuel(self, amount_of_fuel: float) -> None:
        pass

    @abstractmethod
    def load(self, container: Container) -> bool:
        pass

    @abstractmethod
    def unload(self, containers: Container) -> bool:
        pass


@dataclass(kw_only=True)
class Ship(IShip):
    port: Port
    destination_port: Port
    configs: ConfigShip
    fuel: float
    containers: List[Container]
    ship_counter: int = 1



    def __post_init__(self):
        self.id = Ship.ship_counter
        Ship.ship_counter += 1

    def get_current_containers(self) -> list:
        container_info = []
        for containers in self.containers:
            container_data = {
                "id": containers.container_id,
                "weight": containers.weight,
                "type": containers.__class__.__name__
            }
            container_info.append(container_data)
        return container_info

    def sail_to(self, port: Port) -> bool:
        if self.fuel > 0 and isinstance(self.port, Port) and isinstance(port, Port):
            distance = self.port.get_distance(port)
            fuel_required = distance * self.configs.fuel_consumption_per_km
            if self.fuel >= fuel_required:
                self.fuel -= fuel_required
                if self.port.outgoing_ship(self) and port.incoming_ship(self):
                    self.destination_port = port
                    return True
        return False

    def refuel(self, amount_of_fuel: float) -> None:
        self.fuel += amount_of_fuel

    def load(self, containers: Container) -> bool:
        if len(self.containers) < self.configs.max_number_of_all_containers:
            self.containers.append(containers)
            return True
        return False

    def unload(self, container: Container) -> bool:
        if container in self.containers:
            self.containers.remove(container)
            return True
        return False

    def to_dict(self):
        pass