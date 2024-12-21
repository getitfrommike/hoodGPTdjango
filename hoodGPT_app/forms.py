from django import forms

class OpenAIForm(forms.Form):
    prompt = forms.CharField(label='Prompt', max_length=1000, widget=forms.Textarea)