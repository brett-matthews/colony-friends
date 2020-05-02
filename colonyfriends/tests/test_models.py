from django.test import TestCase

from colonyfriends.models import Food


class FoodModelTest(TestCase):

    def test_food_type_saves_correctly(self):

        food = Food.objects.create(
            name=Food.BANANA_TYPE
        )

        self.assertEqual(food.type, Food.FRUIT_TYPE)
