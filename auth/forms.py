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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs["class"] = "textinput form-control"
    #         field.widget.attrs["placeholder"] = field_name

    # def clean(self):
    #     cleaned_data = super().clean()
    #     print('---\ncleaned_data')
    #     print(cleaned_data)

    #     print('---\nfields')
    #     for field_name, field in self.fields.items():
    #         print(field_name)
    #         print(field)
    #         print(type(field))
    #         print(dir(field))

    #     print('---\nerrors')
    #     print(type(self.errors))
    #     print(self.errors)
    #     for k, v in self.errors.items():
    #         print(k)
    #         print(v)

    #     print('---\ncleaned_data items')
    #     for item in cleaned_data:
    #         print(item)
