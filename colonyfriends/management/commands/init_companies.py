import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from colonyfriends.api.serializers import CompanyInitSerializer


class Command(BaseCommand):

    help = 'Initialise Company Data From Structured JSON File'
    default_file =  settings.BASE_DIR + '/assets/companies.json'

    def add_arguments(self, parser):

        parser.add_argument(
            'file', type=str, nargs='?', default=self.default_file
        )

    def handle(self, *args, **options):

        if options['file']:
            self.default_file = options['file']

        with open(self.default_file, 'rb') as f:

            try:
                company_json = json.load(f)
            except json.decoder.JSONDecodeError:
                raise CommandError('Failure Input Invalid JSON')

            serializer = CompanyInitSerializer(data=company_json, many=True)

            if serializer.is_valid():
                serializer.save()
                self.stdout.write(self.style.SUCCESS('Successfully Initialised Companies'))
            else:
                raise CommandError('Failure: {}'.format(serializer.errors))

