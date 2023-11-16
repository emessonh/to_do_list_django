from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def taskList(request):
    tasks_list = Task.objects.all().order_by('-created_at')

    paginator = Paginator(tasks_list, 5)
    page = request.GET.get('page')
    tasks = paginator.get_page(page)

    return render(request, 'tasks/list.html', {'tasks':tasks})

@login_required
def taskView(request, id):
    task = get_object_or_404(Task, pk=id)
    return render(request, 'tasks/task.html', {'task': task})

@login_required
def newTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.done = 'Doing'
            task.save()
            messages.success(request, 'Tarefa adicionada com sucesso')
            return redirect('/')
        
    else:
        form = TaskForm()
        return render(request, 'tasks/addtask.html', {'form': form})

@login_required 
def taskEdit(request, id):
    task = get_object_or_404(Task, pk=id)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task.save()
            messages.success(request, 'Tarefa editada com sucesso')
            return redirect('/')
        else:
            messages.error(request, 'Erro ao adicionar tarefa')
            return render(request, 'tasks/edittask.html', {'form': form, 'task':task})
    else:
        return render(request, 'tasks/edittask.html', {'form': form, 'task':task})

@login_required    
def taskDelete(request, id):
    task = get_object_or_404(Task, pk=id)
    task.delete()
    messages.success(request, 'Tarefa Excluída com sucesso')
    return redirect('/')

def helloWorld(request):
    return HttpResponse('Hello World!')
