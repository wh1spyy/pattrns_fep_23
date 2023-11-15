import json
from containers import BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer, Container
from ship import Ship, ConfigShip
from port import Port


# Define the serialize_container function
def serialize_container(containers: Container) -> dict:
    return {
        "container_id": container.container_id,
        "weight": container.weight,
        "type": container.__class__.__name__,
        "consumption": container.consumption()
    }


# Define the serialize_port function
def serialize_port(port: Port) -> dict:
    def serialize_container(container) -> dict:
        if isinstance(container, Container):
            return {
                "container_id": container.container_id,
                "weight": container.weight,
                "type": container.__class__.__name__,
                "consumption": container.consumption()
            }
        return {}

    return {
        "port_id": port.port_id,
        "latitude": port.latitude,
        "longitude": port.longitude,
        "containers": [serialize_container(container) for container in port.containers if
                       isinstance(container, Container)],
        "ship_history": [ship.to_dict() if isinstance(ship, Ship) else ship for ship in port.ship_history],
        "current_ships": [ship.to_dict() if isinstance(ship, Ship) else ship for ship in port.current_ships]
    }


# Load data from JSON file
with open("input.json", "r") as json_file:
    data = json.load(json_file)

# Parse data from JSON
ship_data = data["ships"]
container_data = data["containers"]
port_data = data["ports"]

# Create a list of ports
ports = [Port(**port_info) for port_info in port_data]

# Create ships
ships = []
for ship_info in ship_data:
    config = ConfigShip(**ship_info)
    destination_port_id = ship_info['destination_port_id']

    # Find the destination port for the ship
    destination_port_info = next((port_info for port_info in port_data if port_info["port_id"] == destination_port_id),
                                 None)

    if destination_port_info is not None:
        destination_port = Port(**destination_port_info)
        ship = Ship(
            port=ports,  # Use the 'ports' list here
            destination_port=destination_port,
            configs=config,
            fuel=100.0,
            containers=container_data
        )
        ships.append(ship)
    else:
        print(f"Port not found for ship with destination_port_id={destination_port_id}")

# Create containers
container_objects = []

for container_info in container_data:
    container_type = container_info["type"]
    if container_type == "BasicContainer":
        container = BasicContainer(**container_info)
    elif container_type == "HeavyContainer":
        container = HeavyContainer(**container_info)
    elif container_type == "RefrigeratedContainer":
        container = RefrigeratedContainer(**container_info)
    elif container_type == "LiquidContainer":
        container = LiquidContainer(**container_info)
    else:
        # Handle unknown container type
        continue

    container_objects.append(container)

# Perform operations in a loop
for ship in ships:
    for container in container_objects[:]:  # Iterate over container_objects
        if ship.load(container):
            container_objects.remove(container)  # Remove from container_objects

    for port in ports:
        if ship.sail_to(port):
            ship.refuel(100.0)


# Serialize data for output
def serialize_ship(ship: Ship) -> dict:
    # Get a list of container_ids for this ship
    container_ids = ship.configs.container_ids

    def serialize_ship_container(container):
        if isinstance(container, dict):
            return {
                "container_id": container["container_id"],
                "weight": container["weight"],
                "type": container["type"],
                "consumption": None  # You can add logic for consumption if available in the dictionary
            }
        return {
            "container_id": container.container_id,
            "weight": container.weight,
            "type": container.__class__.__name__,
            "consumption": container.consumption()
        }

    containers_for_ship = [serialize_ship_container(container) for container in ship.containers if
                           (isinstance(container, dict) and container["container_id"] in container_ids) or
                           (isinstance(container, Container) and container.container_id in container_ids)]

    return {
        "ship_id": ship.id,
        "destination_port_id": ship.destination_port.port_id,
        "total_weight_capacity": ship.configs.total_weight_capacity,
        "fuel_consumption_per_km": ship.configs.fuel_consumption_per_km,
        "containers": containers_for_ship
    }


# Update the output_data variable to call serialize_container for each container
output_data = {
    "ships": [serialize_ship(ship) for ship in ships],
    "ports": [serialize_port(port) for port in ports],
    "containers": [serialize_container(container) for container in container_objects]
}

# Save the output data to a JSON file
with open("output.json", "w") as output_file:
    json.dump(output_data, output_file, indent=4, default=lambda x: x.__dict__)