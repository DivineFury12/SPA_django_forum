import django.forms

import forum.models


class ForumPost(django.forms.ModelForm):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = forum.models.Posts
        exclude = (
            'author',
            'created_at',
            'updated_at',
        )