import datetime
from rest_framework import serializers

from colonyfriends.models import Company, Food, Person, Tags


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
    greeting = serializers.CharField()

    registered_datetime = None

    def validate_company_id(self, value):
        try:
            Company.objects.get(pk=value)
        except Company.DoesNotExist:
            raise serializers.ValidationError('Company Does Not Exist')
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

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        balance = validated_data.pop('balance').replace('$','').replace(',', '')
        validated_data.pop('registered')
        person = Person(
            id=validated_data['index'],
            eye_colour=validated_data['eyeColor'],
            balance=balance,
            registered=self.registered_datetime
        )
        for key, value in validated_data.items():
            setattr(person, key, value)

        person.save()

        for t in tags:
            Tags.objects.create(
                title=t,
                person=person
            )

        return person
