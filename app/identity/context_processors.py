from .models import Profile


def profile_context(request):
    """
    Add the Profile instance to the context for all templates.
    This ensures the navbar logo and other profile data are available everywhere.
    """
    try:
        profile = Profile.objects.first()
    except Exception:
        profile = None
    return {'profile': profile}
