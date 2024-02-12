from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.endpoint, name='endpoint'),
    path('api/user/', views.UserGetCreate.as_view(), name='user'),
    
        # ==================== Email Verify ==================================
    path('api/confirm-email/<int:user_id>/', views.confirm_email, name="confirm_email"),

]