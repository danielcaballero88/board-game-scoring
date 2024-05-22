from django import forms

from .utils import get_user_by_email


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=100,
    )
    password = forms.CharField(
        label="Password",
        max_length=50,
    )
    remember_me = forms.BooleanField(required=False)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs["class"] = "textinput form-control"
    #         field.widget.attrs["placeholder"] = field_name

    # def clean(self):
    #     cleaned_data = super().clean()
    #     if self.errors:
    #         return cleaned_data

    #     email = cleaned_data["email"]
    #     user = get_user_by_email(email)
    #     if not user:
    #         self.add_error(None, "Wrong credentials.")

    #     return cleaned_data
