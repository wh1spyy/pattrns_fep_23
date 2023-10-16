from abc import ABC, abstractmethod
import haversine as hs
from ship import Ship

# Перевірка, чи виконується цей файл як основна програма або імпортується
# в інший файл як модуль 'port'.
if __name__ == "__main__" or __name__ == "port":
    from typing import TYPE_CHECKING

# Перевірка, чи виконується код в режимі TYPE_CHECKING (типізація).
if TYPE_CHECKING:
    from ship import Ship

class IPort(ABC):
    # Абстрактний клас, який оголошує методи, які повинні бути реалізовані в підкласах.

    @abstractmethod
    def incoming_ship(self, ship: 'Ship'):
        pass

    @abstractmethod
    def outgoing_ship(self, ship: 'Ship'):
        pass

class Port(IPort):
    # Реалізація інтерфейсу IPort для порту.

    def __init__(self, port_id: str, latitude: float, longitude: float) -> None:
        # Конструктор класу Port, приймає ініціальні значення порту.

        self.id = port_id  # Ідентифікатор порту
        self.containers = []  # Контейнери в порту
        self.ship_history = []  # Історія суден, що виходили з порту
        self.current_ships = []  # Поточні судна в порту
        self.latitude = longitude  # Широта порту
        self.longitude = latitude  # Довгота порту

    def get_distance(self, port) -> float:
        # Метод для обчислення відстані між поточним портом і іншим портом за координатами.
        dist = hs.haversine((self.latitude, self.longitude), (port.latitude, port.longitude))
        return dist

    def incoming_ship(self, ship: 'Ship') -> bool:
        # Метод, який обробляє прибуття судна до порту.
        if isinstance(ship, Ship) and ship not in self.current_ships:
            self.current_ships.append(ship)
            return True
        return False

    def outgoing_ship(self, ship: 'Ship') -> bool:
        # Метод, який обробляє вибуття судна з порту.
        if isinstance(ship, Ship) and ship in self.current_ships:
            self.current_ships.remove(ship)
            self.ship_history.append(ship)
            return True
        return False
