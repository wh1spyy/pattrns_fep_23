class Customer:
    def __init__(self, ID, name, age, operators, bills, limitingAmount):
        self.ID = ID
        self.name = name
        self.age = age
        self.operators = operators
        self.bills = bills
        self.limitingAmount = limitingAmount

    def talk(self, minute, other):
        if self.operators and other.operators and self.check(self.operators.calculateTalkingCost(minute, self)):
            cost = self.operators.calculateTalkingCost(minute, self)
            if self.age < 18 or self.age > 65:
                cost *= (1.0 - self.operators.getDiscountRate() / 100.0)
            self.bills.add(cost)

    def message(self, quantity, other):
        if self.operators and other.operators and self.check(self.operators.calculateMessageCost(quantity, self, other)):
            cost = self.operators.calculateMessageCost(quantity, self, other)
            if self.operators == other.operators:
                cost *= (1.0 - self.operators.getDiscountRate() / 100.0)
            self.bills.add(cost)

    def connection(self, amount):
        if self.operators and self.check(self.operators.calculateNetworkCost(amount)):
            self.bills.add(self.operators.calculateNetworkCost(amount))

    def pay(self, amount):
        if self.check(amount):
            self.bills.pay(amount)

    def change_operator(self, new_operator):
        self.operators = new_operator

    def change_bill_limit(self, amount):
        self.bills.change_the_limit(amount)

    def check(self, amount):
        return (self.bills.get_current_debt() + amount) <= self.limitingAmount

    def get_age(self):
        return self.age

    def set_age(self, age):
        self.age = age

    def get_operator(self):
        return self.operators

    def set_operator(self, operators):
        self.operators = operators

    def get_bill(self):
        return self.bills

    def set_bill(self, bills):
        self.bills = bills


class Operator:
    def __init__(self, ID, talkingCharge, messageCost, networkCharge, discountRate):
        self.ID = ID
        self.talkingCharge = talkingCharge
        self.messageCost = messageCost
        self.networkCharge = networkCharge
        self.discountRate = discountRate

    def calculateTalkingCost(self, minute, customer):
        return minute * self.talkingCharge

    def calculateMessageCost(self, quantity, customer, other):
        return quantity * self.messageCost

    def calculateNetworkCost(self, amount):
        return amount * self.networkCharge

    def getDiscountRate(self):
        return self.discountRate

    def setDiscountRate(self, discountRate):
        self.discountRate = discountRate


class Bill:
    def __init__(self, limitingAmount):
        self.limitingAmount = limitingAmount
        self.currentDebt = 0.0

    def check(self, amount):
        return (self.currentDebt + amount) <= self.limitingAmount

    def add(self, amount):
        self.currentDebt += amount

    def pay(self, amount):
        self.currentDebt -= amount

    def change_the_limit(self, amount):
        self.limitingAmount = amount

    def get_limiting_amount(self):
        return self.limitingAmount

    def get_current_debt(self):
        return self.currentDebt

if __name__ == "__main__":
    N = 5  
    M = 3 
    customers = []
    operators = []
    bills = []

    for i in range(N):
        customers.append(Customer(i, f"Customer{i}", 30, None, None, 100.0))
        bills.append(Bill(1000.0)) 
        customers[i].set_bill(bills[i])

    for i in range(M):
        operators.append(Operator(i, 0.1, 0.02, 0.001, 10)) 
