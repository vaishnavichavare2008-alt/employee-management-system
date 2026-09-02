from django.http import HttpResponse
from django.shortcuts import render
import datetime


def home(request):

    date = datetime.datetime.now()

    name = "NehaRuhatiya"

    list_of_programs = [
        'WAP to check even or odd',
        'WAP to check prime number',
        'WAP to print all prime numbers from 1 to 100',
        'WAP to print pascals triangle'
    ]

    student = {
        'student_name': "Rahul",
        'student_collage': "XYZ",
        'student_city': "LUCKNOW"
    }

    data = {
        'date': date,
        'name': name,
        'list_of_programs': list_of_programs,
        'student_data': student
    }

    return render(request, "home.html", data)


def about(request):
    return render(request, "about.html", {})


def services(request):
    return render(request, "services.html", {})