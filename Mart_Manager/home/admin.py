from django.contrib import admin
from django.contrib.sessions.models import Session

# Register your models here.
class sessionTable(admin.ModelAdmin):
    display_session = ['Session_Key', 'Session_Value', 'Session_Expiry']

admin.site.register(Session, sessionTable)