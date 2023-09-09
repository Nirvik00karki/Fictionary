from django.contrib import admin

from .models import Novel
from .models import Chapter
from .models import Payment
from .models import CustomUser

admin.site.register(Novel)
admin.site.register(Chapter)
admin.site.register(Payment)
admin.site.register(CustomUser)