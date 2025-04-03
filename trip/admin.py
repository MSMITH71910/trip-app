# trip/admin.py

from django.contrib import admin
from .models import Trip, ItineraryItem, BudgetItem, TripPhoto, Comment, UserProfile, Reaction

class ItineraryItemInline(admin.TabularInline):
    model = ItineraryItem
    extra = 1

class BudgetItemInline(admin.TabularInline):
    model = BudgetItem
    extra = 1

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'user')
    list_filter = ('start_date', 'end_date', 'user')
    search_fields = ('title', 'description')
    inlines = [ItineraryItemInline, BudgetItemInline]

@admin.register(ItineraryItem)
class ItineraryItemAdmin(admin.ModelAdmin):
    list_display = ('activity', 'location', 'date', 'time', 'trip')
    list_filter = ('date', 'trip')
    search_fields = ('activity', 'location')

@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'category', 'amount', 'trip')
    list_filter = ('category', 'trip')
    search_fields = ('description',)

@admin.register(TripPhoto)
class TripPhotoAdmin(admin.ModelAdmin):
    list_display = ('trip', 'caption', 'uploaded_at')
    list_filter = ('trip', 'uploaded_at')
    search_fields = ('caption',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('trip', 'user', 'text', 'created_at')
    list_filter = ('trip', 'user', 'created_at')
    search_fields = ('text',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'reaction_type', 'trip', 'photo', 'created_at')
    list_filter = ('reaction_type', 'created_at')
    search_fields = ('user__username',)