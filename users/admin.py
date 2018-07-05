from django.contrib import admin

# Register your models here.
from users.models import User,ActivationToken,PasswordRecoveryToken

# Register your models here.
admin.site.register(User)
admin.site.register(ActivationToken)
admin.site.register(PasswordRecoveryToken)

