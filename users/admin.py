from django.contrib import admin

# Register your models here.
from users.models import User,ActivationToken

# Register your models here.
admin.site.register(User)
admin.site.register(ActivationToken)

