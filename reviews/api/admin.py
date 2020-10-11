from django.contrib import admin
from api.models import CustomUser, Company, Review, Reviewer


admin.site.register(CustomUser)
admin.site.register(Company)
admin.site.register(Review)
admin.site.register(Reviewer)
