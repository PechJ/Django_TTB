from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import PermissionDenied


class WhitelistAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username, password, **kwargs)
        
        if user is not None:
            if user.is_superuser:
                return user
                
            user_email = user.email.lower() if user.email else ""
            whitelist = [email.lower() for email in getattr(settings, 'EMAIL_WHITELIST', [])]
            
            print(f"DEBUG: Versuche E-Mail zu prüfen: '{user_email}'")
            print(f"DEBUG: Erlaubte Whitelist: {whitelist}")
            
            if user_email not in whitelist:
                print("DEBUG: E-Mail NICHT auf der Whitelist! Login wird blockiert.")
                # ValidationError wird von Djangos LoginView abgefangen und im Formular angezeigt
                raise ValidationError("Deine E-Mail-Adresse ist nicht für dieses System freigeschaltet.")
                
        return user
