from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, ProfileForm
from .models import StudentProfile, Opportunity
from .utils import real_scraper

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            StudentProfile.objects.create(user=user, domain="AI")
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

from django.shortcuts import render, redirect
from .models import Opportunity, StudentProfile

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile, created = StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={'domain': 'AI'}
    )

    selected_domain = request.GET.get('domain')

    if selected_domain:
        opportunities = Opportunity.objects.filter(domain=selected_domain)
    else:
        opportunities = Opportunity.objects.all()

    total_count = Opportunity.objects.count()
    total_universities = Opportunity.objects.values('university').distinct().count()

    return render(request, 'dashboard.html', {
        'opportunities': opportunities,
        'profile': profile,
        'total_count': total_count,
        'total_universities': total_universities
    })

def leaderboard(request):
    profiles = StudentProfile.objects.all()

    # Sort by score descending
    profiles = sorted(profiles, key=lambda p: p.calculate_score(), reverse=True)

    return render(request, 'leaderboard.html', {
        'profiles': profiles
    })


from .forms import ProfileForm

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

def auto_application(request):
    return render(request, 'coming_soon.html', {
        'title': 'Auto-Application System'
    })

def community(request):
    return render(request, 'coming_soon.html', {
        'title': 'Academic Community Platform'
    })


from .models import Application, Opportunity

def apply_opportunity(request, opp_id):
    if not request.user.is_authenticated:
        return redirect('login')

    opportunity = Opportunity.objects.get(id=opp_id)

    # Save application if not already applied
    Application.objects.get_or_create(
        user=request.user,
        opportunity=opportunity
    )

    # Auto increment profile stats based on domain
    profile = request.user.studentprofile

    application, created = Application.objects.get_or_create(
    user=request.user,
    opportunity=opportunity
)

    if created:
        # Only increase score first time
        if opportunity.domain == "AI":
            profile.hackathons += 1
        elif opportunity.domain == "Engineering":
            profile.internships += 1
        elif opportunity.domain == "Law":
            profile.research_papers += 1

        profile.save()

    return redirect(opportunity.link)

