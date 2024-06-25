#!/usr/bin/env python3
"""
    This module defines the CustomUserCreationForm
    and CustomAuthenticationForm classes.
"""
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import widgets


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        """
        Initializes the CustomUserCreationForm class.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None

        This method overrides the __init__ method of the UserCreationForm class.
        It calls the __init__ method of the parent class and
        updates the class attribute for each field in the form's fields dictionary.
        The class attribute is updated with CSS classes for styling the field's border,
        focus state, and other visual properties.

        Example:
            form = CustomUserCreationForm()
        """
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': '''
                            border border-green-300
                            focus:border-green-500 focus:ring
                            focus:ring-green-200
                            focus:ring-opacity-50 rounded-md shadow-sm
                        '''
            })


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        """
        Initializes the CustomAuthenticationForm class.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None

        This method overrides the __init__ method of the AuthenticationForm class.
        It calls the __init__ method of the parent class
        and updates the class attribute for each field in the form's fields dictionary.
        The class attribute is updated with CSS classes for styling the field's border,
        focus state, and other visual properties.
        """
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': '''
                            border border-green-300
                            focus:border-green-500 focus:ring
                            focus:ring-green-200
                            focus:ring-opacity-50 rounded-md shadow-sm
                        '''
            })