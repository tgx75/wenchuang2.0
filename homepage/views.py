from django.shortcuts import render, redirect, get_object_or_404


def homepage(request):
    """首页视图"""
    return render(request, "homepage.html")
