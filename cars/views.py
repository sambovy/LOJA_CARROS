from django.shortcuts import render, redirect
from django.http import HttpResponse
from cars.models import Car
from cars.forms import CarForm
from cars.forms import CarModelForm
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# def car_views1(request):
#     # CODIGO HTML IMBUTIDO NO VIEWS

#     html = '''
#         <html>
#             <head>
#                 <title>Meus carros 1</title>
#             </head>
#             <body>
#                 <h1>Carros da Views</h1>
#                 <h3>Só Carro top</h3>
#             </body>
#         </html>
#     '''

#     return HttpResponse(html)

# def car_views2(request):
#     # CODIGO HTML INCLUSO NO TEMPLATES

#     return render(request, 'cars.html')

# def car_views3(request):
#     # CODIGO HTML INCLUSO NO TEMPLATES USANDO VARIAVEL

#     return render(
#         request, 
#         'cars2.html',
#         {'cars':{'model':'Astra 2.0'}}          
#                   )

# def car_views4(request):
#     # CODIGO HTML INCLUSO NO TEMPLATES USANDO ORM

#     cars = Car.objects.all() #SELECT * FROM CARS
#     #cars = Car.objects.filter(brand__name='Volkswagen') #SELECT * FROM CARS WHERE BRAND = 2
#     #cars = Car.objects.filter(model__contains='un')
#     print(cars) #somente para ver a lista no terminal

#     return render(
#         request, 
#         'cars3.html',
#         {'cars':cars}          
#     )

def car_views5(request):
    

    cars = Car.objects.all()
    search = request.GET.get('search')
    #http://127.0.0.1:8000/cars5/?search=gol

    if search:
        cars = Car.objects.filter(model__icontains=search).order_by('model')

    return render(
        request, 
        'cars3.html',
        {'cars':cars}          
    )

# def car_list(request):
    
#     cars = Car.objects.all()
#     search = request.GET.get('search')

#     if search:
#         cars = Car.objects.filter(model__icontains=search).order_by('model')

#     return render(
#         request, 
#         'carsN.html',
#         {'cars':cars}          
#     )

# def new_car_view(request):

#     if request.method == 'POST':
#         #new_car_form = CarForm(request.POST, request.FILES)
#         new_car_form = CarModelForm(request.POST, request.FILES)
#         print(new_car_form.data)
#         if new_car_form.is_valid():
#             new_car_form.save()
#             return redirect('car_list')
#         else:
#             pass
#     else:
#         new_car_form = CarForm()
#     return render(request, 'new_car.html', {'new_car_form': new_car_form})
    
    
class CarsView(View):
    
    def get(self, request):

        cars = Car.objects.all().order_by('model')
        search = request.GET.get('search')

        if search:
            cars = cars.filter(model__icontains=search)

        return render(
            request,
            'carsN.html',
            {'cars':cars}
        )
    

class CarsListView(ListView):
    model = Car # modelo (BD) de onde pegar os dados
    template_name = 'carsN.html' # a pagina template que irá mostrar
    context_object_name = 'cars' # Car.objects.all()

    def get_queryset(self):
        cars = super().get_queryset().order_by('model')
        # é igual a Car.objects.all().order_by('model')
        search = self.request.GET.get('search')
        if search:
            cars =  cars.filter(model__icontains=search)
        return cars
    
class NewCarView(View):

    def get(self, request):
        new_car_form = CarModelForm()
        return render(request, 'new_car.html', { 'new_car_form': new_car_form})
    
    def post(self, request):
         new_car_form = CarModelForm(request.POST, request.FILES)
         if new_car_form.is_valid():
             new_car_form.save()
             return redirect('cars')
         return render(request, 'new_car.html', {'new_car_form': new_car_form})


@method_decorator(login_required(login_url='login'), name='dispatch')    
class NewCarCreateView(CreateView):
    model = Car
    form_class = CarModelForm
    template_name = 'new_car.html'
    success_url = '/cars/'


class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'


@method_decorator(login_required(login_url='login'), name='dispatch')   
class CarUpdateView(UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = 'car_update.html'
    success_url = '/cars/'

    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required(login_url='login'), name='dispatch')   
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = '/cars/'
