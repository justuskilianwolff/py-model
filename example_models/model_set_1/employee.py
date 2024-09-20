from .person import Person


class Employee(Person):
    def __init__(self, name: str, age: int, employee_id: int, salary, should_not_show):
        super().__init__(name, age)
        self.employee_id: int = employee_id
        self.salary = salary

    def spend_salary(self, amount: float, test="salary"):
        print(f"{self.name} is spending {amount} of their {test}.")
