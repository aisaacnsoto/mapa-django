from django.shortcuts import render, redirect
from .models import Search
from .forms import SearchForm
import folium
import geocoder

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = SearchForm()
    address = Search.objects.all().last()
    location = geocoder.osm(address)
    lat = location.lat
    lng = location.lng
    country = location.country
    m = folium.Map(location=[19,-12], zoom_start=2)
    if lat == None or lng == None:
        if (address != None):
            address.delete()
    else:
        folium.Marker([lat,lng], tooltip="Haz click para ver más", popup=country).add_to(m)

    #Crear objeto mapa
    
    
    m = m._repr_html_()
    context = {
        'm': m,
        'form': form
    }
    return render(request, 'index.html', context)