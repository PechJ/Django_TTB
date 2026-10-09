from django.shortcuts import render


def administration(request):
    context = {"route": "administration_home"}
    return render(request, "administration.html", context)


def administration_funk(request):
    context = {"route": "administration_funk"}
    return render(request, "administration_funk.html", context)


def administration_pager(request):
    context = {"route": "administration_pager"}
    return render(request, "administration_pager.html", context)