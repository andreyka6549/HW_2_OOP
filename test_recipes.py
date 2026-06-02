from recipes import Ingredient, Recipe, ShoppingList
import pytest

class TestIngredient: # Почему я оформил всё в классах? https://habr.com/ru/articles/835196/

    @pytest.fixture  # Что такое фикстура? https://habr.com/ru/articles/716248/
    def flour(self):
        return Ingredient("Мука", 500, "г")

    @pytest.fixture
    def sugar(self):
        return Ingredient("Сахар", 500, "г")

    @pytest.fixture
    def more_flour(self):
        return Ingredient("Мука", 600, "г")

    @pytest.fixture
    def cup_of_flour(self):
        return Ingredient("Мука", 1, "стакан")

    def test_initialization(self, flour):
        assert flour.name == "Мука"
        assert flour.quantity == 500
        assert flour.unit == "г"
        assert isinstance(flour.quantity, float)

    def test_quantity_setter_negative_raises_error(self):
        with pytest.raises(ValueError) as e:
            Ingredient("Мука", -1, "г")
        assert str(e.value) == "Количество должно быть положительным"

    def test_str_representation(self, flour):
        expected = "Мука: 500.0 г"
        assert str(flour) == expected

    def test_eq_same_name_and_unit(self, flour, more_flour):
        assert flour == flour
        assert more_flour == flour

    def test_eq_different_names(self, flour, sugar):
        assert flour != sugar

    def test_eq_different_units(self, flour, cup_of_flour):
        assert flour != cup_of_flour


class TestRecipe:

    @pytest.fixture
    def recipe(self):
        return Recipe("Пицца маргарииииита")

    @pytest.fixture
    def mozzarella(self):
        return Ingredient("Моцарелла", 200, "г")

    @pytest.fixture
    def flour(self):
        return Ingredient("Мука", 300, "г")

    def test_initialization(self, recipe):
        assert recipe.title == "Пицца маргарииииита"
        assert recipe.ingredients == []

    def test_add_ingredient(self, recipe, mozzarella):
        recipe.add_ingredient(mozzarella)
        assert mozzarella in recipe.ingredients
        assert len(recipe) == 1

    def test_add_duplicate_sums_quantity(self, recipe, mozzarella):
        extra = Ingredient("Моцарелла", 100, "г")
        recipe.add_ingredient(mozzarella)
        recipe.add_ingredient(extra)

        assert len(recipe) == 1
        assert recipe.ingredients[0].quantity == 300.0

    def test_scale_returns_new_objects(self, recipe, mozzarella):
        recipe.add_ingredient(mozzarella)
        new_recipe = recipe.scale(2)
        assert new_recipe is not recipe
        assert new_recipe.ingredients is not recipe.ingredients
        assert new_recipe.ingredients[0] is not recipe.ingredients[0]

    def test_scale_doesnt_mutate_original(self, recipe, mozzarella):
        recipe.add_ingredient(mozzarella)
        original_qty = recipe.ingredients[0].quantity
        recipe.scale(5)
        assert recipe.ingredients[0].quantity == original_qty

    def test_scale(self, recipe, mozzarella, flour):
        recipe.add_ingredient(mozzarella)
        recipe.add_ingredient(flour)
        new_recipe = recipe.scale(4.5)
        assert new_recipe.ingredients[0].quantity == 200 * 4.5
        assert new_recipe.ingredients[1].quantity == 300 * 4.5

    def test_scale_with_negative_ratio(self, recipe):
        with pytest.raises(ValueError) as e: # https://habr.com/ru/companies/otus/articles/901858/
            recipe.scale(-0.5)

        assert str(e.value) == "Ratio должно быть положительным числом"

    def test_scale_with_zero_ratio(self, recipe):
        with pytest.raises(ValueError):
            recipe.scale(0)

    def test_len(self, recipe, mozzarella, flour):
        assert len(recipe) == 0
        recipe.add_ingredient(mozzarella)
        assert len(recipe) == 1
        recipe.add_ingredient(flour)
        assert len(recipe) == 2
        recipe.add_ingredient(Ingredient("Мука", 50, "г"))
        assert len(recipe) == 2


class TestShoppingList:

    @pytest.fixture
    def pizza_recipe(self):
        recipe = Recipe("Пицца")
        recipe.add_ingredient(Ingredient("Помидор", 2, "шт"))
        recipe.add_ingredient(Ingredient("Оливковое масло", 3, "ст. л."))
        recipe.add_ingredient(Ingredient("Мука", 250, "г"))
        recipe.add_ingredient(Ingredient("Дрожжи", 10, "г"))
        recipe.add_ingredient(Ingredient("Сахар", 1 / 4, "ч. л."))
        recipe.add_ingredient(Ingredient("Соль", 1 / 4, "ч. л."))
        recipe.add_ingredient(Ingredient("Моцарелла", 150, "г"))
        return recipe

    @pytest.fixture
    def tea_recipe(self):
        recipe = Recipe("Чай")
        recipe.add_ingredient(Ingredient("Кипяток", 250, "мл"))
        recipe.add_ingredient(Ingredient("Чайный пакетик", 1, "шт"))
        recipe.add_ingredient(Ingredient("Сахар", 2, "ч. л."))
        return recipe

    def test_add_recipe_scales_quantities(self, pizza_recipe):
        sl = ShoppingList()
        sl.add_recipe(pizza_recipe, 2)
        items_by_key = {(ing.name, ing.unit): ing.quantity for ing, _ in sl._items}
        for orig_ing in pizza_recipe.ingredients:
            key = (orig_ing.name, orig_ing.unit)
            assert items_by_key[key] == orig_ing.quantity * 2

    def test_add_recipe_puts_correct_title(self, pizza_recipe):
        sl = ShoppingList()
        sl.add_recipe(pizza_recipe, 1)
        for _, title in sl._items:
            assert title == "Пицца"

    def test_add_recipe_raises_error(self, pizza_recipe):
        shopping_list = ShoppingList()
        with pytest.raises(ValueError) as e:
            shopping_list.add_recipe(pizza_recipe, -0.1)
        assert str(e.value) == "Количество порций должно быть положительным"

    def test_add_recipe_raises_error_on_zero_portions(self, pizza_recipe):
        sl = ShoppingList()
        with pytest.raises(ValueError):
            sl.add_recipe(pizza_recipe, 0)

    def test_remove_recipe(self, pizza_recipe, tea_recipe):
        sl = ShoppingList()
        sl.add_recipe(pizza_recipe, 1)
        sl.add_recipe(tea_recipe, 1)
        sl.remove_recipe("Пицца")
        titles = {t for _, t in sl._items}
        assert "Пицца" not in titles
        assert "Чай" in titles
        assert len(sl._items) == len(tea_recipe.ingredients)

    def test_remove_nonexistent_recipe(self, pizza_recipe):
        shopping_list = ShoppingList()
        shopping_list.add_recipe(pizza_recipe, 1)

        shopping_list.remove_recipe("Борщ")

        assert len(shopping_list._items) == len(pizza_recipe.ingredients)

        for (item_ing, item_title), expected_ing in zip(shopping_list._items, pizza_recipe.ingredients):
            assert item_title == "Пицца"
            assert item_ing == expected_ing
            assert item_ing.quantity == expected_ing.quantity

    def test_get_list_sums_same_ingredients(self, pizza_recipe, tea_recipe):
        sl = ShoppingList()
        sl.add_recipe(pizza_recipe, 1)
        sl.add_recipe(tea_recipe, 1)
        result = sl.get_list()
        result_by_key = {(i.name, i.unit): i.quantity for i in result}
        assert result_by_key[("Сахар", "ч. л.")] == 2.25

    def test_get_list_sorted_by_name(self, pizza_recipe, tea_recipe):
        sl = ShoppingList()
        sl.add_recipe(pizza_recipe, 1)
        sl.add_recipe(tea_recipe, 1)
        result = sl.get_list()
        assert result == sorted(result, key=lambda x: x.name)

    def test_add_lists_return_new_list_and_items_are_independent(self, pizza_recipe, tea_recipe):
        list1 = ShoppingList()
        list1.add_recipe(pizza_recipe, 1)

        list2 = ShoppingList()
        list2.add_recipe(tea_recipe, 1)

        combined_list = list1 + list2

        assert combined_list is not list1
        assert combined_list is not list2

        expected_items = list1._items + list2._items
        assert len(combined_list._items) == len(expected_items)

        for new_item, old_item in zip(combined_list._items, expected_items):
            new_ing, new_title = new_item
            old_ing, old_title = old_item

            assert new_title == old_title
            assert new_ing == old_ing
            assert new_ing.quantity == old_ing.quantity
            assert new_ing is not old_ing

