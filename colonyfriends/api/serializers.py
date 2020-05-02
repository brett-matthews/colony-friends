import datetime
from rest_framework import serializers

from colonyfriends.models import Company, Food, Person, Tag


class CompanyModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class FoodModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = '__all__'


class CompanyInitSerializer(serializers.Serializer):

    index = serializers.IntegerField()
    company = serializers.CharField()

    def create(self, validated_data):

        object = Company.objects.create(
            id=validated_data['index'],
            name=validated_data['company']
        )
        return object


class PeopleInitSerializer(serializers.Serializer):

    index = serializers.IntegerField()
    guid = serializers.CharField()
    has_died = serializers.BooleanField()
    balance = serializers.CharField()
    picture = serializers.CharField()
    age = serializers.IntegerField()
    eyeColor = serializers.CharField()
    name = serializers.CharField()
    gender = serializers.CharField()
    company_id = serializers.IntegerField()
    email = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()
    about = serializers.CharField()
    registered = serializers.CharField()
    tags = serializers.ListField()
    favouriteFood = serializers.ListField()
    greeting = serializers.CharField()

    registered_datetime = None

    def validate_company_id(self, value):
        try:
            Company.objects.get(pk=value)
        except Company.DoesNotExist:
            # some people have a company that doesn't exist
            return None
        return value

    def validate_registered(self, value):
        # colon in timezone poorly supported, parse to datetime manually
        k = value.rfind(':')
        date_string = value[:k] + '' + value[k + 1:]
        try:
            self.registered_datetime = datetime.datetime.strptime(
                date_string, '%Y-%m-%dT%H:%M:%S %z'
            )
        except ValueError:
            raise serializers.ValidationError('Registered Invalid DateTime Input')

        return value

    def _map_person_model_data(self, validated_data):

        balance = validated_data.pop('balance').replace('$', '').replace(',', '')
        validated_data.pop('registered')

        return Person(
            id=validated_data['index'],
            eye_colour=validated_data['eyeColor'],
            balance=balance,
            registered=self.registered_datetime
        )

    def create(self, validated_data):

        tags = validated_data.pop('tags', [])
        foods = validated_data.pop('favouriteFood', [])

        person = self._map_person_model_data(validated_data=validated_data)

        for key, value in validated_data.items():
            setattr(person, key, value)

        person.save()

        for t in tags:
            Tag.objects.create(
                title=t,
                person=person
            )

        for f in foods:
            food, created = Food.objects.get_or_create(name=f)
            person.favourite_foods.add(food)

        person.save()

        return validated_data


class FriendInitSerializer(serializers.Serializer):

    index = serializers.IntegerField()

    def validate_index(self, value):
        try:
            Person.objects.get(id=value)
        except Person.DoesNotExist:
            raise serializers.ValidationError('Invalid Friend ID: {}'.format(value))
        return value


class PeopleInitFriendsSerializer(serializers.Serializer):

    index = serializers.IntegerField()
    friends = FriendInitSerializer(many=True)

    def create(self, validated_data):

        friends = validated_data.pop('friends', [])

        person = Person.objects.get(id=validated_data['index'])

        for friend in friends:
            if person.id == friend['index']:
                continue
            person.friends.add(friend['index'])

        person.save()
