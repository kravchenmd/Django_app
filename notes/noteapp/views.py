from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import Tag, Note, User
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
    if request.method == 'GET':
        return render(request, 'noteapp/signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                return redirect('login_user')
            except IntegrityError as err:
                return render(request, 'noteapp/signup.html',
                              {'form': UserCreationForm(), 'error': "This username already exists!"})
        else:
            return render(request, 'noteapp/signup.html',
                          {'form': UserCreationForm(), 'error': "Passwords don't match!"})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'noteapp/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'noteapp/login.html',
                          {'form': AuthenticationForm(), 'error': 'Check username or password!'})
        login(request, user)
        return redirect('main')


def logout_user(request):
    logout(request)
    return redirect('main')
