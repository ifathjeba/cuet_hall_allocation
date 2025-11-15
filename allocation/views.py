from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Application, Hall,RoomApplication
from .forms import SignUpForm, RoomApplicationForm
from django.contrib.auth.models import User

# Home Page
def home(request):
    halls = Hall.objects.all()
    return render(request, 'allocation/home.html', {'halls': halls})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create user
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            # Update profile user_type
            user_type = form.cleaned_data.get('user_type', 'student')
            profile = Profile.objects.get(user=user)
            profile.user_type = user_type
            profile.save()

            # Optionally mark authority users as staff (if you want admin site access)
            if user_type == 'authority':
                user.is_staff = True
                user.save()

            login(request, user)
            if profile.user_type == 'authority':
                return redirect('authority_dashboard')
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'allocation/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on profile.user_type
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                # Create profile if missing
                profile = Profile.objects.create(user=user, user_type='student')

            if profile.user_type == 'authority':
                return redirect('authority_dashboard')
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'allocation/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def about_us(request):
    return render(request, 'allocation/about_us.html')


def contact_us(request):
    if request.method == "POST":
        messages.success(request, 'Your message has been sent successfully!')
        return render(request, 'allocation/contact_us.html')
    return render(request, 'allocation/contact_us.html')


@login_required
def student_dashboard(request):
    # Only allow non-authority users
    if request.user.profile.user_type != 'student':
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('home')

    # Show this user's latest application (if any)
    latest_app = Application.objects.filter(student=request.user).order_by('-applied_at').first()
    return render(request, 'allocation/student_dashboard.html', {'latest_app': latest_app})


@login_required
def authority_dashboard(request):
    # Only allow authority users
    if request.user.profile.user_type != 'authority':
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('home')

    total_students = User.objects.filter(profile__user_type='student').count()
    pending_apps = Application.objects.filter(status='pending').order_by('-applied_at')
    approved_count = Application.objects.filter(status='approved').count()
    rejected_count = Application.objects.filter(status='rejected').count()

    context = {
        'total_students': total_students,
        'pending_applications': pending_apps.count(),
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'pending_apps': pending_apps,
    }
    return render(request, 'allocation/authority_dashboard.html', context)


@login_required
def approve_application(request, app_id):
    if request.user.profile.user_type != 'authority':
        messages.error(request, 'Not authorized.')
        return redirect('home')

    application = get_object_or_404(Application, id=app_id)
    application.status = 'approved'
    application.save()
    messages.success(request, f"Application for {application.student.username} approved.")
    return redirect('authority_dashboard')


@login_required
def reject_application(request, app_id):
    if request.user.profile.user_type != 'authority':
        messages.error(request, 'Not authorized.')
        return redirect('home')

    application = get_object_or_404(Application, id=app_id)
    application.status = 'rejected'
    application.save()
    messages.success(request, f"Application for {application.student.username} rejected.")
    return redirect('authority_dashboard')




def student_apply_room(request):
    # Prevent multiple applications
    existing_app = RoomApplication.objects.filter(student=request.user).exclude(status='rejected').first()
    if existing_app:
        return render(request, 'allocation/application_status.html', {'application': existing_app})

    if request.method == 'POST':
        form = RoomApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.save()
            messages.success(request, 'Application submitted successfully.')
            return redirect('student_dashboard')
        else:
            print(form.errors)  # debug line to see any validation errors
    else:
        form = RoomApplicationForm()

    return render(request, 'allocation/apply_room.html', {'form': form})
