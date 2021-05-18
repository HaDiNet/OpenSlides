from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group as DjangoBuiltinGroup
from .users.models import User as OpenSlidesUser, Group as OpenSlidesGroup
from django_auth_ldap.backend import LDAPBackend


class OpenSlidesLDAPBackend(LDAPBackend):
    def get_user_model(self):
        return OpenSlidesUser

    def authenticate_ldap_user(self, ldap_user, password):
        user = super().authenticate_ldap_user(ldap_user, password)

        for builtin_group in user.groups.all():
            group = OpenSlidesGroup(group_ptr=builtin_group)
            group.__dict__.update(builtin_group.__dict__)
            group.save()

        user.save()

        return user;
