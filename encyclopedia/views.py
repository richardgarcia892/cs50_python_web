from django.forms.forms import Form
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from markdown2 import Markdown
import random

from . import util


class NewEntryForm(forms.Form):
    entry_title = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control'})
    )
    entry_body = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={'class': 'form-control'})
    )


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_details(request, entry_title):
    markdown_text = Markdown()
    return render(request, "encyclopedia/entry.html", {
        "entry_title": entry_title,
        "entry_body": markdown_text.convert(util.get_entry(entry_title))
    })


def randon_entry(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return HttpResponseRedirect(reverse("details", args=[random_entry]))


def entry_search(request):
    entry_title = request.GET.get('entry_title')
    entries = util.list_entries()
    matching_entries = [
        entry for entry in entries if entry_title.lower() in entry.lower()]
    if len(matching_entries) == 1:
        matching_entry = matching_entries[0]
        return HttpResponseRedirect(reverse("details", args=[matching_entry]))
    else:
        return render(request, "encyclopedia/search.html", {
            "entry_title": entry_title,
            "entries": matching_entries
        })


def entry_add(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            form.clean()
            entry_title = form.cleaned_data['entry_title'].capitalize()
            entry_body = form.cleaned_data['entry_body'].capitalize()
            if util.get_entry(entry_title):
                return render(request, "encyclopedia/add.html", {
                    'form': form,
                    'error_message': f'Entry {entry_title} already exist'
                })
            else:
                util.save_entry(entry_title, entry_body)
                return HttpResponseRedirect(reverse("details", args=[entry_title]))
    else:
        form = NewEntryForm()
    return render(request, "encyclopedia/add.html", {'form': form})


def edit_entry(request, entry_title):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            form.clean()
            entry_title = form.cleaned_data['entry_title'].capitalize()
            entry_body = form.cleaned_data['entry_body'].capitalize()
            util.save_entry(entry_title, entry_body)
            return HttpResponseRedirect(reverse("details", args=[entry_title]))
    else:
        form = NewEntryForm(initial={
            'entry_title': entry_title,
            'entry_body': util.get_entry(entry_title.capitalize())
        })
    return render(request, "encyclopedia/edit.html", {'form': form})
