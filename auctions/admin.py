from django.contrib import admin
from .models import User, Listing, Bid, Comment, Category

# Custom admin classes
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'active', 'start_bid', 'current_bid')
    list_filter = ('active', 'creator', 'category')
    search_fields = ('title', 'description')

class BidAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'bid_amount')
    list_filter = ('user',)
    search_fields = ('listing__title',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'comment_text')
    search_fields = ('listing__title', 'comment_text')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register models with custom admin classes
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
