from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def administration(request):
    context = {"route": "administration_home"}
    return render(request, "administration.html", context)


@login_required
def administration_funk(request):
    context = {"route": "administration_funk"}
    return render(request, "administration_funk.html", context)


@login_required
def administration_pager(request):
    context = {"route": "administration_pager"}
    return render(request, "administration_pager.html", context)


'''
@login_required
def administration_user(request):
    context = {"route": "administration_user"}
    return render(request, "administration_nutzer.html", context)
'''


@login_required
def administration_user(request):
    # Holt alle Benutzer aus der Datenbank
    all_users = User.objects.all()
    print(("Die Nutzer: ", User.objects.all()))
    
    # Übergibt die Benutzer im "Context" an das HTML-Template
    context = {
        'all_users': all_users
    }
    return render(request, 'administration_nutzer.html', context)
