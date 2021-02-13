from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('reader', 'post', 'content')
        readonly_fields = ('date',)

        widgets = {
            'reader': forms.HiddenInput(),
            'post': forms.HiddenInput()
        }
