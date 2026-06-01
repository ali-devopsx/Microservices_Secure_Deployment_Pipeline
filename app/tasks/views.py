from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import get_object_or_404, redirect
from .models import Task
from .forms import TaskForm
from celery import shared_task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 12

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        context['status_counts'] = {
            'total': qs.count(),
            'pending': qs.filter(status='pending').count(),
            'in_progress': qs.filter(status='in_progress').count(),
            'completed': qs.filter(status='completed').count(),
            'cancelled': qs.filter(status='cancelled').count(),
            'high_priority': qs.filter(priority__in=['high', 'critical'], status__in=['pending', 'in_progress']).count(),
        }
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Task created successfully!')
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully!')
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Task deleted successfully!')
        return super().form_valid(form)


class TaskToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'], user=request.user)
        if task.status == 'completed':
            task.status = 'pending'
        else:
            task.status = 'completed'
        task.save()
        messages.success(request, f'Task "{task.title}" marked as {task.get_status_display().lower()}.')
        return redirect('tasks:task_list')



@shared_task
def test_task():
    print("Celery is working 🔥")
