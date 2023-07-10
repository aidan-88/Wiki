from django.shortcuts import render
import markdown
from random import choice

from . import util

def convert_markdown_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert_markdown_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This page does not exist."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_markdown_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })
        else:
            allEntries = util.list_entries()
            suggestions = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    suggestions.append(entry)
            return render(request, "encyclopedia/search.html", {
                "suggestions": suggestions
            })

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else: 
        title = request.POST['title']
        content = request.POST['content']
        titleExists = util.get_entry(title)
        if titleExists is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = convert_markdown_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })
        
def edit(request): 
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert_markdown_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    
def random(request):
    allEntries = util.list_entries()
    random_entry = choice(allEntries)
    html_content = convert_markdown_html(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": html_content
    })