from django import forms


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
