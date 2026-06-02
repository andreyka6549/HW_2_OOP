class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str) -> None:
        self.name: str = name
        self.quantity: float = quantity
        self.unit: str = unit

    @property
    def quantity(self) -> float:
        return self._quantity

    @quantity.setter
    def quantity(self, value) -> None:
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = float(value)

    def __str__(self) -> str:
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self) -> str:
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.unit == other.unit


