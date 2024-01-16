import json
import os
import typing

import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

ACCESS_TOKEN_URL = (
    'https://entreprise.pole-emploi.fr'
    '/connexion/oauth2/access_token'
    '?realm=%2Fpartenaire'
)

AppId = typing.NewType('AppId', str)
AppSecret = typing.NewType('AppSecret', str)
AccessToken = typing.NewType('AccessToken', str)


def get_app_credentials() -> tuple[AppId, AppSecret]:
    """Retrieve Application ID and Secret from environement."""
    app_id = os.environ.get('FRANCE_TRAVAIL_ID')
    app_secret = os.environ.get('FRANCE_TRAVAIL_SECRET')

    if not app_id or not app_secret:
        raise CommandError('No APP ID or SECRET in env var.')

    return AppId(app_id), AppSecret(app_secret)


def get_access_token(
    app_id: AppId,
    app_secret: AppSecret,
) -> AccessToken:
    """Generate an access token granted by client credentials."""
    response = requests.post(ACCESS_TOKEN_URL, data={
        'grant_type': 'client_credentials',
        'client_id': app_id,
        'client_secret': app_secret,
        'scope': 'api_rome-metiersv1 nomenclatureRome',
    })

    if response.status_code != 200:
        raise CommandError('Unable to retrieve access token.')

    data = response.json()
    return AccessToken(data['access_token'])


def get_rome_professions(access_token: AccessToken) -> dict:
    """Request France Travail API to get ROME 4.0 set of professions."""
    url = (
        'https://api.pole-emploi.io'
        '/partenaire/rome-metiers/v1/metiers/metier'
    )
    params = {
        'champs': 'code,libelle,codeIsco,definition,emploiCadre',
    }
    headers = {"Authorization": f'Bearer {access_token}'}
    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise CommandError(
            'Unable to retrieve ROME professions:\n%s' % response.text
        )

    return response.json()


class Command(BaseCommand):
    help = "Download ROME professions from France Travail's API."

    def handle(self, *args, **options):
        # get access token
        app_id, app_secret = get_app_credentials()
        access_token = get_access_token(app_id, app_secret)

        # retrieve ROME 4.0 professions
        rome_professions = get_rome_professions(access_token)

        # store data into a json file
        filename = settings.CATALOG_DIR / 'raw_rome.json'
        with open(filename, 'w') as fd:
            fd.write(json.dumps(rome_professions))
