# accounts/decorators.py

from django.contrib.auth.decorators import user_passes_test, login_required

def is_reviewer(user):
    return user.userprofile.is_reviewer

def reviewer_required(view_func):
    decorated_view_func = login_required(user_passes_test(is_reviewer)(view_func))
    return decorated_view_func
