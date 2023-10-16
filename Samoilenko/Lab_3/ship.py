from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import uuid4

# Dataclass, який визначає конфігурацію судна
@dataclass
class ConfigShip:
    total_weight_capacity: int
    max_number_of_all_containers: int
    maxNumberOfHeavyContainers: int
    maxNumberOfRefrigeratedContainers: int
    maxNumberOfLiquidContainers: int
    fuelConsumptionPerKM: float

# Абстрактний клас IShip визначає методи, які повинні бути реалізовані в підкласах.
class IShip(ABC):

    @abstractmethod
    def sail_to(self, Port) -> bool:
        pass

    @abstractmethod
    def refuel(self, amount_of_fuel: float) -> None:
        pass

    @abstractmethod
    def load(self, container) -> bool:
        pass

    @abstractmethod
    def unload(self, container) -> bool:
        pass

# Клас Ship реалізує функціональність судна, успадковуючи IShip.
class Ship(IShip):
    """Реалізація судна"""

    def __init__(self, port: 'Port', ship_config: ConfigShip, fuel: float = 0.0) -> None:
        # Конструктор судна ініціалізує його атрибути.
        self.id = uuid4()  # Унікальний ідентифікатор судна (UUID).
        self.fuel = fuel  # Кількість пального на борту судна.
        self.port = port  # Початковий порт судна.
        self.configs = ship_config  # Конфігурація судна.
        self.containers = []  # Контейнери, що перевозить судно.

    def get_current_containers(self) -> list:
        # Повертає список контейнерів на борту судна.
        return self.containers

    def sail_to(self, port: 'Port') -> bool:
        # Метод, який визначає можливість руху судна до заданого порту.
        if self.fuel > 0:
            distance = self.port.get_distance(port)
            fuel_needed = distance * self.configs.fuelConsumptionPerKM
            if self.fuel >= fuel_needed:
                self.fuel -= fuel_needed
                self.port = port
                return True
        return False

    def refuel(self, amount_of_fuel: float) -> None:
        # Метод для заправки пального судна.
        self.fuel += amount_of_fuel

    def load(self, container) -> bool:
        # Метод для завантаження контейнера на судно.
        if len(self.containers) < self.configs.max_number_of_all_containers:
            self.containers.append(container)
            return True
        return False

    def unload(self, container) -> bool:
        # Метод для вивантаження контейнера з судна.
        if container in self.containers:
            self.containers.remove(container)
            return True
        return False
