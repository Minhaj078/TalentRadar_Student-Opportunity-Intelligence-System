from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, ProfileForm
from .models import StudentProfile, Opportunity, Application


# =========================
# AUTH VIEWS
# =========================

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            StudentProfile.objects.create(user=user, domain="General")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# =========================
# DASHBOARD
# =========================

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile, created = StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={'domain': 'General'}
    )

    type_filter = request.GET.get('type')

    opportunities = Opportunity.objects.all()

    if type_filter:
        opportunities = opportunities.filter(type=type_filter)

    opportunities = opportunities.order_by('-id')

    total_count = Opportunity.objects.count()
    total_universities = Opportunity.objects.values('organization').distinct().count()

    context = {
        'opportunities': opportunities,
        'profile': profile,
        'total_count': total_count,
        'total_universities': total_universities,
        'active_type': type_filter,
    }

    return render(request, 'dashboard.html', context)


# =========================
# LEADERBOARD
# =========================

def leaderboard(request):
    profiles = StudentProfile.objects.all()
    profiles = sorted(profiles, key=lambda p: p.calculate_score(), reverse=True)

    return render(request, 'leaderboard.html', {
        'profiles': profiles
    })


# =========================
# PROFILE
# =========================

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form})


# =========================
# COMING SOON MODULES
# =========================

def auto_application(request):
    return render(request, 'coming_soon.html', {
        'title': 'Auto-Application System'
    })


def community(request):
    return render(request, 'coming_soon.html', {
        'title': 'Academic Community Platform'
    })


# =========================
# APPLY OPPORTUNITY
# =========================

def apply_opportunity(request, opp_id):
    if not request.user.is_authenticated:
        return redirect('login')

    opportunity = get_object_or_404(Opportunity, id=opp_id)

    profile = request.user.studentprofile

    application, created = Application.objects.get_or_create(
        user=request.user,
        opportunity=opportunity
    )

    if created:
        # Update stats based on TYPE (not domain)
        if opportunity.type == "Hackathon":
            profile.hackathons += 1
        elif opportunity.type == "Internship":
            profile.internships += 1
        elif opportunity.type == "Research":
            profile.research_papers += 1

        profile.save()

    return redirect(opportunity.link)