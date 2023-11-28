class Customer:
    def __init__(self, id, name, age, operator, bills, limiting_amount):
        self.id = id
        self.name = name
        self.age = age
        self.operator = operator
        self.bills = bills
        self.limiting_amount = limiting_amount

    def talk(self, other, minutes):
        # Перевірка наявності оператора та додаткових перевірок
        if not self.operator:
            print("Не достатньо вільних операторів для розмови.")
            return

        if not self.bills or not self.bills[0]:
            print("Помилка: Немає рахунку для клієнта.")
            return

        if self.bills[0].check(minutes * self.operator.talking_charge):
            return
        # Обчислення вартості розмови
        cost = minutes * self.operator.talking_charge

        # Застосування знижки
        if 18 <= self.age <= 65:
            cost = cost * (1 - self.operator.discount_rate / 100)
        # Додавання вартості розмови до рахунку
        self.bills[0].pay(cost)
        # Вивід інформації про розмову
        print(
            f"{self.name} розмовляє з {other.name} протягом {minutes} хвилин. Загальна сума: {self.bills[0].current_debt}")

    def message(self, other, quantity):
        # Перевірка ліміту витрат
        if not self.operator:
            print("Попередження: Недостатньо операторів для надсилання повідомлень.")
            return

        # Перевірка існування рахунку для клієнта
        if not self.bills:
            self.bills.append(Bill(self.limiting_amount))

        # Перевірка існування рахунку для іншого клієнта
        if not other.bills:
            other.bills.append(Bill(other.limiting_amount))

        if self.bills[0].check(quantity * other.operator.message_cost):
            return

        # Обчислення вартості повідомлень
        cost = quantity * other.operator.message_cost

        # Застосування знижки, якщо обидва клієнти використовують одного оператора
        if self.operator == other.operator:
            cost = cost * (1 - other.operator.discount_rate / 100)

        # Додавання вартості повідомлень до рахунку
        self.bills[0].pay(cost)

        print(
            f"{self.name} відправив {quantity} повідомлень для  {other.name}  Вартість: {cost}. Загальна сума: {self.bills[0].current_debt}")

    def connection(self, amount):
        # Перевірка ліміту витрат
        if not self.operator or not self.bills or self.bills[0].check(amount * self.operator.network_charge):
            print("Попередження: Недостатньо операторів або рахунку для використання Інтернету.")
            return

        # Обчислення вартості використання Інтернету
        cost = amount * self.operator.network_charge

        # Додавання вартості використання Інтернету до рахунку
        self.bills[0].pay(cost)

        # Вивід інформації про використання Інтернету
        print(f"{self.name} використовує Інтернет на суму: {cost}. Загальна сума: {self.bills[0].current_debt}")

    def pay(self, amount):
        # Додавання суми оплати до рахунку
        self.bills[0].pay(amount)

    def change_operator(self, operator):
        # Перевірка наявності оператора
        if operator not in main_program.operators:
            print(f"Попередження: Немає оператора з ім'ям {operator.name}")
            return

        # Перенесення рахунку на нового оператора
        self.bills[0].operator = operator

    def change_limiting_amount(self, limiting_amount):
        # Перевірка допустимості значення
        if limiting_amount < 0:
            return

        # Зміна ліміту витрат
        self.limiting_amount = limiting_amount



# Клас оператора
class Operator:
    def __init__(self, id, name, talking_charge, message_cost, network_charge, discount_rate):
        self.id = id
        self.name = name
        self.talking_charge = talking_charge
        self.message_cost = message_cost
        self.network_charge = network_charge
        self.discount_rate = discount_rate

    def calculate_talking_cost(self, minutes, customer):
        # Перевірка віку клієнта
        if customer.age < 18 or customer.age > 65:
            cost = minutes * self.talking_charge * (1 - self.discount_rate / 100)
        else:
            cost = minutes * self.talking_charge
        return cost

    def calculate_message_cost(self, quantity, customer1, customer2):
        # Перевірка того, що обидва клієнта використовують одного оператора
        if self.id == customer1.operator[0].id and self.id == customer2.operator[0].id:
            cost = quantity * self.message_cost * (1 - self.discount_rate / 100)
        else:
            cost = quantity * self.message_cost
        return cost

    def calculate_network_cost(self, amount):
        return amount * self.network_charge


# Клас рахунку
class Bill:
    def __init__(self, limiting_amount):
        self.limiting_amount = limiting_amount
        self.current_debt = 0

    def check(self, amount):
        return self.current_debt + amount < self.limiting_amount

    def add(self, amount):
        self.current_debt += amount

    def pay(self, amount):
        self.current_debt -= amount

# Клас головної програми
class Main:
    def __init__(self):
        self.customers = []
        self.operators = []
        self.bills = []

    def create_customer(self, first_name, second_name, age, limiting_amount, initial_balance):
        new_customer = Customer(len(self.customers), f"{first_name} {second_name}", age, None, [Bill(limiting_amount)], limiting_amount)
        # print(self.operators)
        # Перевірка наявності операторів
        if len(self.operators) > 0:
            new_customer.operator = self.operators[0]  # Присвоєння першого оператора, якщо вони є

        # Застосування знижки для клієнтів віком від 18 до 65 років
        if 18 <= age <= 65 and new_customer.operator:
            new_customer.operator.discount_rate = 0

        # Присвоєння оператора клієнтові
        new_customer.operator = self.operators[0] if self.operators else None

        # Встановлення початкового балансу
        new_customer.pay(-initial_balance)

        self.customers.append(new_customer)

    def create_operator(self, operator_data):
        new_operator = Operator(
            operator_data["id"],
            operator_data["name"],
            operator_data["talking_charge"],
            operator_data["message_cost"],
            operator_data["network_charge"],
            operator_data["discount_rate"]
        )
        self.operators.append(new_operator)

    def main(self):
        # Встановлення початкового балансу на рахунках клієнтів
        initial_balance = 2000
        for operator_data in [
            {"id": 1123, "name": "Operator1", "talking_charge": 1.2, "message_cost": 0.79, "network_charge": 0.25, "discount_rate": 10},
            {"id": 1124, "name": "Operator2", "talking_charge": 2, "message_cost": 0.8, "network_charge": 0.2, "discount_rate": 15},
            {"id": 3213, "name": "Operator3", "talking_charge": 2.65, "message_cost": 0.88, "network_charge": 0.21, "discount_rate": 9},
            {"id": 5325, "name": "Operator4", "talking_charge": 0.31, "message_cost": 1.55, "network_charge": 0.11, "discount_rate": 12}
        ]:
            self.create_operator(operator_data)

        for customer_data in [
            {"first_name": "Customer", "second_name": "1", "age": 35},
            {"first_name": "Customer", "second_name": "2", "age": 43},
            {"first_name": "Customer", "second_name": "3", "age": 15}
        ]:
            self.create_customer(**customer_data, limiting_amount=150, initial_balance=initial_balance)



        # Переконайтеся, що у вас достатньо клієнтів та операторів перед викликом методу
        if len(main_program.customers) > 0 and len(self.operators) > 0:
            for customer in self.customers:
                print(f"{customer.name} має на рахунку: {customer.bills[0].current_debt}")
            # Додавання основної логіки взаємодії клієнтів та операторів
            # Приклад виклику методу talk для клієнта
            self.customers[0].talk(self.operators[1], 10)
            self.customers[1].talk(self.operators[2], 30)
            self.customers[0].talk(self.customers[1], 10)
            self.customers[1].talk(self.customers[2], 15)

            # Тест: Виклик інших методів та вивід інформації
            self.customers[0].message(self.customers[2], 50)
            self.customers[0].message(self.customers[1], 10)

            self.customers[0].connection(10)
            self.customers[1].connection(40)
            self.customers[2].connection(200)


        else:
            print("Потрібно створити принаймні по одному клієнту та оператору.")

        # Вивід інформації про клієнтів та їх рахунки
        for customer in self.customers:
            # print(f"{customer.name} має на рахунку: {customer.bills[0].current_debt}")

            # Викликаємо метод talk() для кожного клієнта з індексом 1 та тривалістю розмови 40
            if len(self.operators) > 1:
                operator_index = 1
                operator = self.operators[operator_index]
                cost = operator.calculate_talking_cost(40, customer)
                customer.bills[0].pay(cost)

            print(f"Після розмови {customer.name} має на рахунку: {customer.bills[0].current_debt}")



# Створення об'єкта головної програми та запуск основної логіки
main_program = Main()
main_program.main()
