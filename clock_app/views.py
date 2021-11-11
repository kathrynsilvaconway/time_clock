from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def render_register(request):
    return render(request, 'register.html')

def process_reg(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        this_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash)
        request.session['id'] = this_user.id
        return redirect('/home')

def process_login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        one_user = User.objects.filter(email = request.POST['email'])
        request.session['id'] = one_user[0].id
        request.session['first_name'] = one_user[0].first_name
        return redirect('/home')
    return redirect('/')

def render_home(request):
    context = {
        'user': User.objects.get(id=request.session['id']),
    
    }
    return render(request, 'home.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')