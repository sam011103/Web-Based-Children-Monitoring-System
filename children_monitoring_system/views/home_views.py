from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required

# Create your views here.
def members(request):
  template = loader.get_template('myfirst.html')
  return HttpResponse(template.render())

@login_required
def home(request):
   return render(request, 'home.html')
