from django.forms import ChoiceField, ModelMultipleChoiceField, MultipleChoiceField, MultipleHiddenInput, SelectMultiple, ValidationError

class EnvironmentsChoiceField(ModelMultipleChoiceField):

    def to_python(self, value):
        print(value)
        print(type(value))
        return super().to_python(value)
    
    def validate(self, value):
        print(value)
        print(type(value))
        return super().validate(value)


# class MultipleChoiceField(ChoiceField):
#     hidden_widget = MultipleHiddenInput
#     widget = SelectMultiple
#     default_error_messages = {
#         'invalid_choice': _('Select a valid choice. %(value)s is not one of the available choices.'),
#         'invalid_list': _('Enter a list of values.'),
#     }

#     def to_python(self, value):
#         if not value:
#             return []
#         elif not isinstance(value, (list, tuple)):
#             raise ValidationError(self.error_messages['invalid_list'], code='invalid_list')
#         return [str(val) for val in value]

#     def validate(self, value):
#         """Validate that the input is a list or tuple."""
#         if self.required and not value:
#             raise ValidationError(self.error_messages['required'], code='required')
#         # Validate that each value in the value list is in self.choices.
#         for val in value:
#             if not self.valid_value(val):
#                 raise ValidationError(
#                     self.error_messages['invalid_choice'],
#                     code='invalid_choice',
#                     params={'value': val},
#                 )

#     def has_changed(self, initial, data):
#         if self.disabled:
#             return False
#         if initial is None:
#             initial = []
#         if data is None:
#             data = []
#         if len(initial) != len(data):
#             return True
#         initial_set = {str(value) for value in initial}
#         data_set = {str(value) for value in data}
#         return data_set != initial_set