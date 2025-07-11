from django.contrib.auth.password_validation import validate_password as password_validator

def validate_password(self, value):
    password_validator(value)
    return value
