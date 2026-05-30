"""
Identity Portfolio Models
This module defines the core data models for the digital identity portfolio.
Models include: Profile, Skills, Projects, and Timeline events.
All data is stored in the database and managed via Django admin.
"""

from django.db import models


class Profile(models.Model):
    """
    Single profile record for the portfolio owner.
    This is a singleton model - only one record should exist.
    Fields:
    - name: Full name of the portfolio owner
    - title: Professional title/tagline
    - bio_strong: Main biography/mission statement
    - contact_phrase: Introduction text for contact section
    - created_at: Timestamp of creation
    - updated_at: Timestamp of last update
    """
    name = models.CharField(
        max_length=255,
        default="Ali Mahmoud",
        help_text="Full name of the portfolio owner"
    )
    title = models.CharField(
        max_length=255,
        default="Penetration Tester & Automation Engineer",
        help_text="Professional title/role"
    )
    subtitle = models.CharField(
        max_length=255,
        default="IT Linux Engineer | DevOps Engineer | Cybersecurity Analyst",
        help_text="Typed subtitle line shown under the name"
    )
    bio_strong = models.TextField(
        default="I build calm, resilient systems that balance security and operations.",
        help_text="Short one-sentence bio for the hero section"
    )
    journey = models.TextField(
        blank=True,
        default="My path blends Linux engineering, DevOps automation, and practical cybersecurity.\nI help teams build secure infrastructure that feels smart and stable.",
        help_text="Short story about your journey, displayed in the About section"
    )
    email = models.EmailField(
        default="ali@example.com",
        help_text="Primary contact email address"
    )
    profile_image = models.ImageField(
        upload_to='profile/',
        max_length=255,
        null=True,
        blank=True,
        help_text="Personal photo for the hero section"
    )
    logo_text = models.CharField(
        max_length=50,
        default="AM",
        help_text="Logo/site name shown in navbar (e.g., 'AM' or 'Ali Mahmoud')"
    )
    contact_phrase = models.CharField(
        max_length=255,
        default="Let's connect by email:",
        help_text="Introduction text for contact section"
    )
    youtube_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="YouTube profile URL (optional)"
    )
    facebook_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Facebook profile URL (optional)"
    )
    github_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="GitHub profile URL (optional)"
    )
    linkedin_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="LinkedIn profile URL (optional)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return f"{self.name} - {self.title}"

    @property
    def journey_lines(self):
        """
        Return journey text split into short lines for the About section.
        """
        return [line.strip() for line in self.journey.splitlines() if line.strip()]

    def save(self, *args, **kwargs):
        """
        Override save to ensure only one Profile exists (singleton pattern).
        If a Profile exists, update it instead of creating a new one.
        """
        if not self.pk and Profile.objects.exists():
            # Update existing profile if trying to create another
            profile = Profile.objects.first()
            self.pk = profile.pk
        super().save(*args, **kwargs)


class Skill(models.Model):
    """
    Individual skill/technology model.
    Represents a skill with an associated FontAwesome icon.
    Fields:
    - name: Skill name (e.g., "Python", "Docker", "Linux")
    - icon_class: FontAwesome class for visual representation (e.g., "fa-python")
    - order: Display order in the skills section (lower = appears first)
    - created_at: Timestamp of creation
    - updated_at: Timestamp of last update
    """
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Name of the skill/technology"
    )
    icon_class = models.CharField(
        max_length=100,
        help_text="FontAwesome icon class (e.g., 'fa-python', 'fa-docker')"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return f"{self.name} ({self.icon_class})"


class Project(models.Model):
    """
    Portfolio project model.
    Represents a professional project with description, technologies, and optional image.
    Fields:
    - title: Project name/title
    - description: Detailed project description
    - tech_stack: Comma-separated list of technologies used
    - image: Optional project image/screenshot
    - link: Optional external link (GitHub, demo, etc.)
    - order: Display order in the projects section
    - created_at: Timestamp of creation
    - updated_at: Timestamp of last update
    """
    title = models.CharField(
        max_length=255,
        unique=True,
        help_text="Project title/name"
    )
    description = models.TextField(
        help_text="Detailed description of the project"
    )
    tech_stack = models.CharField(
        max_length=500,
        help_text="Comma-separated list of technologies (e.g., 'Python, Docker, Kubernetes')"
    )
    image = models.ImageField(
        upload_to='projects/',
        max_length=255,
        null=True,
        blank=True,
        help_text="Project image/screenshot (optional)"
    )
    summary = models.CharField(
        max_length=300,
        blank=True,
        help_text="Short project summary for the card, such as tech or results"
    )
    github_url = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        help_text="Link to the project's GitHub repository"
    )
    link = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        help_text="External link to project demo or details (optional)"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    @property
    def tech_tags(self):
        """
        Return a cleaned list of technologies from the comma-separated tech_stack field.
        This avoids using unsupported template filters like split.
        """
        return [tag.strip() for tag in self.tech_stack.split(',') if tag.strip()]

    def __str__(self):
        return self.title


class TimelineEvent(models.Model):
    """
    Timeline event model for the career/journey section.
    Represents a significant milestone or event in chronological order.
    Fields:
    - year: Year of the event
    - title: Event title/headline
    - description: Detailed description of the event
    - order: Display order in the timeline
    - created_at: Timestamp of creation
    - updated_at: Timestamp of last update
    """
    year = models.IntegerField(
        help_text="Year of the event (e.g., 2020, 2024)"
    )
    title = models.CharField(
        max_length=255,
        help_text="Event title/headline"
    )
    description = models.TextField(
        help_text="Detailed description of the event"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'year']
        verbose_name = "Timeline Event"
        verbose_name_plural = "Timeline Events"

    def __str__(self):
        return f"{self.year} - {self.title}"
