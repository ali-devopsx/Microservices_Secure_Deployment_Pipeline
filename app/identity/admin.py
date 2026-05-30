"""
Django Admin Configuration for Identity Portfolio
This module registers all models with the Django admin site for easy editing.
The admin interface allows the user to modify all portfolio data without touching code.
"""

from django.contrib import admin
from .models import Profile, Skill, Project, TimelineEvent


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for the Profile model.
    Displays all profile fields for editing.
    Since this is a singleton (only one record should exist), only one object can be edited.
    """
    list_display = ('name', 'title', 'updated_at')
    fields = ('name', 'title', 'subtitle', 'bio_strong', 'journey', 'email', 'profile_image', 'logo_text', 'contact_phrase', 'youtube_url', 'facebook_url', 'github_url', 'linkedin_url')
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        """
        Prevent adding more than one Profile record.
        If one already exists, users can only edit it.
        """
        return not Profile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deletion of the Profile record.
        This is the main portfolio identity and should never be deleted.
        """
        return False


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """
    Admin interface for the Skill model.
    Allows easy creation and editing of skills/technologies with FontAwesome icons.
    Skills are displayed in order based on the 'order' field.
    """
    list_display = ('name', 'icon_class', 'order')
    list_editable = ('order',)  # Allow inline editing of order
    search_fields = ('name',)
    fields = ('name', 'icon_class', 'order', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('order', 'name')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin interface for the Project model.
    Allows creation and editing of portfolio projects.
    Includes fields for title, description, technologies, image upload, and external links.
    Projects are displayed in order based on the 'order' field.
    """
    list_display = ('title', 'order', 'github_url', 'updated_at')
    list_editable = ('order',)  # Allow inline editing of order
    search_fields = ('title', 'description', 'tech_stack', 'summary')
    fields = (
        'title',
        'summary',
        'description',
        'tech_stack',
        'image',
        'github_url',
        'link',
        'order',
        'created_at',
        'updated_at'
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('order', 'title')


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    """
    Admin interface for the TimelineEvent model.
    Allows creation and editing of career timeline milestones.
    Events are displayed in order based on the 'order' field.
    """
    list_display = ('year', 'title', 'order')
    list_editable = ('order',)  # Allow inline editing of order
    search_fields = ('title', 'description')
    fields = ('year', 'title', 'description', 'order', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('order', 'year')
