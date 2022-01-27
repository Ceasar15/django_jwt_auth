from django.shortcuts import render
from .models import User

# Create your views here.



def user_view():
    users = User.objects.all()
    context = {
        'users': users
    }
    return render('user.html', context)
