import django.contrib.auth
import django.shortcuts

def register(request):
    template = 'users/register.html'
    if request.method == 'POST':
        form = django.contrib.auth.forms.UserCreationForm(
            request.POST,
        )
        if form.is_valid():
            form.save()
            return django.shortcuts.redirect('users:login')
    else:
        form = django.contrib.auth.forms.UserCreationForm()
    
    context = {
        'form': form,
    }
    
    return django.shortcuts.render(request, template, context)
    
    