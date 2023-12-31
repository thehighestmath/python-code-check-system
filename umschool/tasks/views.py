from django.shortcuts import render


def add_to_db_page(request):
    return render(request, 'tasks/add_to_db_page.html')
