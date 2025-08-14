from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


class User(AbstractUser):
    pass

class Project(models.Model):
    pass

class ProjectMember(models.Model):
    pass

class Task(models.Model):
    pass

class TaskAttachment(models.Model):
    pass

class TaskComment(models.Model):
    pass

class Team(models.Model):
    pass

class TeamMember(models.Model):
    pass

