from .person import Person


class Employee(Person):
    def __init__(self, name: str, age: int, employee_id: int, salary):
        super().__init__(name, age)
        self.employee_id = employee_id
        self.salary = salary

    def spend_salary(self, amount: float, test="salary"):
        print(f"{self.name} is spending {amount} of their {test}.")
