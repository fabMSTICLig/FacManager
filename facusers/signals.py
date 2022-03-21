from django.dispatch import receiver
from django_cas_ng.signals import cas_user_authenticated
from django.conf import settings

try:
    from django_auth_ldap.backend import LDAPBackend
    @receiver(cas_user_authenticated)
    def cas_user_authenticated_callback(sender, **kwargs):
        args = {}
        args.update(kwargs)
        if (hasattr(settings,'AUTH_LDAP_USER_SEARCH')):
            user = LDAPBackend().populate_user(args.get('user').username)
            if user is not None:
                user.save()
except ImportError as e:
    pass  # module doesn't exist, deal with it.
