# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Permission(models.Model):
    name = models.CharField(max_length=64)
    allowed_url = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s <> %s' % (self.name, self.allowed_url)


class Role(models.Model):
    name = models.CharField(max_length=64,unique=True)
    permission = models.ManyToManyField(Permission, blank=True)
    memo = models.TextField(u"备注信息", max_length=200, blank=True)

    def __unicode__(self):
        return '%s' % (self.name)


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email or not username:
            raise ValueError('Users must have an email address and username')

        user = self.model(
            username=username,
            email=UserManager.normalize_email(email))
        user.set_password(password)
        user.save(self._db)

        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class UserInfo(AbstractBaseUser):
    username = models.CharField(max_length=64, unique=True, db_index=True)
    email = models.EmailField(max_length=255)
    nickname = models.CharField(max_length=64,blank=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.ManyToManyField(Role,blank=True,default=None)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return '%s:%s' % (self.username, self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        if self.is_active and self.is_superuser:
            return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __unicode__(self):
        return '%s:%s' % (self.username, self.email)

    @property
    def is_staff(self):
        return self.is_superuser
