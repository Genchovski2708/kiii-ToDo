from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Task
from django.http import JsonResponse


def task_list(request):
    tasks = Task.objects.all()
    return render(request, "todo_app/task_list.html", {
        "tasks": tasks,
        "total_tasks": tasks.count(),
        "completed_tasks": tasks.filter(completed=True).count()
    })


def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        priority = request.POST.get("priority")
        due_date = request.POST.get("due_date")

        if title:
            Task.objects.create(
                title=title,
                description=description,
                priority=priority,
                due_date=due_date if due_date else None
            )
            messages.success(request, "Task added successfully!")
            return redirect("task_list")
        else:
            messages.error(request, "Title is required!")

    return render(request, "todo_app/add_task.html")


def toggle_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)
        task.completed = not task.completed
        task.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)


def delete_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect("task_list")
    return JsonResponse({"status": "error"}, status=400)