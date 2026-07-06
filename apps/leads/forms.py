from django import forms

from apps.leads.models import ContactLead


class ContactLeadForm(forms.ModelForm):
    consent_accepted = forms.BooleanField(
        required=True,
        error_messages={
            'required': 'Необходимо дать согласие на обработку персональных данных.',
        },
    )

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

    def clean_consent_accepted(self):
        if not self.cleaned_data.get('consent_accepted'):
            raise forms.ValidationError(
                'Необходимо дать согласие на обработку персональных данных.'
            )
        return True

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        digits = ''.join(c for c in phone if c.isdigit())
        if len(digits) < 10:
            raise forms.ValidationError('Введите корректный номер телефона.')
        return phone
