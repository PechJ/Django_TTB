from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.conf import settings


@login_required
def home(request):
    return render(request, "core/home.html")


@login_required
def login_redirect_view(request):
    # Superuser oder Administratoren landen im Admin-Dashboard
    if request.user.is_superuser or request.user.groups.filter(name='Administrator').exists():
        return redirect('home') # Passe den URL-Namen an dein Projekt an
    
    # Manager landen im Manager-Dashboard
    elif request.user.groups.filter(name='Manager').exists():
        return redirect('home')
    
    # Standard-Mitarbeiter landen im Employee-Dashboard
    else:
        return redirect('home')

class WhitelistedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Deine Firmen-E-Mail-Adresse")

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)


@login_required
def register_view(request):
    if request.method == 'POST':
        form = WhitelistedUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email').lower()
            whitelist = [e.lower() for e in getattr(settings, 'EMAIL_WHITELIST', [])]

            # Whitelist-Prüfung bei der Registrierung
            if email not in whitelist:
                messages.error(request, "Diese E-Mail-Adresse ist nicht für die Registrierung freigeschaltet!")
                return render(request, 'registration/register.html', {'form': form})

            # Wenn die E-Mail erlaubt ist, User speichern
            user = form.save()
            
            # Optional: Hier könntest du dem neuen User direkt eine Standard-Gruppe zuweisen
            # from django.contrib.auth.models import Group
            # default_group = Group.objects.get(name='Employee')
            # user.groups.add(default_group)

            messages.success(request, "Registrierung erfolgreich! Du kannst dich jetzt einloggen.")
            return redirect('login')
    else:
        form = WhitelistedUserCreationForm()
        
    return render(request, 'registration/register.html', {'form': form})
