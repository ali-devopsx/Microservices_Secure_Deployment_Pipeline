from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from .models import CodeSnippet, ErrorSolution, Tutorial, Demo, Comment, Category
from .forms import CommentForm


def snippet_list(request):
    snippets = CodeSnippet.objects.select_related("category").all()
    categories = Category.objects.all()
    return render(request, "blog/snippet_list.html", {
        "snippets": snippets,
        "categories": categories,
        "active_section": "snippets",
    })


def snippet_detail(request, pk):
    snippet = get_object_or_404(CodeSnippet.objects.select_related("category"), pk=pk)
    ct = ContentType.objects.get_for_model(CodeSnippet)
    comments = Comment.objects.filter(content_type=ct, object_id=pk, parent=None)
    form = CommentForm()
    return render(request, "blog/snippet_detail.html", {
        "snippet": snippet,
        "comments": comments,
        "form": form,
        "active_section": "snippets",
    })


def error_list(request):
    errors = ErrorSolution.objects.all()
    return render(request, "blog/error_list.html", {
        "errors": errors,
        "active_section": "errors",
    })


def error_detail(request, pk):
    error = get_object_or_404(ErrorSolution, pk=pk)
    ct = ContentType.objects.get_for_model(ErrorSolution)
    comments = Comment.objects.filter(content_type=ct, object_id=pk, parent=None)
    form = CommentForm()
    return render(request, "blog/error_detail.html", {
        "error": error,
        "comments": comments,
        "form": form,
        "active_section": "errors",
    })


def tutorial_list(request):
    tutorials = Tutorial.objects.all()
    return render(request, "blog/tutorial_list.html", {
        "tutorials": tutorials,
        "active_section": "tutorials",
    })


def tutorial_detail(request, pk):
    tutorial = get_object_or_404(Tutorial, pk=pk)
    ct = ContentType.objects.get_for_model(Tutorial)
    comments = Comment.objects.filter(content_type=ct, object_id=pk, parent=None)
    form = CommentForm()
    return render(request, "blog/tutorial_detail.html", {
        "tutorial": tutorial,
        "comments": comments,
        "form": form,
        "active_section": "tutorials",
    })


def demo_list(request):
    demos = Demo.objects.all()
    return render(request, "blog/demo_list.html", {
        "demos": demos,
        "active_section": "demos",
    })


def demo_detail(request, pk):
    demo = get_object_or_404(Demo, pk=pk)
    ct = ContentType.objects.get_for_model(Demo)
    comments = Comment.objects.filter(content_type=ct, object_id=pk, parent=None)
    form = CommentForm()
    return render(request, "blog/demo_detail.html", {
        "demo": demo,
        "comments": comments,
        "form": form,
        "active_section": "demos",
    })


@login_required
def post_comment(request, content_type_name, object_id):
    ct = ContentType.objects.get(model=content_type_name)
    obj = ct.get_object_for_this_type(pk=object_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = ct
            comment.object_id = object_id
            parent_id = request.POST.get("parent_id")
            if parent_id:
                comment.parent_id = parent_id
            comment.save()
            messages.success(request, "Comment posted!")
    return redirect(request.META.get("HTTP_REFERER", "/"))
