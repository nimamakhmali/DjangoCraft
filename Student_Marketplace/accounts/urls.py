from django.urls import path
from .views import ping, signup, login_view, me, logout_view, password_change

urlpatterns = [
	path('ping/', ping, name='accounts-ping'),
	path('signup/', signup, name='accounts-signup'),
	path('login/', login_view, name='accounts-login'),
	path('logout/', logout_view, name='accounts-logout'),
	path('password-change/', password_change, name='accounts-password-change'),
	path('me/', me, name='accounts-me'),
]
