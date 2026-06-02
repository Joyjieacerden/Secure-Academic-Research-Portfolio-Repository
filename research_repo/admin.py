from django.contrib import admin
from .models import User, Portfolio, Publication, AccessGrant, Authorship

admin.site.register(User)
admin.site.register(Portfolio)
admin.site.register(Publication)
admin.site.register(AccessGrant)
admin.site.register(Authorship)