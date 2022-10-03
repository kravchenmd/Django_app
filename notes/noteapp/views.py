from django.shortcuts import render, redirect

from .models import Tag
from .forms import TagForm


# Create your views here.
def main(request):
    return render(request, 'noteapp/index.html', {})


def tag(request):
    if request.method == 'POST':
        try:
            form = TagForm(request.POST)
            form.save()
            return redirect(to='main')
        except ValueError as err:
            return render(request, 'noteapp/tag.html', {'form': TagForm(), 'error': err})
    return render(request, 'noteapp/tag.html', {'form': TagForm()})
