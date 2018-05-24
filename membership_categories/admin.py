from django.contrib import admin

# Register your models here.
from membership_categories.models import MembershipCategory

admin.site.register(MembershipCategory)