from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from . import util
import markdown2

class newPageForm(forms.Form):
    title = forms.CharField(label="Page Title")
    content = forms.CharField(widget = forms.Textarea, label="Page Content (Formatted with Markdown)")

class editPageForm(forms.Form):
    editcontent = forms.CharField(widget = forms.Textarea, label="Page Content (Formatted with Markdown)")

class searchBar(forms.Form):
    userSearch = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

# show homepage function + return rand list entry
def index(request):

    if request.method == "POST":
        asearch = searchBar(request.POST)
        if asearch.is_valid():
            bsearch = asearch.cleaned_data["userSearch"]
            return HttpResponseRedirect(f"/wiki/search/{bsearch}")

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "rand": util.get_rand_entry_title(),
        "searchBar": searchBar
    })

def search(request, userSearch):
    if request.method == "POST":
        asearch = searchBar(request.POST)
        if asearch.is_valid():
            bsearch = asearch.cleaned_data["userSearch"]
            return HttpResponseRedirect(f"/wiki/search/{bsearch}")


    for i in util.list_entries():
        if userSearch == i:
            return HttpResponseRedirect(f"/wiki/{userSearch}")
    searchResults = list()
    for i in util.list_entries():
        if userSearch.lower() in i.lower():
            searchResults.append(i)
    if len(searchResults) == 0:
        return render(request, "encyclopedia/layout.html", {
            "pageTitle": "No Search Results",
            "text": f"No Search Results found for: {userSearch}",
            "rand": util.get_rand_entry_title(),
            "searchBar": searchBar
        })

    return render(request, "encyclopedia/search.html", {
        "entries": searchResults,
        "rand": util.get_rand_entry_title(),
        "userSearch": userSearch,
        "searchBar": searchBar
    })

#show entry from url function + return rand list entry
def showEntry(request, name):
    if request.method == "POST":
        asearch = searchBar(request.POST)
        if asearch.is_valid():
            bsearch = asearch.cleaned_data["userSearch"]
            return HttpResponseRedirect(f"/wiki/search/{bsearch}")

    #try to find the requested entry
    try:
        return render(request, "encyclopedia/layout.html", {
            "pageTitle": name,
            "text": markdown2.markdown(util.get_entry(name)),
            "rand": util.get_rand_entry_title(),
            "searchBar": searchBar,
            "name": name,
            "EditPage": "Edit Page"
        })

    #else, change the text to an error message
    except:
        return render(request, "encyclopedia/layout.html", {
            "pageTitle": "Error: Page not Found",
            "text": "Error: Page not Found",
            "searchBar": searchBar,
            "rand": util.get_rand_entry_title(),
        })

def editEntry(request, name):
    if request.method == "POST":
        asearch = searchBar(request.POST)
        if asearch.is_valid():
            bsearch = asearch.cleaned_data["userSearch"]
            return HttpResponseRedirect(f"/wiki/search/{bsearch}")

    if request.method == "POST":
        newEdits = editPageForm(request.POST)
        if newEdits.is_valid():
            edits = newEdits.cleaned_data["editcontent"]
            util.save_entry(name, edits)
            return HttpResponseRedirect(f"/wiki/{name}")

    return render(request, "encyclopedia/editEntry.html", {
        "rand": util.get_rand_entry_title(),
        "searchBar": searchBar,
        "name": name,
        "form": editPageForm(initial={'editcontent': f'{util.get_entry(name)}'}),
        })

def addEntry (request):
    if request.method == "POST":
        asearch = searchBar(request.POST)
        if asearch.is_valid():
            bsearch = asearch.cleaned_data["userSearch"]
            return HttpResponseRedirect(f"/wiki/search/{bsearch}")

    if request.method == "POST":
        aform = newPageForm(request.POST)
        if aform.is_valid():
            aentryTitle = aform.cleaned_data["title"]
            aentryContent = aform.cleaned_data["content"]

            for i in util.list_entries():
                 if i == aentryTitle:
                   return render(request, "encyclopedia/layout.html", {
                   "text": "Error: Page with title already exists",
                   "pageTitle": "Error: Page with title already exists",
                   "searchBar": searchBar,
                   "rand": util.get_rand_entry_title()
                   })

        util.save_entry(aentryTitle, aentryContent)
        return HttpResponseRedirect(f"/wiki/{aentryTitle}")

    return render(request, "encyclopedia/addEntry.html", {
        "rand": util.get_rand_entry_title(),
        "form": newPageForm(),
        "searchBar": searchBar,
    })
