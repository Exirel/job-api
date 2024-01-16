import json
import re

from django.conf import settings
from django.http import Http404
from django.shortcuts import render


from .forms import Suggestion

# Hideous hack to justify not having a database
# and store everything in memory instead
with open(settings.CATALOG_DIR / 'rome.json') as fd:
    ROME_DATA = json.loads(fd.read())


def get_suggestions(professions, search_terms):
    """Filter professions by the search terms."""
    regex = re.compile(re.escape(search_terms), re.IGNORECASE)
    try:
        regex = re.compile(search_terms, re.IGNORECASE)
    except:
        pass

    return [
        profession
        for profession in professions
        if regex.search(profession['label'])
    ]


def home(request):
    professions = ROME_DATA['professions']
    form = Suggestion()
    suggestions = []

    if request.method == 'POST':
        form = Suggestion(request.POST)

        if form.is_valid():
            search_terms = form.cleaned_data['search_terms']
            suggestions = get_suggestions(professions, search_terms)

    return render(request, 'home.html', context={
        'professions': professions,
        'search_form': form,
        'suggestions': suggestions,
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
