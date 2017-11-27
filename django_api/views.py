from django.shortcuts import render


def IndexView(request):
    return render(request, "rest_framework/index.html", {})