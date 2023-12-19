from django import forms

class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data