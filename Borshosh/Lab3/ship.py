from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from containers import Container
from port import Port
from item import Item


@dataclass(kw_only=True)
class ConfigShip:
    type: str
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
class Ship(ABC):
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
class LightWeightShip(Ship):
    port: Port
    destination_port: Port
    configs: ConfigShip
    fuel: float
    containers: List[Container]
    items: List[Item]
    ship_counter: int = 1

    def __post_init__(self):
        self.id = LightWeightShip.ship_counter
        LightWeightShip.ship_counter += 1

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

    def load(self, container: Container) -> bool:
        if len(self.containers) < self.configs.max_number_of_all_containers:
            self.containers.append(container)
            return True
        return False

    def unload(self, container: Container) -> bool:
        if container in self.containers:
            self.containers.remove(container)
            return True
        return False


@dataclass(kw_only=True)
class MediumShip(Ship):
    port: Port
    destination_port: Port
    configs: ConfigShip
    fuel: float
    containers: List[Container]
    items: List[Item]
    ship_counter: int = 1

    def __post_init__(self):
        self.id = MediumShip.ship_counter
        MediumShip.ship_counter += 1

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

    def load(self, container: Container) -> bool:
        if len(self.containers) < self.configs.max_number_of_all_containers:
            self.containers.append(container)
            return True
        return False

    def unload(self, container: Container) -> bool:
        if container in self.containers:
            self.containers.remove(container)
            return True
        return False


@dataclass(kw_only=True)
class HeavyShip(Ship):
    port: Port
    destination_port: Port
    configs: ConfigShip
    fuel: float
    containers: List[Container]
    items: List[Item]
    ship_counter: int = 1

    def __post_init__(self):
        self.id = HeavyShip.ship_counter
        HeavyShip.ship_counter += 1

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

    def load(self, container: Container) -> bool:
        if len(self.containers) < self.configs.max_number_of_all_containers:
            self.containers.append(container)
            return True
        return False

    def unload(self, container: Container) -> bool:
        if container in self.containers:
            self.containers.remove(container)
            return True
        return False
