import json
from typing import Dict
import uuid

class Customer:
    def __init__(self, id_: uuid.UUID, operators: Dict[str, 'Operator'] = None, first_name: str = "test",
                 second_name: str = "test", age: int = 0):
        self.id = id_
        self.first_name = first_name
        self.second_name = second_name
        self.age = age
        self.operators = operators
        self.bills = {operator_name: operator.create_bill(self.id) for operator_name, operator in
                      self.operators.items()}

    def talk(self, minutes: int, customer: 'Customer', operator_name: str):
        operator = self.operators.get(operator_name)
        if operator is None:
            raise ValueError(f"Operator {operator_name} is not associated with this customer.")

        talking_charge = operator.calculate_talking_cost(minutes)
        cost = talking_charge * (1 - operator.discount_rate / 100) if 18 <= self.age < 65 else talking_charge

        self.bills[operator_name].add(cost)
        print(f"Customer {self.first_name} talked to {customer.first_name} for {minutes} minutes. To be paid: {cost} ₴")
        self.bills[operator_name].pay(cost)
        print("--------------------------------------------------------------")

    def message(self, quantity: int, customer: 'Customer', operator_name: str):
        operator = self.operators.get(operator_name)
        if operator is None:
            raise ValueError(f"Operator {operator_name} is not associated with this customer.")

        message_cost = operator.calculate_message_cost(quantity)
        cost = message_cost * (1 - operator.discount_rate / 100) if self == customer else message_cost

        self.bills[operator_name].add(cost)
        print(f"Customer {self.first_name} sent {quantity} messages to {customer.first_name}. To be paid: {cost} ₴")
        self.bills[operator_name].pay(cost)
        print("--------------------------------------------------------------")

    def connect(self, traffic: float, operator_name: str):
        operator = self.operators.get(operator_name)
        if operator is None:
            raise ValueError(f"Operator {operator_name} is not associated with this customer.")

        network_cost = operator.calculate_network_cost(traffic)
        if not self.bills[operator_name].check(network_cost):
            cost = round(network_cost, 2)
            self.bills[operator_name].add(cost)
            formatted_cost = '{:.2f}'.format(cost)
            print(f"{self.first_name} used {traffic} MB of data. To be paid: {formatted_cost} ₴")
            self.bills[operator_name].pay(cost)
            print("--------------------------------------------------------------")
        else:
            print(f"Customer {self.first_name} reached the bill limit. No action taken.")
            print("--------------------------------------------------------------")


class Operator:
    def __init__(self, id_: int, talking_charge: float, message_cost: float, network_charge: float, discount_rate: int):
        self.id = id_
        self.talking_charge = talking_charge
        self.message_cost = message_cost
        self.network_charge = network_charge
        self.discount_rate = discount_rate

    def create_bill(self, customer_id: int):
        return Bill()

    def calculate_talking_cost(self, minutes: int) -> float:
        return self.talking_charge * minutes

    def calculate_message_cost(self, quantity: int) -> float:
        return self.message_cost * quantity

    def calculate_network_cost(self, amount: float) -> float:
        return self.network_charge * amount


class Bill:
    def __init__(self, limiting_amount: float = 250):
        self.limiting_amount = limiting_amount
        self.current_debt = 0

    def check(self, amount: float) -> bool:
        return self.current_debt + amount > self.limiting_amount

    def add(self, amount: float):
        if self.check(amount):
            raise ValueError("You reached the limit. Operation is forbidden")
        self.current_debt += amount
        print(f"Added {amount} ₴ to debt")

    def pay(self, amount: float):
        if amount < 0:
            raise ValueError("Payment amount cannot be negative")
        self.current_debt = max(0, self.current_debt - amount)
        print(f"Customer paid {amount} towards the bill ✔")

    def change_limit(self, amount: float):
        self.limiting_amount += amount
        print(f"Limit has been changed to {self.limiting_amount}")


def create_customer_from_json(customer_data, operators) -> Customer:
    customer_id = uuid.uuid4()  
    customer = Customer(
        id_=customer_id,
        operators=operators,
        first_name=customer_data["first_name"],
        second_name=customer_data["second_name"],
        age=customer_data["age"]
    )
    return customer


if __name__ == "__main__":
    with open("package.json", "r") as json_file:
        data = json.load(json_file)

    operators = {}
    for operator_data in data["operators"]:
        operator = Operator(
            id_=operator_data["id"],
            talking_charge=operator_data["talking_charge"],
            message_cost=operator_data["message_cost"],
            network_charge=operator_data["network_charge"],
            discount_rate=operator_data["discount_rate"]
        )
        operators[operator_data["name"]] = operator

    customers = []
    for customer_data in data["customers"]:
        customer = create_customer_from_json(customer_data, operators)
        customers.append(customer)

    for customer in customers:
        customer.talk(13, customers[0], "Operator1")
        customer.message(23, customers[1], "Operator2")
        customer.connect(100, "Operator3")

