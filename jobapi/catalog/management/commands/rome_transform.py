import json

from django.conf import settings
from django.core.management.base import BaseCommand


def transform_formacodes(raw_formacodes: list[dict]) -> list[dict]:
    """Transform ROME 4.0 ``formacodes`` into a list of trainings."""
    return [
        {
            'formacode': formacode['code'],
            'label': formacode['libelle'],
        }
        for formacode in raw_formacodes
    ]


def transform_rome_professions(raw_rome: list[dict]) -> list[dict]:
    """Transform ROME 4.0 professions to a list of normalized professions."""
    return [
        {
            'rome': rome['code'],
            'label': rome['libelle'],
            'formacodes': transform_formacodes(rome['formacodes']),
        }
        for rome in raw_rome
    ]


class Command(BaseCommand):
    help = "Import ROME professions from a downloaded JSON file."

    def handle(self, *args, **options):
        # get raw ROME 4.0 data
        filename = settings.CATALOG_DIR / 'raw_rome.json'
        with open(filename) as fd:
            raw_rome = json.loads(fd.read())

        # transform and save ROME 4.0 data
        filename = settings.CATALOG_DIR / 'rome.json'
        with open(filename, mode='w') as fd:
            professions = transform_rome_professions(raw_rome)
            fd.write(json.dumps({
                'professions': professions,
            }))
