import json

from django.conf import settings
from django.http import Http404
from django.shortcuts import render

with open(settings.CATALOG_DIR / 'rome.json') as fd:
    ROME_DATA = json.loads(fd.read())


def home(request):
    return render(request, 'home.html', context={
        'professions': ROME_DATA['professions'],
    })


def rome_profession(request, code):
    try:
        profession = next(
            p
            for p in ROME_DATA['professions']
            if p['rome'] == code
        )
    except StopIteration:
        raise Http404

    return render(request, 'profession.html', context={
        'profession': profession,
    })
