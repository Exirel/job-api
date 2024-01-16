import json

from django.conf import settings
from django.core.management.base import BaseCommand

from jobapi.catalog.utils import normalize


def transform_rome_professions(raw_rome: list[dict]) -> list[dict]:
    """Transform ROME 4.0 professions to a list of normalized professions."""
    return [
        {
            # mandatory fields
            'rome': rome['code'],
            'label': rome['libelle'],
            'normalized': normalize(rome['libelle']),

            # the next fields are optional
            'codeIsco': rome.get('codeIsco'),
            # apparently the API returns \\n instead of \n properly encoded
            # so we have to deal with this...
            'definition': rome.get('definition', '').replace('\\n', '\n'),
            'isStaffLevel': rome.get('emploiCadre') or False,
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
