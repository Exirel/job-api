from django import forms


class Suggestion(forms.Form):
    search_terms = forms.CharField(label="Recherche", max_length=200)
    """User Input to look for ROME professions."""
