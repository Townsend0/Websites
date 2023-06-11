from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_all_posts, name = 'get_all_posts'),
    path('show-post/<int:post_id>/', views.show_post, name = 'show_post'),
    path('edit-post/<int:post_id>/', views.edit_post, name = 'edit_post'),
    path('delete-post/<int:post_id>/', views.delete_post, name = 'delete_post'),
    path('add-post/', views.add_post, name = 'add_post'),
    path('about/', views.about, name = 'about'),
    path('contact/', views.contact, name = 'contact'),
    path('login/', views.login_user, name = 'login'),
    path('logout/', views.logout_user, name = 'logout'),
    path('register/', views.register_user, name = 'register'),
]
