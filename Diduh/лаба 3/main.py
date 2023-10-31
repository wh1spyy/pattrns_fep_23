import json
from uuid import UUID
from port import Port
from container import BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer
from ship import LightWeightShipBuilder, MediumShipBuilder, HeavyShipBuilder

with open('input.json', 'r') as file:
    data = json.load(file)

ports = {}
containers = []

for port_data in data:
    port_id = UUID(port_data['port_id'])
    latitude = port_data.get('latitude', 0)
    longitude = port_data.get('longitude', 0)
    port = Port(port_id, latitude, longitude)
    ports[port_id] = port

    basic_count = port_data.get('basic', 0)
    heavy_count = port_data.get('heavy', 0)
    refrigerated_count = port_data.get('refrigerated', 0)
    liquid_count = port_data.get('liquid', 0)

    for _ in range(basic_count):
        containers.append(BasicContainer(weight=867.0))

    for _ in range(heavy_count):
        containers.append(HeavyContainer(weight=1634.0))

    for _ in range(refrigerated_count):
        containers.append(RefrigeratedContainer(weight=790.0))

    for _ in range(liquid_count):
        containers.append(LiquidContainer(weight=540.0))

ships = {}

for port_data in data:
    for ship_data in port_data.get('ships', []):
        ship_id = UUID(ship_data['ship_id'])
        port_id = UUID(ship_data['port_id'])
        port = ports[port_id]

        ship_type = ship_data['ship_type']
        ship_builder = None

        if ship_type == 'LightWeightShip':
            ship_builder = LightWeightShipBuilder()
        elif ship_type == 'MediumShip':
            ship_builder = MediumShipBuilder()
        elif ship_type == 'HeavyShip':
            ship_builder = HeavyShipBuilder()

        if ship_builder is not None:
            ship = ship_builder.build_ship(port)
            ships[ship_id] = ship

for port_data in data:
    port_id = UUID(port_data['port_id'])
    port = ports[port_id]

    for ship_data in port_data.get('ships', []):
        ship_id = UUID(ship_data['ship_id'])
        ship = ships[ship_id]

        for container in containers:
            ship.load(container)

        ship.refuel(40.0)

        next_port_id = UUID(ship_data['ports_deliver'])
        next_port = ports.get(next_port_id)

        if next_port and port.incoming_ship(ship) and ship.sail_to(next_port) and port.outgoing_ship(ship):
            for container in containers:
                ship.unload(container)

updated_data = []

for port_id, port in ports.items():
    port_data = {
        'port_id': str(port_id),
        'longitude': port.longitude,
        'latitude': port.latitude,
        'ships': [],
        'basic': 0,
        'heavy': 0,
        'refrigerated': 0,
        'liquid': 0
    }
    for ship in port.current_ships:
        ship_data = {
            'ship_id': str(ship.id),
            'port_id': str(ship.port.id),
            'ports_deliver': str(next_port_id),
            'ship_type': ship.__class__.__name__,
            'totalWeightCapacity': ship.configs.total_weight_capacity,
            'maxNumberOfAllContainers': ship.configs.max_number_of_all_containers,
            'maxNumberOfHeavyContainers': ship.configs.maxNumberOfHeavyContainers,
            'maxNumberOfRefrigeratedContainers': ship.configs.maxNumberOfRefrigeratedContainers,
            'maxNumberOfLiquidContainers': ship.configs.maxNumberOfLiquidContainers,
            'fuelConsumptionPerKM': ship.configs.fuelConsumptionPerKM
        }
        port_data['ships'].append(ship_data)

    updated_data.append(port_data)

data = updated_data

with open('output.json', 'w') as file:
    json.dump(data, file, indent=4)
