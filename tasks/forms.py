from django import forms


class TaskCreationForm(forms.Form):
    title = forms.CharField(label='タイトル', max_length=255)
    content = forms.CharField(label='内容', widget=forms.Textarea())
