from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.contrib.auth.hashers import make_password


class RegistrationForm(forms.ModelForm):
    # 添加确认密码字段
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput(),  # 确保密码字段使用密码输入框
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # 检查两次输入的密码是否一致
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "The two password fields must match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
