from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Category, CodeSnippet, ErrorSolution, Tutorial, Demo, Comment


class CommentInline(GenericTabularInline):
    model = Comment
    extra = 0
    readonly_fields = ("user", "body", "created_at", "parent")
    can_delete = True

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    list_display = ("title", "language", "category", "created_at")
    list_filter = ("language", "category")
    search_fields = ("title", "description", "code")
    inlines = [CommentInline]


@admin.register(ErrorSolution)
class ErrorSolutionAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "description", "cause", "solution", "tags")
    inlines = [CommentInline]


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "content")
    inlines = [CommentInline]


@admin.register(Demo)
class DemoAdmin(admin.ModelAdmin):
    list_display = ("title", "video_url", "created_at")
    search_fields = ("title", "description")
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "content_type", "object_id", "created_at")
    list_filter = ("content_type", "created_at")
    search_fields = ("body", "user__username")
    readonly_fields = ("user", "content_type", "object_id", "body", "parent", "created_at")

    def has_add_permission(self, request):
        return False
