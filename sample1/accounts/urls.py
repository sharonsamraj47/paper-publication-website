from django.urls import path
from . import views

urlpatterns = [
    path('', views.home2, name='home2'),
    path('home2/', views.home2, name='home2'),
    path('indexing/', views.indexing, name='indexing'),
    path('author/', views.author, name='author'),
    path('edit/', views.edit, name='edit'),
    path('scope/', views.scope, name='scope'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),  # Set home2 as the default route
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('admin-home/', views.admin_home, name='admin_home'),
    path('home/', views.home, name='home'),
    path('dashboard/', views.user_dashboard, name='dashboard'),  # New URL for user dashboard
    # path('home2/', views.home2, name='home2'),
    path('reviewer-login/', views.reviewer_login_view, name='reviewer_login'),  # New URL for reviewer login
    path('reviewer-home/', views.reviewer_home, name='reviewer_home'),  # New URL for reviewer home
    path('reviewer_comment/', views.reviewer_comment, name='reviewer_comment'),
    path('paper_submission/', views.paper_submission, name='paper_submission'),
]
