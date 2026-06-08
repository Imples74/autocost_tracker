from django.shortcuts import render
from .forms import CarForm

def home(request):
    return render(request, 'home.html')

from django.shortcuts import redirect

def car_create(request):

    if request.method == 'POST':

        form = CarForm(request.POST)

        if form.is_valid():

            car = form.save(commit=False)

            car.owner = request.user

            car.save()

            return redirect('/')

    else:

        form = CarForm()

    return render(
        request,
        'cars/car_form.html',
        {
            'form': form
        }
    )
