import json
from uuid import UUID
from port import Port
from container import BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer
from ship import ConfigShip, Ship

# Функція для завантаження даних з файлу
def load_data_from_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Функція для створення словника портів на основі вхідних даних
def create_ports(data):
    ports = {}
    for port_data in data:
        port_id = UUID(port_data['port_id'])
        latitude = port_data.get('latitude', 0)
        longitude = port_data.get('longitude', 0)
        port = Port(port_id, latitude, longitude)
        ports[port_id] = port
    return ports

# Функція для створення списку контейнерів на основі вхідних даних
def create_containers(data):
    containers = []
    for port_data in data:
        basic_count = port_data['basic']
        heavy_count = port_data['heavy']
        refrigerated_count = port_data['refrigerated']
        liquid_count = port_data['liquid']

        for _ in range(basic_count):
            containers.append(BasicContainer(weight=867.0))

        for _ in range(heavy_count):
            containers.append(HeavyContainer(weight=1634.0))

        for _ in range(refrigerated_count):
            containers.append(RefrigeratedContainer(weight=790.0))

        for _ in range(liquid_count):
            containers.append(LiquidContainer(weight=540.0))

    return containers

# Функція для створення словника суден на основі вхідних даних та словника портів
def create_ships(data, ports):
    ships = {}
    for port_data in data:
        for ship_data in port_data['ships']:
            ship_id = UUID(ship_data['ship_id'])
            port_id = UUID(ship_data['port_id'])
            port = ports[port_id]

            ship_config = ConfigShip(
                total_weight_capacity=ship_data['totalWeightCapacity'],
                max_number_of_all_containers=ship_data['maxNumberOfAllContainers'],
                maxNumberOfHeavyContainers=ship_data['maxNumberOfHeavyContainers'],
                maxNumberOfRefrigeratedContainers=ship_data['maxNumberOfRefrigeratedContainers'],
                maxNumberOfLiquidContainers=ship_data['maxNumberOfLiquidContainers'],
                fuelConsumptionPerKM=ship_data['fuelConsumptionPerKM']
            )
            ship = Ship(port, ship_config)
            ships[ship_id] = ship
    return ships

# Головна функція програми
def main():
    # Завантажуємо вхідні дані з файлу
    data = load_data_from_file('input.json')

    # Створюємо словник портів
    ports = create_ports(data)

    # Створюємо список контейнерів
    containers = create_containers(data)

    # Створюємо словник суден
    ships = create_ships(data, ports)

    # Виконуємо операції з контейнерами і суднами
    for port_data in data:
        for ship_data in port_data['ships']:
            ship_id = UUID(ship_data['ship_id'])
            port_id = UUID(ship_data['port_id'])
            port = ports[port_id]
            ship = ships[ship_id]

            for container in containers:
                ship.load(container)

            ship.refuel(40.0)
            next_port_id = UUID(ship_data['ports_deliver'])
            next_port = ports[next_port_id]

            if port.incoming_ship(ship) and ship.sail_to(next_port) and port.outgoing_ship(ship):
                for container in containers:
                    ship.unload(container)

    # Оновлюємо дані для збереження
    updated_data = []
    for port_id, port in ports.items():
        port_data = {
            'port_id': str(port_id),
            'longitude': port.longitude,
            'latitude': port.latitude,
            'ships': [],
            'basic': port_data['basic'],
            'heavy': port_data['heavy'],
            'refrigerated': port_data['refrigerated'],
            'liquid': port_data['liquid']
        }
        for ship in port.current_ships:
            ship_data = {
                'ship_id': str(ship.id),
                'port_id': str(ship.port.id),
                'ports_deliver': str(next_port_id),
                'totalWeightCapacity': ship.configs.total_weight_capacity,
                'maxNumberOfAllContainers': ship.configs.max_number_of_all_containers,
                'maxNumberOfHeavyContainers': ship.configs.maxNumberOfHeavyContainers,
                'maxNumberOfRefrigeratedContainers': ship.configs.maxNumberOfRefrigeratedContainers,
                'maxNumberOfLiquidContainers': ship.configs.maxNumberOfLiquidContainers,
                'fuelConsumptionPerKM': ship.configs.fuelConsumptionPerKM
            }
            port_data['ships'].append(ship_data)

        updated_data.append(port_data)

    # Записуємо оновлені дані у файл
    with open('output.json', 'w') as file:
        json.dump(updated_data, file, indent=4)
