from django.db import models


class Company(models.Model):

    name = models.CharField(max_length=20)

    class Meta:
        app_label = 'colonyfriends'


class Food(models.Model):

    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'colonyfriends'


class Person(models.Model):

    BLUE_EYE_COLOR = "blue"
    BROWN_EYE_COLOR = "brown"

    EYE_COLOR_CHOICES = (
        (BLUE_EYE_COLOR, "blue"),
        (BROWN_EYE_COLOR, "brown"),
    )

    FEMALE_GENDER = "female"
    MALE_GENDER = "male"

    GENDER_CHOICES = (
        (FEMALE_GENDER, "female"),
        (MALE_GENDER, "male"),
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


class Tags(models.Model):

    title = models.CharField(max_length=25)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='tags')

    class Meta:
        app_label = 'colonyfriends'
