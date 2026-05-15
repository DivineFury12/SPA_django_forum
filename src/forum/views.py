from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from forum.forms import ForumPost


@login_required
def forum(request):
    form = ForumPost()

    if request.method == 'POST':
        form = ForumPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('forum:forum')

    return render(request, 'forum/forum.html', {'form': form})