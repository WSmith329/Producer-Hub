from __future__ import annotations
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Track(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    cover_art = models.ForeignKey('CovertArt', models.SET_NULL)

    creator = models.ForeignKey(User, models.SET_NULL, related_name='created_tracks')
    owners = models.ManyToManyField(User, related_name='owned_tracks')
    collaborators = models.ManyToManyField(User, 'track_contributions')
    collaborator_groups = models.ManyToManyField('CollaboratorGroup', 'track_group_contributions')


class TrackBranch(models.Model):
    track = models.ForeignKey('Track', models.CASCADE)

    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    audio_file = models.FileField()
    project_file = models.FileField()

    started_by = models.ForeignKey(User, models.SET_NULL)
    started_on = models.DateTimeField(auto_now_add=True)

    is_default = models.BooleanField()


class TrackCommit(models.Model):
    branch = models.ForeignKey('TrackBranch', models.CASCADE)

    description = models.TextField(blank=True)

    audio_file = models.FileField()
    project_file = models.FileField()

    submitted_by = models.ForeignKey(User, models.SET_NULL)
    submitted_on = models.DateTimeField(auto_now_add=True)

    is_accepted = models.BooleanField()


class BranchRequest(models.Model):
    track = models.ForeignKey('Track', models.CASCADE)
    branch = models.OneToOneField('TrackBranch', models.CASCADE)

    class RequestStatus(models.TextChoices):
        PENDING = 'PE', _('Pending')
        ACCEPTED = 'PE', _('Accepted')
        REJECTED = 'RE', _('Rejected')
    status = models.CharField(max_length=5, choices=RequestStatus, default=RequestStatus.PENDING)


class CovertArt(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    image_file = models.FileField()
    uploaded_by = models.ForeignKey(User, models.SET_NULL, related_name='uploaded_cover_arts')


class Collection(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    cover_art = models.ForeignKey('CovertArt', models.SET_NULL)

    creator = models.ForeignKey(User, models.SET_NULL, related_name='created_collections')
    owners = models.ManyToManyField(User, related_name='owned_collections')
    collaborators = models.ManyToManyField(User, related_name='collection_contributions')
    collaborator_groups = models.ManyToManyField('CollaboratorGroup', 'collection_group_contributions')


class CollaboratorGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    collaborators = models.ManyToManyField(User)

    creator = models.ForeignKey(User, models.SET_NULL, related_name='created_tracks')
    owners = models.ManyToManyField(User, related_name='owned_tracks')
