import json
from uuid import uuid4
import random


def generate_coordinates():
    return round(random.uniform(-90, 90), 6)


ports_id = [str(uuid4()) for _ in range(5)]


ship_types = {
    'LightWeight': {
        'totalWeightCapacity': (10000, 50000),
        'maxNumberOfAllContainers': (10, 50),
        'maxNumberOfHeavyContainers': (5, 15),
        'maxNumberOfRefrigeratedContainers': (2, 10),
        'maxNumberOfLiquidContainers': (5, 10),
        'fuelConsumptionPerKM': (0.1, 0.2)
    },
    'Medium': {
        'totalWeightCapacity': (50000, 75000),
        'maxNumberOfAllContainers': (40, 80),
        'maxNumberOfHeavyContainers': (10, 25),
        'maxNumberOfRefrigeratedContainers': (5, 15),
        'maxNumberOfLiquidContainers': (10, 15),
        'fuelConsumptionPerKM': (0.2, 0.3)
    },
    'Heavy': {
        'totalWeightCapacity': (75000, 100000),
        'maxNumberOfAllContainers': (80, 100),
        'maxNumberOfHeavyContainers': (25, 30),
        'maxNumberOfRefrigeratedContainers': (15, 20),
        'maxNumberOfLiquidContainers': (15, 20),
        'fuelConsumptionPerKM': (0.3, 0.5)
    }
}
item_types = {
    'BasicItem': {
        'weightMultiplier': 1.5
    },
    'HeavyItem': {
        'weightMultiplier': 3.0
    },
    'RefrigeratedItem': {
        'weightMultiplier': 4.0
    },
    'LiquidItem': {
        'weightMultiplier': 5.0
    }
}

# Ships
ships = []
for i in range(5):
    ship_type = random.choice(list(ship_types.keys()))
    ship_config = ship_types[ship_type]


    port_id = random.choice(ports_id)


    fuel_consumption = round(random.uniform(*ship_config['fuelConsumptionPerKM']), 2)

    ship = {
        "ship_id": str(uuid4()),
        "port_id": port_id,
        "ship_type": ship_type,
        "ports_deliver": random.choice([pid for pid in ports_id if pid != port_id]),
        "totalWeightCapacity": random.randint(*ship_config['totalWeightCapacity']),
        "maxNumberOfAllContainers": random.randint(*ship_config['maxNumberOfAllContainers']),
        "maxNumberOfHeavyContainers": random.randint(*ship_config['maxNumberOfHeavyContainers']),
        "maxNumberOfRefrigeratedContainers": random.randint(*ship_config['maxNumberOfRefrigeratedContainers']),
        "maxNumberOfLiquidContainers": random.randint(*ship_config['maxNumberOfLiquidContainers']),
        "fuelConsumptionPerKM": fuel_consumption,
    }
    ships.append(ship)

# Ports
ports = []
for port_id in ports_id:
    port = {
        "port_id": port_id,
        "ships": [ship for ship in ships if ship["port_id"] == port_id],
        "basic": random.randint(1, 10),
        "heavy": random.randint(1, 8),
        "refrigerated": random.randint(1, 5),
        "liquid": random.randint(1, 5),
        "latitude": generate_coordinates(),
        "longitude": generate_coordinates(),
        "items": []
    }

    # items
    for _ in range(5):
        item_type = random.choice(list(item_types.keys()))
        item_config = item_types[item_type]
        item = {
            "item_id": str(uuid4()),
            "weight": round(random.uniform(1, 10), 2),
            "count": random.randint(1, 5),
            "containerID": str(uuid4()),
            "item_type": item_type,
            "total_weight": round(random.uniform(1, 10) * item_config['weightMultiplier'], 2)
        }
        port["items"].append(item)

    ports.append(port)

data = {
    "ports": ports,
    "ships": ships
}

json_object = json.dumps(data, indent=2)

with open("input.json", "w") as outfile:
    outfile.write(json_object)
