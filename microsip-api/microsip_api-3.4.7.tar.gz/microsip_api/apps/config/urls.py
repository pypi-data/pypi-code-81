from django.urls import path
from microsip_api.apps.config import views

urlpatterns = (
    path('conexiones/',views.conexiones_View),
    path('conexion/<int:id>/', views.conexion_manageView),
    path('conexion/delete/<int:id>/', views.delete_conexion),
    path('conexion/', views.conexion_manageView),

    path('login/',views.ingresar),
    path('logout/', views.logoutUser),
    path('select_db/',views.select_db),    
)