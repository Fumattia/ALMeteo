from django.shortcuts import render

# Create your views here.
def alm(request):
    return render(request, 'ALM/ALM_paginaweb.html')