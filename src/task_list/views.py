from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from forms import UserForm, AddTaskForm
from models import Task


# Create your views here.
@login_required(login_url="/task_list/login")
def task_list(request):
    """
    Task list page.

    First checks whether user specified completed tasks are to be hidden via a
    query string paramter. Then creates a list of dicts of each user and their
    tasks which is handled by the template.

    """
    # First check if user specified completed searches to be hidden via query
    # string
    if request.GET.get("hide_completed") and int(request.GET
                                                 .get("hide_completed")):
        filter_completed = True
    else:
        filter_completed = False

    user_tasks = []
    # we want the currently logged in user and their tasks (if any) first
    if filter_completed:
        user_tasks.append({"user": request.user, "tasks": Task.objects
                           .filter(user=request.user, is_done=False)})
    else:
        user_tasks.append({"user": request.user, "tasks": Task.objects
                           .filter(user=request.user)})

    # Do same for rest of users!
    for user in User.objects.all():
        if user == request.user:
            continue

        if filter_completed:
            user_tasks.append({"user": user, "tasks": Task.objects
                               .filter(user=user, is_done=False, is_hidden=False)})
        else:
            user_tasks.append({"user": user, "tasks": Task.objects
                               .filter(user=user, is_hidden=False)})
    return render(request, "index.html", {"user_tasks": user_tasks,
                                          "filter_completed": filter_completed})


def about(request):
    """About page"""
    return render(request, "about.html")


def register_user(request):
    """User registration"""
    registered = False
    form_errors = None
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            form_errors = str(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, "register.html", {"user_form": user_form,
                                             "registered": registered,
                                             "form_errors": form_errors})


@login_required
def logout_user(request):
    """Logout user and redirect to index page"""
    logout(request)
    return HttpResponseRedirect("/task_list")


def login_user(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/task_list')
            else:
                return HttpResponse("You account is disabled, please contact "
                                    "the site administrator.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return render(request, "login_fail.html", status=401)

    else:
        return render(request, "login.html")


@login_required
def add_task(request):
    """Add a task"""
    task_added = False
    form_errors = None
    if request.method == "POST":
        task_form = AddTaskForm(data=request.POST)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.user = request.user
            task.save()
            task_added = True
        else:
            form_errors = str(task_form.errors)
    else:
        task_form = AddTaskForm()

    return render(request, "add_task.html", {"task_form": task_form,
                                             "task_added": task_added,
                                             "form_errors": form_errors})


@login_required
def edit_task(request, task_id):
    """
    Edit a task.

    If user is trying to edit someone else's task (should not be possible via
    UI) then send 403 error.

    """
    saved_task = Task.objects.get(id=task_id)
    # Avoid getting a SimpleLazyObject
    current_user = (request.user._wrapped if hasattr(request.user, '_wrapped')
                    else request.user)
    if current_user != saved_task.user:
        raise PermissionDenied
    task_edited = False
    form_errors = None
    if request.method == "POST":
        task_form = AddTaskForm(data=request.POST, instance=saved_task)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            # Get radio button values from POST data as we're re-using the
            # AddTaskForm
            task.is_done = True if int(request.POST["task_status"]) else False
            task.is_hidden = True if not int(request.POST["is_hidden"]) else False
            task.save()
            task_edited = True
        else:
            form_errors = str(task_form.errors)
    else:
        task_form = AddTaskForm()

    return render(request, "edit_task.html", {"task_form": task_form,
                                              "task_edited": task_edited,
                                              "task": saved_task,
                                              "form_errors": form_errors})


@login_required
def close_task(request, task_id):
    """
    Toggle the status of a Task (assuming user should be able to close
    others'tasks)
    """
    task = Task.objects.get(id=task_id)
    if not task.is_done:
        task.is_done = True
        task.status_changed_by = request.user
        task.save()
    return HttpResponseRedirect("/task_list")


@login_required
def delete_task(request, task_id):
    """Delete a task.

    If user is trying to delete someone else's task (should not be possible via
    UI) then send 403 error.
    """
    saved_task = Task.objects.get(id=task_id)
    # Avoid getting a SimpleLazyObject
    current_user = (request.user._wrapped if hasattr(request.user, '_wrapped')
                    else request.user)
    if current_user != saved_task.user:
        raise PermissionDenied
    saved_task.delete()
    return render(request, "delete_task.html")
