from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

SubAdmin = get_user_model()

class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    confirm_password = forms.CharField(widget = forms.PasswordInput)

    class Meta:
        model = SubAdmin
        fields = ['email', 'first_name', 'last_name', 'phone_number']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password is not None and password != confirm_password:
            self.add_error("confirm_password", "Your passwords must match")
        return cleaned_data

    def save(self, commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = SubAdmin
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'password', 'active', 'staff']

    def clean_password(self):
        return self.initial['password']