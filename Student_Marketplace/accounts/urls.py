from django.urls import path
from .views import ping, signup, login_view, me, logout_view, password_change, send_verification, verify_email
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
	path('ping/', ping, name='accounts-ping'),
	path('signup/', signup, name='accounts-signup'),
	path('login/', login_view, name='accounts-login'),
	path('logout/', logout_view, name='accounts-logout'),
	path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('password-change/', password_change, name='accounts-password-change'),
	path('verify/send/', send_verification, name='accounts-verify-send'),
	path('verify/confirm/', verify_email, name='accounts-verify-confirm'),
	path('me/', me, name='accounts-me'),
]
