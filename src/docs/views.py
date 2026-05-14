import django.shortcuts
import django.contrib.auth.decorators
import django.views.decorators.http
import django.http
import forum.models
import forum.forms


def docs(request):
    posts = forum.models.Posts.raw.all_posts()
    form = forum.forms.ForumPost()
    return django.shortcuts.render(request, 'docs/documentation.html', {
        'posts': posts,
        'form': form,
    })


def can_modify(user, post_author_username):
    """Check if user is post author or admin."""
    return user.is_authenticated and (
        user.username == post_author_username or user.is_staff
    )


@django.contrib.auth.decorators.login_required
@django.views.decorators.http.require_POST
def post_create(request):
    form = forum.forms.ForumPost(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        form.save_m2m()
    return django.shortcuts.redirect('docs:docs')


@django.contrib.auth.decorators.login_required
def post_edit(request, post_id):
    post = django.shortcuts.get_object_or_404(forum.models.Posts, id=post_id)

    if not can_modify(request.user, post.author.username):
        return django.http.HttpResponseForbidden('Нет прав для редактирования.')

    form = forum.forms.ForumPost(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return django.shortcuts.redirect('docs:docs')

    return django.shortcuts.render(request, 'docs/documentation.html', {
        'posts': forum.models.Posts.raw.all_posts(),
        'form': forum.forms.ForumPost(),
        'edit_form': form,
        'edit_post_id': post_id,
    })


@django.contrib.auth.decorators.login_required
@django.views.decorators.http.require_POST
def post_delete(request, post_id):
    post = django.shortcuts.get_object_or_404(forum.models.Posts, id=post_id)

    if not can_modify(request.user, post.author.username):
        return django.http.HttpResponseForbidden('Нет прав для удаления.')

    forum.models.Posts.raw.delete_post(post_id)
    return django.shortcuts.redirect('docs:docs')