import json

from django.db import IntegrityError, transaction
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from colonyfriends.api.serializers import PeopleInitSerializer
from colonyfriends.models import Food, Person


class Command(BaseCommand):

    help = 'Initialise People Data From Structured JSON File'
    default_file = settings.BASE_DIR + '/assets/people.json'

    def add_arguments(self, parser):

        parser.add_argument(
            'file', type=str, nargs='?', default=self.default_file
        )

    def handle(self, *args, **options):

        if options['file']:
            self.default_file = options['file']

        food_set = set()
        person_friends_and_food = {}

        try:
            with transaction.atomic():

                with open(self.default_file, 'rb') as f:

                    try:
                        people_json = json.load(f)
                    except json.decoder.JSONDecodeError:
                        raise CommandError('Failure Input Invalid JSON')

                    for p in people_json:
                        serializer = PeopleInitSerializer(data=p)
                        if not serializer.is_valid():
                            raise CommandError('Invalid Person Error:{} Data:{}'.format(serializer.errors, p))
                        serializer.save()

                        food_set.update(p['favouriteFood'])
                        person_friends_and_food[p['index']] = {
                            'friends': p['friends'],
                            'food': p['favouriteFood']
                        }

                for f in food_set:
                    Food.objects.create(
                        name=f
                    )

                food_queryset = Food.objects.all()

                for p in person_friends_and_food:
                    person = Person.objects.get(id=p)

                    for friend in person_friends_and_food[p]['friends']:
                        if friend['index'] == person.id:
                            continue
                        person.friends.add(friend['index'])

                    for food in person_friends_and_food[p]['food']:
                        person.favourite_foods.add(
                            food_queryset.filter(name=food).first()
                        )
                    person.save()

        except IntegrityError as ex:
            raise CommandError('Invalid People Input: {}'.format(ex))

        self.stdout.write(self.style.SUCCESS('Successfully Initialised People'))
