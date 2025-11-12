from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Tailwind styling to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-[#54C4C7] focus:ring-2 focus:ring-[#54C4C7]/20 transition-colors',
                'placeholder': field.label,
            })
        
        # Add specific styling for password fields
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-[#54C4C7] focus:ring-2 focus:ring-[#54C4C7]/20 transition-colors'
        })
        self.fields['password_confirm'].widget.attrs.update({
            'placeholder': 'Confirm Password',
            'class': 'w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-[#54C4C7] focus:ring-2 focus:ring-[#54C4C7]/20 transition-colors'
        })

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
