import json
from typing import List, Union
from containers import BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer, Container
from ship import LightWeightShip, MediumShip, HeavyShip, ConfigShip
from port import Port
from item import Item, create_item


# Оновлена функція для серіалізації контейнерів
def serialize_container(container: Union[BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer]) -> dict:
    items_ids = container.items_ids
    item_info = []

    return {
        "container_id": container.container_id,
        "weight": container.weight,
        "type": container.type,
        "consumption": container.consumption() if hasattr(container, "consumption") else None,
        "items": item_info
    }


# Оновлена функція для серіалізації предметів
def serialize_item(item: Item) -> dict:
    item_info = {
        "item_id": item.item_id,
        "weight": item.weight,
        "count": item.count,
        "type": item.type,
        "container_id": item.container_id,
        "total_weight": item.getTotalWeight()
    }

    if "specific_attribute" in item:
        item_info["specific_attribute"] = item["specific_attribute"]
    return item_info


# Оновлена функція для серіалізації портів
def serialize_port(port: Port) -> dict:
    ship_history = [serialize_ship(ship) if isinstance(ship, (LightWeightShip, MediumShip, HeavyShip)) else ship for
                    ship in port.ship_history]
    current_ships = [serialize_ship(ship) if isinstance(ship, (LightWeightShip, MediumShip, HeavyShip)) else ship for
                     ship in port.current_ships]

    return {
        "port_id": port.port_id,
        "latitude": port.latitude,
        "longitude": port.longitude,
        "containers": [serialize_container(container) for container in port.containers if
                       isinstance(container, Container)],
        "ship_history": ship_history,
        "current_ships": current_ships
    }


# Оновлена функція для серіалізації суден
def serialize_ship(ship: Union[LightWeightShip, MediumShip, HeavyShip]) -> dict:
    container_ids = ship.configs.container_ids
    container_info = []

    for container in ship.containers:
        if isinstance(container, dict) and container["container_id"] in container_ids:
            container_items = []
            for item in container["items"]:
                item_info = serialize_item(item)
                container_items.append(item_info)
            container_info.append({
                "container_id": container["container_id"],
                "weight": container["weight"],
                "type": container.get("type"),
                "consumption": container.get("consumption"),
                "items": container_items
            })
        elif isinstance(container, Container) and container.container_id in container_ids:
            container_items = []
            for item in container.items_ids:
                item_info = serialize_item(item_data)
                container_items.append(item_info)
            container_info.append({
                "container_id": container.container_id,
                "weight": container.weight,
                "type": container.type,
                "consumption": container.consumption() if hasattr(container, "consumption") else None,
                "items": container_items
            })

    return {
        "ship_id": ship.id,
        "destination_port_id": ship.destination_port.port_id,
        "total_weight_capacity": ship.configs.total_weight_capacity,
        "fuel_consumption_per_km": ship.configs.fuel_consumption_per_km,
        "containers": container_info
    }


# Завантаження даних з файлу JSON
with open("input.json", "r") as json_file:
    data = json.load(json_file)

# Розбір даних з JSON
ship_data = data["ships"]
container_data = data["containers"]
port_data = data["ports"]
item_data = data.get("items")  # Додаткові дані про предмети, якщо вони доступні

# Створення списку портів
ports = [Port(**port_info) for port_info in port_data]

# Створення суден
ships = []
for ship_info in ship_data:
    config = ConfigShip(**ship_info)
    destination_port_id = ship_info['destination_port_id']

    # Знаходження порту призначення для судна
    destination_port_info = next((port_info for port_info in port_data if port_info["port_id"] == destination_port_id),
                                 None)

    if destination_port_info is not None:
        destination_port = Port(**destination_port_info)
        ship_type = ship_info['type']
        if ship_type == 'LightWeightShip':
            ship = LightWeightShip(
                port=ports,
                destination_port=destination_port,
                configs=config,
                fuel=100.0,
                containers=container_data,
                items=[create_item(item["type"], item) for item in item_data]
            )
        elif ship_type == 'MediumShip':
            ship = MediumShip(
                port=ports,
                destination_port=destination_port,
                configs=config,
                fuel=150.0,
                containers=container_data,
                items=[create_item(item["type"], item) for item in item_data]
            )
        elif ship_type == 'HeavyShip':
            ship = HeavyShip(
                port=ports,
                destination_port=destination_port,
                configs=config,
                fuel=200.0,
                containers=container_data,
                items=[create_item(item["type"], item) for item in item_data]
            )
        else:
            print(f"Unknown ship type: {ship_type}")
            continue

        ships.append(ship)
    else:
        print(f"Port not found for ship with destination_port_id={destination_port_id}")

# Оновлений словник для контейнерів з окремими списками для кожного типу судна
container_objects = {
    "LightWeightShip": [],
    "MediumShip": [],
    "HeavyShip": [],
}

# Створення контейнерів
for container_info in container_data:
    container_type = container_info["type"]
    if container_type in container_objects:
        if container_type == "BasicContainer":
            container = BasicContainer(**container_info)
        elif container_type == "HeavyContainer":
            container = HeavyContainer(**container_info)
        elif container_type == "RefrigeratedContainer":
            container = RefrigeratedContainer(**container_info)
        elif container_type == "LiquidContainer":
            container = LiquidContainer(**container_info)

        container_objects[container_type].append(container)

# Виконання операцій в циклі
for ship in ships:
    for container in container_objects[ship.configs.type]:
        if ship.load(container):
            container_objects[ship.configs.type].remove(container)

    for port in ports:
        if ship.sail_to(port):
            ship.refuel(100.0)

# Серіалізація даних для виводу
output_data = {
    "ships": [serialize_ship(ship) for ship in ships],
    "ports": [serialize_port(port) for port in ports],
    "containers": [serialize_container(container) for containers in container_objects.values() for container in containers],
    "items": item_data  # Включає серіалізацію предметів
}

# Збереження даних в файл JSON
with open("output.json", "w") as output_file:
    json.dump(output_data, output_file, indent=4, default=lambda x: x.__dict__)
