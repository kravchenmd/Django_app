from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Tag, Note
from .forms import TagForm, NoteForm


# Create your views here.
def main(request):
    notes = Note.objects.all()
    return render(request, 'noteapp/index.html', {"notes": notes})


def tag(request):
    if request.method == 'POST':
        try:
            form = TagForm(request.POST)
            form.save()
            return redirect(to='main')
        except ValueError as err:
            return render(request, 'noteapp/tag.html', {'form': TagForm(), 'error': err})
    return render(request, 'noteapp/tag.html', {'form': TagForm()})


def detail(request, note_id):
    note = Note.objects.get(pk=note_id)
    # extend object from DB to have access to all tags when rendering
    note.tag_list = ', '.join([str(name) for name in note.tags.all()])
    return render(request, 'noteapp/detail.html', {"note": note})


def note(request):
    tags = Tag.objects.all()
    if request.method == 'POST':
        try:
            list_tags = request.POST.getlist('tags')
            form = NoteForm(request.POST)
            new_note = form.save()
            chosen_tags = Tag.objects.filter(name__in=list_tags)  # WHERE name in
            for tag in chosen_tags.iterator():  # add m_to_m relationship
                new_note.tags.add(tag)
            return redirect(to='main')
        except ValueError as err:
            return render(request, 'noteapp/note.html', {"tags": tags, 'form': NoteForm(), 'error': err})
    return render(request, 'noteapp/note.html', {"tags": tags, 'form': NoteForm()})


def set_done(request, note_id):
    Note.objects.filter(pk=note_id).update(done=True)
    return redirect(to='main')


def delete_note(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.delete()
    return redirect(to='main')


def signup_user(request):
    return render(request, 'noteapp/signup.html', {'form': UserCreationForm()})


def login_user(request):
    return render(request, 'noteapp/login.html', {'form': AuthenticationForm()})
