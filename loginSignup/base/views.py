from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer


# -----------------------------
# Home Page (requires login)
# -----------------------------
@login_required
def home(request):
    return render(request, "home.html", {})


# -----------------------------
# Django Signup View (frontend form)
# -----------------------------
def authView(request):
    """Server-side signup using Django's UserCreationForm.

    This ensures passwords are validated and stored hashed (so authentication works).
    After successful signup the user is logged in and redirected to `home`.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optionally generate JWT tokens for API usage
            try:
                refresh = RefreshToken.for_user(user)
                # tokens available as str(refresh) and str(refresh.access_token)
            except Exception:
                refresh = None

            # Log the user in via session
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Account created and you are now logged in.')
                return redirect('base:home')
            else:
                messages.warning(request, 'Account created but automatic login failed. Please login manually.')
                return redirect('base:login')
        # form invalid: render with errors
        return render(request, 'registration/signup.html', {'form': form})

    # GET: show the Django signup form
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# -----------------------------
# Django Login View (Session-based)
# -----------------------------
def loginView(request):
    """
    Handles login using Django's AuthenticationForm.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")

            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('base:home')
        else:
            # Provide clearer handling for invalid logins.
            # If the supplied value isn't a username, try resolving it as an email
            # so users can enter either their username or email address.
            username_input = request.POST.get('username', '').strip()
            from django.contrib.auth import get_user_model
            UserModel = get_user_model()

            resolved_username = None
            if username_input:
                # Exact username match (case-sensitive depending on DB)
                if UserModel.objects.filter(username=username_input).exists():
                    resolved_username = username_input
                else:
                    # Try to resolve by email (case-insensitive)
                    user_by_email = UserModel.objects.filter(email__iexact=username_input).first()
                    if user_by_email:
                        resolved_username = user_by_email.username

            if username_input and resolved_username is None:
                # No user found matching username or email
                messages.error(request, 'No account found with that username or email.')
            else:
                # Username/email exists but credentials invalid
                messages.error(request, 'Invalid credentials — please check your username/email and password.')

            return render(request, 'registration/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})


def logoutView(request):
    """Log the user out and redirect to the login page.

    Accept GET and POST so clicking a logout link works in this demo.
    """
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been logged out.')
    return redirect('base:login')


# -----------------------------
# REST API Registration (JWT-based)
# -----------------------------
class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration (used if your frontend calls via fetch or axios).
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
