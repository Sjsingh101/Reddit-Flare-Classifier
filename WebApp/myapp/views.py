from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import NameForm
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from . import flare

import json
# Create your views here.

def predict(post):
	return post

def index(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            result = flare.predict(url)
            print(result)
            form = NameForm()
            return render(request,"myapp/index.html",{'form':form,'value':"The flare of the post is : "+str(result)})
    
    form = NameForm()
    return render(request,"myapp/index.html",{'form':form})
	
@csrf_exempt
def flareis(request):
    if request.method == 'POST':
        #post = request.POST.get("rpost")
        myfile = request.FILES['upload_file']
        fs = FileSystemStorage()
        filename = fs.save('media/'+myfile.name, myfile)
        url = fs.url(filename)
        data=[]
        with open(url) as file1:
                data = file1.readlines()
        flares = flare.predict_all(data) 
        
        try:
            response = json.dumps(flares)
        except:
            response = json.dumps({ 'Error': 'Post could not be processed!'})
    return HttpResponse(response, content_type='text/json')
