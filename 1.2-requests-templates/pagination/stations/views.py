import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from pagination.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице

    with open(BUS_STATION_CSV, encoding="utf-8", newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        all_stations = [row for row in reader]

    paginator = Paginator(all_stations, 10)
    page = paginator.get_page(request.GET.get('page', 1))

    context = {
        'bus_stations': page.object_list,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
