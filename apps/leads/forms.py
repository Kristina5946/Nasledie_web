from django import forms

from apps.leads.models import ContactLead


class ContactLeadForm(forms.ModelForm):
    class Meta:
        model = ContactLead
        fields = ['name', 'phone', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ваше имя',
                'autocomplete': 'name',
                'class': 'form-input',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Номер телефона',
                'autocomplete': 'tel',
                'type': 'tel',
                'class': 'form-input',
            }),
            'comment': forms.Textarea(attrs={
                'placeholder': 'Ваш комментарий или вопрос (необязательно)',
                'rows': 3,
                'class': 'form-input form-textarea',
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        digits = ''.join(c for c in phone if c.isdigit())
        if len(digits) < 10:
            raise forms.ValidationError('Введите корректный номер телефона.')
        return phone
