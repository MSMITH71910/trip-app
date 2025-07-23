# trip/context_processors.py

def user_profile(request):
    """Add user profile to template context."""
    if request.user.is_authenticated:
        try:
            from .models import UserProfile
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            return {'user_profile': profile}
        except:
            return {'user_profile': None}
    return {'user_profile': None}