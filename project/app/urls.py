from django.urls import path
from app import views
urlpatterns = [
     path('', views.index, name='index'),
     path('about/', views.about, name='about'),
     path('contact/', views.contact, name='contact'),
     path('login/', views.handlelogin, name='handlelogin'),
     path('logout/', views.handlelogout, name='handlelogout'),
     path('signup/', views.handlesignup, name='handlesignup'),
     path('admin_login/', views.admin_login, name='admin_login'),
     path('admin_panel/', views.admin_panel, name='admin_panel'),
     path('admin_panel/add-user/', views.add_user, name='add_user'),
     path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
     path('admin_panel/delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
     path('admin_logout/', views.admin_logout,name='admin_logout'),

] 