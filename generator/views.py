from django.shortcuts import render
import secrets
import string
from zxcvbn import zxcvbn
from django.utils import timezone
from django.utils.translation import gettext as _


def generate_password(request):
    # Default context
    password = ''
    context = {
        'password': password,
        'length': 16,
        'uppercase': True,
        'lowercase': True,
        'digits': True,
        'symbols': True,
    }

    if request.method == 'POST':
        # Get form data
        length = int(request.POST.get('length', 16))
        uppercase = 'uppercase' in request.POST
        lowercase = 'lowercase' in request.POST
        digits = 'digits' in request.POST
        symbols = 'symbols' in request.POST

        # Build character set based on user preferences
        chars = ''
        if uppercase:
            chars += string.ascii_uppercase
        if lowercase:
            chars += string.ascii_lowercase
        if digits:
            chars += string.digits
        if symbols:
            chars += '!@#$%^&*()_-+=[]{}|;:,.<>?/'

        # If no character types are selected, return the default context
        if not chars:
            return render(request, 'generator/index.html', context)

        # Generate password
        password = ''.join(secrets.choice(chars) for _ in range(length))

        # Calculate password strength
        strength = zxcvbn(password)

        # Store password history in session (last 5 passwords)
        password_entry = {
            'password': password,
            'strength': strength['score'],
            'timestamp': timezone.now().isoformat(),  # Convert to string
            'expires': (timezone.now() + timezone.timedelta(hours=1)).isoformat()  # Convert to string
        }

        request.session.setdefault('password_history', [])
        request.session['password_history'] = [password_entry] + request.session['password_history'][:4]
        request.session.modified = True  # Ensure the session is saved

        # Update context with new data
        context.update({
            'password': password,
            'strength': strength['score'],
            'expiration_time': 60,  # minutes
            'length': length,
            'uppercase': uppercase,
            'lowercase': lowercase,
            'digits': digits,
            'symbols': symbols,
        })

    return render(request, 'generator/index.html', context)