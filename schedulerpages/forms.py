from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from .models import Course
from .tables import CourseTable

class RegistrationForm(UserCreationForm):
    # class Meta:
    #     model = User
    #     fields = ['username', 'password1', 'password2']

    # def __init__(self, *args, **kwargs):
    #     super(RegistrationForm, self).__init__(*args,**kwargs)
    #     self.helper = FormHelper(self)
    #     self.helper.form_method = 'post'
    #     self.helper.add_input(Submit('submit', 'Register'))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
# class CourseForm(forms.ModelForm):
#     # purpose = forms.ChoiceField(choices=Purpose.choices)
    
#     class Meta:
#         model = Course
#         fields = ("Course Code", "Course, Year & Block", "Descriptive Title", "Lecture Units", "Laboratory Units" "Total Units", "Adviser" )
    