from django.db import models


class Company(models.Model):

    name = models.CharField(max_length=20)

    class Meta:
        app_label = 'colonyfriends'


class Food(models.Model):

    APPLE_TYPE = 'apple'
    BANANA_TYPE = 'banana'
    ORANGE_TYPE = 'orange'
    STRAWBERRY_TYPE = 'strawberry'

    FRUIT_CHOICES = (
        (APPLE_TYPE, 'apple'),
        (BANANA_TYPE, 'banana'),
        (ORANGE_TYPE, 'orange'),
        (STRAWBERRY_TYPE, 'strawberry'),
    )

    BEETROOT_TYPE = 'beetroot'
    CARROT_TYPE = 'carrot'
    CELERY_TYPE = 'celery'
    CUCUMBER_TYPE = 'cucumber'

    VEGETABLE_CHOICES = (
        (BEETROOT_TYPE, 'beetroot'),
        (CARROT_TYPE, 'carrot'),
        (CELERY_TYPE, 'celery'),
        (CUCUMBER_TYPE, 'cucumber'),
    )

    FOOD_CHOICES = FRUIT_CHOICES + VEGETABLE_CHOICES

    FRUIT_TYPE = 1
    VEGETABLE_TYPE = 2

    FOOD_TYPE_CHOICES = (
        (FRUIT_TYPE, 1),
        (VEGETABLE_TYPE, 2),
    )

    name = models.CharField(max_length=50, choices=FOOD_CHOICES)
    type = models.IntegerField(choices=FOOD_TYPE_CHOICES)

    class Meta:
        app_label = 'colonyfriends'

    def save(self, *args, **kwargs):

        if self.name in dict(self.FRUIT_CHOICES):
            self.type = self.FRUIT_TYPE

        if self.name in dict(self.VEGETABLE_CHOICES):
            self.type = self.VEGETABLE_TYPE

        super(Food, self).save(*args, **kwargs)


class Person(models.Model):

    BLUE_EYE_COLOR = 'blue'
    BROWN_EYE_COLOR = 'brown'

    EYE_COLOR_CHOICES = (
        (BLUE_EYE_COLOR, 'blue'),
        (BROWN_EYE_COLOR, 'brown'),
    )

    FEMALE_GENDER = 'female'
    MALE_GENDER = 'male'

    GENDER_CHOICES = (
        (FEMALE_GENDER, 'female'),
        (MALE_GENDER, 'male'),
    )

    guid = models.CharField(max_length=36)
    has_died = models.BooleanField()
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    picture = models.CharField(max_length=50)
    age = models.IntegerField()
    eye_colour = models.CharField(choices=EYE_COLOR_CHOICES, max_length=20)
    name = models.CharField(max_length=100)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    about = models.TextField()
    registered = models.DateTimeField()
    greeting = models.CharField(max_length=200)
    friends = models.ManyToManyField("self")
    favourite_foods = models.ManyToManyField(Food)

    class Meta:
        app_label = 'colonyfriends'


class Tag(models.Model):

    title = models.CharField(max_length=25)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='tags')

    class Meta:
        app_label = 'colonyfriends'
