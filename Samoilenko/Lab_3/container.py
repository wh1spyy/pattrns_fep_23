from abc import ABC, abstractmethod
from uuid import uuid4

# Абстрактний клас Container визначає спільні атрибути та методи для контейнерів.
class Container(ABC):
    def __init__(self, weight: float) -> None:
        self.id = uuid4()  # Генерує унікальний ідентифікатор контейнера (UUID).
        self.weight = weight

    @abstractmethod
    def consumption(self) -> float:
        pass

    def __eq__(self, other) -> bool:
        # Перевіряє, чи два контейнери рівні за ідентифікатором, вагою та типом.
        id_check = self.id == other.id
        weight_check = self.weight == other.weight
        type_check = self.__class__ == other.__class__
        if id_check and weight_check and type_check:
            return True
        else:
            return False

# Підклас BasicContainer успадковує від Container і реалізує метод consumption.
class BasicContainer(Container):
    def __init__(self, weight: float) -> None:
        super().__init__(weight=weight)

    def consumption(self) -> float:
        # Реалізує розрахунок споживання пального для базового контейнера.
        return self.weight * 2.5

# Підклас HeavyContainer також успадковує від Container та реалізує власний метод consumption.
class HeavyContainer(Container):
    def __init__(self, weight: float) -> None:
        super().__init__(weight=weight)

    def consumption(self) -> float:
        # Реалізує розрахунок споживання пального для важкого контейнера.
        return self.weight * 3.0

# Підклас RefrigeratedContainer успадковує від HeavyContainer та також реалізує метод consumption.
class RefrigeratedContainer(HeavyContainer):
    def __init__(self, weight: float) -> None:
        super().__init__(weight=weight)

    def consumption(self) -> float:
        # Реалізує розрахунок споживання пального для холодильного контейнера.
        return self.weight * 5.0

# Підклас LiquidContainer також успадковує від HeavyContainer і реалізує метод consumption.
class LiquidContainer(HeavyContainer):
    def __init__(self, weight: float) -> None:
        super().__init__(weight=weight)

    def consumption(self) -> float:
        # Реалізує розрахунок споживання пального для рідкого контейнера.
        return self.weight * 4.0
