import json

from django.db import transaction
from django.db.utils import IntegrityError
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from colonyfriends.api.serializers import PeopleInitSerializer


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

        try:
            with transaction.atomic():

                with open(self.default_file, 'rb') as f:

                    try:
                        people_json = json.load(f)
                    except json.decoder.JSONDecodeError:
                        raise CommandError('Failure Input Invalid JSON')

                    serializer = PeopleInitSerializer(data=people_json, many=True)
                    if not serializer.is_valid():
                        raise CommandError('Invalid People Input: {}'.format(serializer.errors))
                    serializer.save()

        except (IntegrityError, KeyError) as ex:
            raise CommandError('Invalid People Input: {}'.format(ex))

        self.stdout.write(self.style.SUCCESS('Successfully Initialised People'))
