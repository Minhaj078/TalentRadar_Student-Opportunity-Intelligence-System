from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    domain = models.CharField(max_length=100)
    skills = models.TextField()
    hackathons = models.IntegerField(default=0)
    internships = models.IntegerField(default=0)
    research_papers = models.IntegerField(default=0)
    coding_rating = models.IntegerField(default=0)

    def calculate_score(self):
        return (
            self.hackathons * 10 +
            self.internships * 20 +
            self.research_papers * 25 +
            self.coding_rating / 100
        )

class Opportunity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    university = models.CharField(max_length=100, default="Unknown")
    domain = models.CharField(max_length=100)
    link = models.URLField()

    TYPE_CHOICES = [
        ('Hackathon', 'Hackathon'),
        ('Internship', 'Internship'),
        ('Research', 'Research'),
        ('Conference', 'Conference'),
        ('General', 'General'),
    ]

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='General'
    )

    def __str__(self):
        return f"{self.title} - {self.university}"


from django.contrib.auth.models import User

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opportunity = models.ForeignKey('Opportunity', on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} applied to {self.opportunity.title}"
