from django.contrib import admin
from .models import User, Portfolio, Publication, ReviewerAssignment

admin.site.register(User)
admin.site.register(Portfolio)
admin.site.register(Publication)
admin.site.register(ReviewerAssignment)