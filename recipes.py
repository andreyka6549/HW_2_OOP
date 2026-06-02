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


class ShoppingList:
    def __init__(self) -> None:
        self._items: list[tuple[Ingredient, str]] = []

    def add_recipe(self, recipe: Recipe, portions: float) -> None:
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        new_recipe: Recipe = recipe.scale(portions)
        for ingredient in new_recipe.ingredients:
            self._items.append((ingredient, new_recipe.title))

    def remove_recipe(self, title: str) -> None:
        for i in range(len(self._items) - 1, -1, -1):
            if self._items[i][1] == title:
                self._items.pop(i)

    def get_list(self) -> list[Ingredient]:
        d: dict[tuple[str, str], float] = {}
        for item in self._items:
            key = (item[0].name, item[0].unit)
            if d.get(key, None) is not None:
                d[key] += item[0].quantity
            else:
                d[key] = item[0].quantity

        ret: list[Ingredient] = [Ingredient(name, quantity, unit) for (name, unit), quantity in d.items()]
        ret.sort(key=lambda x: x.name)
        return ret

    def __add__(self, other: "ShoppingList") -> "ShoppingList":
        new_items = [(Ingredient(ing.name, ing.quantity, ing.unit), title) for ing, title in (self._items + other._items)]
        new_list = ShoppingList()
        new_list._items = new_items
        return new_list
