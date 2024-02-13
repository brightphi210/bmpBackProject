from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.endpoint, name='endpoint'),
    path('api/user/', views.UserGetCreate.as_view(), name='user'),
        path('api/user/<str:pk>', views.UserGetUpdateDelete.as_view(), name="user_update"),

    path('api/userprofiles', views.UserProfileGet.as_view(), name="user_profile"),
    path('api/userprofile/update/<str:pk>', views.UserProfileGetUpdate.as_view(), name="user_profile_single"),
    
        # ==================== Email Verify ==================================
    path('api/confirm-email/<int:user_id>/', views.confirm_email, name="confirm_email"),

]