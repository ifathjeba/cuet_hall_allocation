from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Profile, RoomApplication, Hall,ROOM_TYPE_CHOICES
from .forms import SignUpForm, RoomApplicationForm,ProfileUpdateForm
from django.contrib.auth.models import User
from django.utils import timezone



# Home Page
def home(request):
    halls = Hall.objects.all()
    return render(request, 'allocation/home.html', {'halls': halls})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            # Update profile user_type
            user_type = form.cleaned_data.get('user_type', 'student')
            profile, created = Profile.objects.get_or_create(user=user)
            profile.user_type = user_type
            profile.save()

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
        if user:
            login(request, user)
            profile, _ = Profile.objects.get_or_create(user=user)
            if profile.user_type == 'authority':
                return redirect('authority_dashboard')
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'allocation/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')



def about_us(request):
    return render(request, 'allocation/about_us.html')

def contact_us(request):
    return render(request, 'allocation/contact_us.html')


# Room application without login
# Apply room
@login_required
def student_apply_room(request):
    if request.method == 'POST':
        form = RoomApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your application has been submitted and sent to authority!")
            return redirect('student_dashboard')
    else:
        form = RoomApplicationForm()
    return render(request, 'allocation/apply_room.html', {'form': form})

@login_required
def student_dashboard(request):
    applications = RoomApplication.objects.filter(email=request.user.email).order_by('-applied_at')
    return render(request, 'allocation/student_dashboard.html', {'applications': applications})

# Authority Dashboard
@login_required
def authority_dashboard(request):
    applications = RoomApplication.objects.filter(status='pending').order_by('applied_at')
    return render(request, 'allocation/authority_dashboard.html', {'applications': applications})



# Approve application (allocation logic)
@login_required
def approve_application(request, app_id):
    app = get_object_or_404(RoomApplication, id=app_id)
    # Check if room already allocated
    same_room_apps = RoomApplication.objects.filter(room_number=app.room_number, status='approved')
    
    if same_room_apps.exists():
        # Resolve conflict: prioritize higher year -> higher CGPA
        candidate = app
        for existing in same_room_apps:
            if int(candidate.year) > int(existing.year):
                continue  # candidate is higher year, ok
            elif int(candidate.year) == int(existing.year):
                if candidate.cgpa > existing.cgpa:
                    # swap allocation
                    existing.status = 'rejected'
                    existing.save()
                else:
                    candidate.status = 'rejected'
                    candidate.save()
                    messages.warning(request, f"{candidate.email} rejected due to lower CGPA for room {app.room_number}")
                    return redirect('authority_dashboard')
            else:
                candidate.status = 'rejected'
                candidate.save()
                messages.warning(request, f"{candidate.email} rejected due to lower year for room {app.room_number}")
                return redirect('authority_dashboard')

    app.status = 'approved'
    app.allocated_at = timezone.now()
    app.save()
    messages.success(request, f"{app.email} approved and allocated room {app.room_number}")
    return redirect('authority_dashboard')

# Reject application
@login_required
def reject_application(request, app_id):
    app = get_object_or_404(RoomApplication, id=app_id)
    app.status = 'rejected'
    app.save()
    messages.success(request, f"{app.email} application rejected")
    return redirect('authority_dashboard')



@login_required
def profile_update(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('student_dashboard')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'allocation/profile_update.html', {'form': form})




TOTAL_FLOORS = 5
ROOMS_PER_FLOOR = 24
SPECIAL_ROOMS = [0, 25]  # Example: room numbers reserved for guest, prayer, office, etc.

def available_rooms(request):
    room_type = request.GET.get('room_type', 'Standard Room (4 People)')
    
    # Generate all possible rooms
    all_rooms = []
    for floor in range(1, TOTAL_FLOORS + 1):
        for num in range(1, ROOMS_PER_FLOOR + 1):
            if num not in SPECIAL_ROOMS:
                all_rooms.append(f"{floor}{num:02d}")  # e.g., 101, 102, 510

    # Get already allocated rooms for this type
    occupied_rooms = RoomApplication.objects.filter(
        room_type=room_type,
        status='approved'
    ).values_list('room_number', flat=True)

    # Filter available rooms
    available_rooms = [r for r in all_rooms if r not in occupied_rooms]

    return JsonResponse({'available_rooms': available_rooms})
