from django.urls import path
from . import views

urlpatterns = [
    path('',views.edit_items,name="edit_items" ),
    path('success/', views.success_view, name='success_view'),
]

