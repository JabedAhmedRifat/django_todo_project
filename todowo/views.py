from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User 
from django.contrib.auth import login ,logout ,authenticate
# form.py theke import korse
from .form import TodoForm
# for currenttodos
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
    return render( request,'todowo/home.html')


@login_required
def currenttodos(request):
    return render( request,'todowo/currenttodos.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request,'todowo/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST ['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodos')
            except :
                return render(request,'todowo/signupuser.html', {'form':UserCreationForm(), 'error':'Username already exist'})
        else:
            return render(request,'todowo/signupuser.html', {'form':UserCreationForm(), 'error':'password didn\'t match'})




def loginuser(request):
    if request.method== 'GET':
        return render(request,'todowo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate (request,username=request.POST['username'],password=request.POST['password']) 
        if user is None:
            return render(request,'todowo/loginuser.html', {'form':AuthenticationForm(), 'error':'did not matched'})
        else:
            login(request,user)
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todowo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except:
            return render(request, 'todowo/createtodo.html', {'form':TodoForm() , 'error':'bad data inserted'})

    
@login_required
def currenttodos(request):
    todos= Todo.objects.filter(user=request.user, datecompleted__isnull = True)
    return render(request, 'todowo/currenttodos.html',{'todos':todos})


@login_required
def completedtodos(request):
    todo = Todo.objects.filter(user =request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'todowo/completedtodos.html', {'todo':todo})



@login_required
def viewtodo (request , todo_pk):
    todo = get_object_or_404(Todo , pk=todo_pk,user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance = todo)
        return render (request, 'todowo/viewtodo.html', {'todo':todo, 'form':form})
    
    else:
        form = TodoForm(request.POST, instance=todo)
        form.save()
        return redirect('currenttodos')

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo , pk=todo_pk, user=request.user)
    if request.method =='POST':
        todo.delete()
        return redirect('currenttodos')

