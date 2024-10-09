# from flask import jsonify

# class ValidationError(Exception):
  
#     def __init__(self, errors):
#         self.errors = errors

# def validate_login(data):
#     """Validate login request data."""
#     errors = {}
    
#     if not data.get('email'):
#         errors['email'] = "Email is required."
    
#     if not data.get('password'):
#         errors['password'] = "Password is required."
    
#     # You can add more validation rules here, such as email format validation

#     if errors:
#         raise ValidationError(errors)  # Raise custom exception with errors

def validate_required_fields(data, required_fields):
    """Utility to validate that all required fields are present in data."""
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"'{field}' is required"
    return True, None