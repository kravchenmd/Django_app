from django.shortcuts import render, redirect

from .models import Tag


# Create your views here.
def main(request):
    return render(request, 'noteapp/index.html', {})


def tag(request):
    if request.method == 'POST':
        name = request.POST['name']
        if name:
            tl = Tag(name=name)
            tl.save()
        return redirect(to='main')
    return render(request, 'noteapp/tag.html', {})
