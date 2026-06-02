from numbers import Number

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


class Recipe:
    def __init__(self, title: str) -> None:
        self.title = title
        self.ingredients: list[Ingredient] = []

    def add_ingredient(self, ingredient: Ingredient) -> None:
        for other in self.ingredients:
            if other == ingredient:
                other.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio) -> bool:
        return isinstance(ratio, Number) and ratio > 0

    def scale(self, ratio: float) -> "Recipe": # forward reference https://stackoverflow.com/questions/55320236/does-python-evaluate-type-hinting-of-a-forward-reference первый коммент первое решение
        if not self.is_valid_ratio(ratio): # иначе зачем мы этот метод определяли?
            raise ValueError("Ratio должно быть положительным числом")
        obj: Recipe = Recipe(self.title)
        for ingredient in self.ingredients:
            new_ingredient = Ingredient(ingredient.name, ingredient.quantity * ratio, ingredient.unit)
            obj.add_ingredient(new_ingredient)

        return obj

    def __len__(self) -> int:
        return len(self.ingredients)

    def __str__(self) -> str:
        return f"{self.title}. Список ингридиентов: {self.ingredients}"
