from dataclasses import dataclass

from .employee import Employee


@dataclass
class Company:
    company_name: str
    employees: list[Employee]

    def go_public(self, stock_price: float) -> None:
        self.public: bool = True
        self.sold = False
        print(f"{self.company_name} is going public at a stock price of {stock_price}.")

    def sell(self) -> tuple[float, int]:
        print(f"{self.company_name} is being sold.")
        return (100.0, 10)
