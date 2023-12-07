#1. load data from JSON
import json
import random
from uuid import uuid4

portsID = [str(uuid4()) for i in range(5)]

dummyShips = []
for i in range(10):
  fillerShipList = {}
  fillerShipList["ship_id"] = str(uuid4())
  fillerShipList["port_id"] = random.choice(portsID)
  fillerShipList["ports_deliver"] = random.choice([i for i in portsID if i != fillerShipList["ship_id"]])
  fillerShipList["totalWeightCapacity"] = 1000
  fillerShipList["maxNumberOfAllContainers"] = 20
  fillerShipList["maxNumberOfHeavyContainers"] = 5
  fillerShipList["maxNumberOfRefrigeratedContainers"] = 2
  fillerShipList["maxNumberOfLiquidContainers"] = 5
  fillerShipList["fuelConsumptionPerKM"] = 20
  dummyShips.append(fillerShipList)



dummyPorts = []
for i in range(5):
  fillerPortList = {}
  fillerPortList["port_id"] = portsID[i]
  fillerPortList["ships"] = [ship for ship in dummyShips if ship["port_id"] == fillerPortList["port_id"]]
  fillerPortList["basic"] = random.randint(1, 10)
  fillerPortList["heavy"] = random.randint(1, 8)
  fillerPortList["refrigerated"] = random.randint(1, 5)
  fillerPortList["liquid"] = random.randint(1, 5)
  dummyPorts.append(fillerPortList)


json_object = json.dumps(dummyPorts, indent=2)


from Containers import *
from Port import IPort, PortClass
from Ship import IShip, ShipСlass, ConfigShip

with open("D:\\University\\2 course\\Semester 1\\Design patterns\\Labs\\Lab2\\input.json", "w") as outfile:
  outfile.write(json_object)

containers = [BasicContainer(250), BasicContainer(450), HeavyContainer(350), RefrigeratedContainer(250.5), LiquidContainer(124)]
ports = [PortClass(
  dummyPorts[i]["port_id"],
  round(random.uniform(0, 10**6)/10**6, 6),
  round(random.uniform(0, 10**6)/10**6, 6),
  containers
) for i in range(len(dummyPorts))]
ships = [ShipСlass(
    dummyShips[i]["ship_id"],
    ports,
    ConfigShip(
        dummyShips[i]["totalWeightCapacity"],
        dummyShips[i]["maxNumberOfAllContainers"],
        dummyShips[i]["maxNumberOfHeavyContainers"],
        dummyShips[i]["maxNumberOfRefrigeratedContainers"],
        dummyShips[i]["maxNumberOfLiquidContainers"],
        dummyShips[i]["fuelConsumptionPerKM"]
    ),
    containers,
    205*(i+1)
  ) for i in range(len(dummyShips))]
for i in range(len(containers)-1):
  for ship in ships:
    if type(containers[i]) == str:
      break
    containerID = containers[i].id
    ship.load(containerID)
    ship.unload(containerID)
    ship.sailTo(ports[i])
  i+=1
