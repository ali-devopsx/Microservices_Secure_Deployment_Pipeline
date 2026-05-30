"""
Identity Portfolio Views
This module handles the rendering of the portfolio homepage and manages default data loading.
The home view retrieves all profile, skills, projects, and timeline data from the database.
"""

from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from .models import Profile, Skill, Project, TimelineEvent
from .utils import populate_default_data


class HomeView(TemplateView):
    """
    Main portfolio homepage view.
    This view retrieves all portfolio data from the database and renders it.
    The Intersection Observer JavaScript handles the scroll fade-in/fade-out effects.
    
    Context variables passed to template:
    - profile: Single Profile object with owner information
    - skills: All Skill objects ordered by order field
    - projects: All Project objects ordered by order field
    - timeline_events: All TimelineEvent objects ordered by order field
    """
    template_name = 'identity/home.html'

    def get_context_data(self, **kwargs):
        """
        Build the context dictionary with all portfolio data.
        Ensures default data exists before rendering.
        """
        context = super().get_context_data(**kwargs)
        
        # Populate default data if it doesn't exist
        # This is called on every page load to ensure data is available
        populate_default_data()

        # Retrieve all portfolio data from database
        try:
            # Get the single profile record (or use defaults if none exists)
            context['profile'] = Profile.objects.first()
        except Profile.DoesNotExist:
            context['profile'] = None

        # Get all skills ordered by the 'order' field
        context['skills'] = Skill.objects.all()

        # Get all projects ordered by the 'order' field and paginate (3 per page)
        all_projects = Project.objects.all()
        paginator = Paginator(all_projects, 3)  # Show 3 projects per page
        page_number = self.request.GET.get('page', 1)
        context['page_obj'] = paginator.get_page(page_number)

        # Get all timeline events ordered by the 'order' field
        context['timeline_events'] = TimelineEvent.objects.all()

        return context


# Function-based view alternative (if preferred over class-based view)
def home(request):
    """
    Alternative function-based view for the portfolio homepage.
    This can be used instead of HomeView if preferred.
    Retrieves all portfolio data and renders the template.
    """
    # Populate default data if it doesn't exist
    populate_default_data()

    # Retrieve all data
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    
    # Paginate projects (3 per page)
    all_projects = Project.objects.all()
    paginator = Paginator(all_projects, 4)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    timeline_events = TimelineEvent.objects.all()

    context = {
        'profile': profile,
        'skills': skills,
        'page_obj': page_obj,
        'timeline_events': timeline_events,
    }

    return render(request, 'identity/home.html', context)
