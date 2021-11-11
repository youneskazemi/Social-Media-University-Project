from django import forms
from .models import Post, Comment


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image', 'body')


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image', 'body')


class AddCommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.TextInput(attrs={'class': 'form-control'}),
        }

