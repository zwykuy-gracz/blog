from django.contrib import admin
from .models import Post, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_date", "published_date")
    filter_horizontal = ("tags",)  # Allows easy management of tags in admin


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
