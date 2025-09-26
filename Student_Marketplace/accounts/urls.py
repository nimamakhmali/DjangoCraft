from django.urls import path
from .views import ping, signup, login_view, me, logout_view

urlpatterns = [
	path('ping/', ping, name='accounts-ping'),
	path('signup/', signup, name='accounts-signup'),
	path('login/', login_view, name='accounts-login'),
	path('logout/', logout_view, name='accounts-logout'),
	path('me/', me, name='accounts-me'),
]
