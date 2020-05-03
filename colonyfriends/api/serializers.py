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

        company = Company.objects.create(
            id=validated_data['index'],
            name=validated_data['company']
        )
        return company


class FriendInitSerializer(serializers.Serializer):

    index = serializers.IntegerField()


class FriendPostCreateSerializer(FriendInitSerializer):

    def validate_index(self, value):
        try:
            Person.objects.get(id=value)
        except Person.DoesNotExist:
            raise serializers.ValidationError('Invalid Friend ID: {}'.format(value))
        return value

    def save(self):
        if self.context['person'].id == self.validated_data['index']:
            return None
        self.context['person'].friends.add(self.validated_data['index'])
        return self.validated_data['index']

class PeopleInitListSerializer(serializers.ListSerializer):

    post_create_friends_serializers = []

    def _get_registered_date(self):
        return self.child.registered_datetime

    def _map_person_model_data(self, validated_data):

        balance = validated_data.pop('balance').replace('$', '').replace(',', '')
        validated_data.pop('registered')

        return Person(
            id=validated_data['index'],
            eye_colour=validated_data['eyeColor'],
            balance=balance,
            registered=self._get_registered_date()
        )

    def create(self, validated_data):

        created_people = []

        for item in validated_data:

            tags = item.pop('tags', [])
            foods = item.pop('favouriteFood', [])
            friends = item.pop('friends', [])

            person = self._map_person_model_data(validated_data=item)

            for key, value in item.items():
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

            for f in friends:
                serializer = FriendPostCreateSerializer(data=f, context={'person': person})
                if not serializer.is_valid():
                    self.post_create_friends_serializers.append(
                        FriendPostCreateSerializer(data=f, context={'person': person})
                    )
                    continue
                serializer.save()

            person.save()
            created_people.append(person)

        for s in self.post_create_friends_serializers:
            s.is_valid()
            s.save()

        return created_people


class PeopleInitSerializer(serializers.Serializer):

    class Meta:
        list_serializer_class = PeopleInitListSerializer

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
    friends = FriendInitSerializer(many=True)

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
