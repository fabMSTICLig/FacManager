from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

class Organization(models.Model):
    """
    Represent an Organization
    """
    name = models.CharField(max_length=30)
    contact = models.EmailField(max_length=100, null=True, blank=True)
    
    type = models.CharField(
        max_length=20,
        choices=settings.ORGANIZATION_TYPES,
        blank=True,
        default='',
        help_text='Type d\'affiliation',
    )


    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    organizations : [Organizations]
        Organizations to which the user belongs
    charter : bool
        True if the user have signed the charter
    rgpd_accept : date
        the date when the person has accepted the RGPD
    """
    organizations = models.ManyToManyField(
        Organization, blank=True, related_name="members")
    charter = models.BooleanField(default=False)
    rgpd_accept =  models.DateField(null=True, blank=True)
    def __str__(self):
        return self.username+"("+self.first_name+" "+self.last_name+")"


class Project(models.Model):
    """
    Represent a project
    ----------

    name : str
    descrition : str, optional
    referent : Person
        Referent of the project
    start_date : date
        starting date of the project
    end_date : date
        ending date of the project
    members : [User]
        member of this project, can be a person or an organization
    """
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300, null=True, blank=True)
    referent = models.ForeignKey(User, null=True, blank=True, related_name="project_referent",
                                 on_delete=models.SET_NULL)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    members = models.ManyToManyField(
        User, blank=True, related_name="projects")

    def __str__(self):
        return self.name
