"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/


"""
from django.urls import path
from . import views

urlpatterns = [
    path('automated_testing', views.flareis,name = 'flareis'),
    path('', views.index,name = 'index'),
]
