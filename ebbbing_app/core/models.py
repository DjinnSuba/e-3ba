from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.
class AppUserManager(BaseUserManager):
    def create_user(self, username, password=None, role='bidder', **extra_fields):
        user = self.model(username=username, role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        return self.create_user(username, password, role='admin', is_superuser=True, is_staff=True, **extra_fields)

###---------------###
### AppUser Model ###
class AppUser(AbstractUser):
    ROLE_CHOICES = (
        ('bidder', 'Bidder'),
        ('bac', 'BAC Member'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='bidder')
    cert_path = models.CharField(max_length=255, blank=True)
    key_path = models.CharField(max_length=255, blank=True)

###---------------###
### Project Model ###
class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, default='draft')  # e.g., draft, active, completed, closed
    bid_deadline = models.DateTimeField()
    created_by = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='projects_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

###---------------###
###   Bid Model   ###
class Bid(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(AppUser, on_delete=models.CASCADE, limit_choices_to={'role': 'bidder'})
    ipfs_tech_doc = models.CharField(max_length=255)  # IPFS hash
    ipfs_financial_doc = models.CharField(max_length=255)
    is_validated = models.BooleanField(default=False)  # after chaincode check
    submitted_at = models.DateTimeField(auto_now_add=True)

###---------------###
###   BAC Apprvl  ###
class BACApproval(models.Model):
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE)
    bac_member = models.ForeignKey(AppUser, on_delete=models.CASCADE, limit_choices_to={'role': 'bac'})
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(auto_now_add=True)

