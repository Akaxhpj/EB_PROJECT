
from django.contrib import admin
from django.urls import path
from billing import views  # Import views from your billing app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.homepage, name='home'),
    path('show/', views.show, name='show_bills'),
    path('update/', views.update, name='update_bill'),
    path('delete/', views.delete, name='delete_bill'),
    path('search/', views.search, name='search_bill'),
]
