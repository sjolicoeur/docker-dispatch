from django.contrib import admin
from registry.dock.models import Token
# Register your models here.
class TokenAdmin(admin.ModelAdmin):
    raw_id_fields = [ 'owner']
    list_display = ["owner", "token"]
    search_fields = ["owner__name", "owner__id"]



admin.site.register(Token, TokenAdmin)