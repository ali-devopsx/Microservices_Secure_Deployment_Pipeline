from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=100, default="fa-code")
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class CodeSnippet(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    code = models.TextField()
    language = models.CharField(max_length=50, default="bash")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="snippets"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comments = GenericRelation("Comment", related_query_name="snippet")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Code Snippet"
        verbose_name_plural = "Code Snippets"

    def __str__(self):
        return self.title


class ErrorSolution(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(help_text="What was the error / what happened?")
    cause = models.TextField(help_text="What caused the error?")
    solution = models.TextField(help_text="Step-by-step fix")
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comments = GenericRelation("Comment", related_query_name="error")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Error & Solution"
        verbose_name_plural = "Errors & Solutions"

    def __str__(self):
        return self.title

    @property
    def tag_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]


class Tutorial(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(help_text="Markdown or HTML content")
    image = models.ImageField(
        upload_to="tutorials/", max_length=255, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comments = GenericRelation("Comment", related_query_name="tutorial")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Demo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_url = models.URLField(max_length=500, help_text="YouTube embed URL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comments = GenericRelation("Comment", related_query_name="demo")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_comments"
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user} on {self.content_object}"
