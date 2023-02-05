from csv import reader

from django.core.management.base import BaseCommand

from services.models import Service, Status


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Service.objects.all().delete()
        Status.objects.all().delete()
        with open('data/services.csv', 'r', encoding='UTF-8') as services:
            for line in reader(services):
                if len(line) == 1:
                    Service.objects.get_or_create(
                        name=line[0],
                    )
        with open('data/statuses.csv', 'r', encoding='UTF-8') as statuses:
            for line in reader(statuses):
                if len(line) == 1:
                    Status.objects.get_or_create(
                        name=line[0],
                    )
