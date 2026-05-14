import django.shortcuts

__all__ = []


def home(request):
    template = 'homepage/simple.html'
    context = {}
    return django.shortcuts.render(request, template, context)