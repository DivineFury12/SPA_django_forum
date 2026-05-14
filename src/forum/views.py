from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from forum.forms import ForumPost


@login_required
def forum(request):
    form = ForumPost()

    if request.method == 'POST':
        form = ForumPost(request.POST, request.FILES)  # request.FILES for file upload
        if form.is_valid():
            post = form.save(commit=False)  # don't save yet
            post.author = request.user      # assign logged-in user as author
            post.save()
            form.save_m2m()                 # save ManyToMany (tags) separately
            return redirect('forum:forum')

    return render(request, 'forum/forum.html', {'form': form})