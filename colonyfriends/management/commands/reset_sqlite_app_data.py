from django.apps import apps
from django.core.management.base import BaseCommand

from django.db import connection


class Command(BaseCommand):

    help = 'Removes App Data and Resets SQLite Sequences'

    def handle(self, *args, **options):

        models = apps.get_models('colonyfriends')

        with connection.cursor() as cursor:

            for m in models:
                if m._meta.app_label == 'colonyfriends':
                    m.objects.all().delete()
                    table = m._meta.db_table
                    sqlstr = "delete from sqlite_sequence where name='{}';".format(table)
                    cursor.execute(sqlstr)
