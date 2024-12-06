from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
from django.http import Http404
from rest_framework import viewsets
from .forms import CreateUserForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .serializers import TyphoidSerializer
from healthcare.models import Ugonjwa
from .models import Typhoid, Illness, Sign, Merchandise, Image, User, Doctor, Appointment, Department,ContactMessage
from .forms import TyphoidForm, TyphoidPhotoFormSet, IllnessForm, SignForm, SearchForm, MerchandiseForm, ImageForm, AppointmentForm, ContactMessageForm
from .mpesa import AccessToken, Password
from django.http import HttpResponse
import requests
import random
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

# function -based views(normal)
@login_required
def index(request):
    departments=Department.objects.all()
    doctors=Doctor.objects.all()
    return render(request,'index.html', {"departments":departments, "doctors":doctors})

def register(request):
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
           
        
    else:
        form=CreateUserForm()
        
    return render(request, 'register.html', {'form':form})
           

def create_ugonjwa(request): 
    if request.method == 'POST': 
        form = TyphoidForm(request.POST) 
        formset = TyphoidPhotoFormSet(request.POST, request.FILES) 
        if form.is_valid() and formset.is_valid(): 
            typhoid = form.save() 
            for form in formset: 
                photo = form.save(commit=False) 
                photo.typhoid = typhoid
                photo.save() 
            return redirect('create_ugonjwa') # Redirect to a success page or the detail view
    else: 
        form = TyphoidForm() 
        formset = TyphoidPhotoFormSet() 

    return render(request, 'create_ugonjwa.html', {'form': form, 'formset': formset})

def tengeneza_illness(request):
    context={}

    if request.method=='POST':
        if 'save' in request.POST:
            pk=request.POST.get('save')
            if pk:
                illness=get_object_or_404(Illness, pk=pk)
                illness_form=IllnessForm(request.POST,instance=illness)
                sign_form=SignForm(request.POST, request.FILES)
            
            else:
                illness_form= IllnessForm(request.POST)
                sign_form=(request.POST, request.FILES)
            
            if illness_form.is_valid() and sign_form.is_valid():
                illness=illness_form.save()

                if 'symptoms' in request.FILES:
                    for uploaded_file in request.FILES.getlist('symptoms'):
                        Sign.objects.create(illness=illness, pic=uploaded_file)

                return redirect('tengeneza_illness')
            
        elif 'delete' in request.POST:
            pk=request.POST.get('delete')
            illness=get_object_or_404(Illness, pk=pk)
            illness.delete()
            return redirect('tengeneza_illness')
        
        elif 'edit' in request.POST:
            pk= request.POST.get('edit')
            illness=get_object_or_404(Illness,pk=pk)
            illness_form=IllnessForm(instance=illness)
            sign_form=SignForm()
        
        else:
            illness_form=IllnessForm()
            sign_form=SignForm()
    
    else:
        illness_form=IllnessForm()
        sign_form=SignForm()
    
    illnesses=Illness.objects.all()
    context['illness_form'] = illness_form
    context['sign_form'] = sign_form
    context['illnesses'] =illnesses

    return render(request, 'tengeneza_illness.html', context)


def shop_now(request):
    merchandise_list=Merchandise.objects.all()
    context={
        "merchandise_list": merchandise_list,
    }
    return render(request,'shop_now.html', context)

def pay(request, merchandise_id):
    merchandise=get_object_or_404(Merchandise, id=merchandise_id)
    return render(request, 'pay.html',{'merchandise':merchandise})

def appointment_view(request):
    if request.method == 'POST': 
        form=AppointmentForm(request.POST)
        if form.is_valid():
            appointment=form.save()

            send_mail(
                'Appointment Request Confirmation',
                f'Hello {form.cleaned_data["name"]},\n\n'
                f'Your appointment with {form.cleaned_data["doctor"]} on {form.cleaned_data["date"]} has been confirmed.',
                settings.DEFAULT_FROM_EMAIL,
                [form.cleaned_data["email"]],
                fail_silently=False,
            )

            messages.success(request, 'Your appointment request has been successfully sent. Thank you!')

            return redirect('index')
    
    else:
        form=AppointmentForm()
    
    return render(request,'index.html',{"form":form})

def stk(request):
    if request.method=='POST':
        phone=request.POST['phone']
        amount=int(float(request.POST['amount']))
        access_token=AccessToken.access_token
        api_url='https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        header={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
        request= {    
             "BusinessShortCode": Password.shortcode,    
             "Password": Password.decoded_password,
             "Timestamp":Password.timestamp,    
             "TransactionType": "CustomerPayBillOnline",    
             "Amount": amount,    
             "PartyA":phone,    
             "PartyB":Password.shortcode,    
             "PhoneNumber":phone,    
             "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa",    
             "AccountReference":"Nitibu Solutions",    
             "TransactionDesc":"Payment for kicks"
             }
        print(request)
    response= requests.post(api_url, json=request, headers=header)
    print(response)
    return HttpResponse('success')



def tengeneza_product(request):
    context={}

    if request.method=='POST':
        if 'save' in request.POST:
            pk=request.POST.get('save')
            if pk:
                merchandise=get_object_or_404(Merchandise, pk=pk)
                merchandise_form=MerchandiseForm(request.POST,instance=merchandise)
                image_form=ImageForm(request.POST, request.FILES)
            
            else:
                merchandise_form= MerchandiseForm(request.POST)
                image_form=(request.POST, request.FILES)
            
            if merchandise_form.is_valid() and image_form.is_valid():
                merchandise=merchandise_form.save()

                if 'images' in request.FILES:
                    for uploaded_file in request.FILES.getlist('images'):
                        Image.objects.create(merchandise=merchandise, Image=uploaded_file)

                return redirect('tengeneza_product')
            
        elif 'delete' in request.POST:
            pk=request.POST.get('delete')
            merchandise=get_object_or_404(Merchandise, pk=pk)
            merchandise.delete()
            return redirect('tengeneza_product')
        
        elif 'edit' in request.POST:
            pk= request.POST.get('edit')
            merchandise=get_object_or_404(Merchandise,pk=pk)
            merchandise_form= MerchandiseForm(instance=merchandise)
            image_form=ImageForm()
        
        else:
            merchandise_form=MerchandiseForm()
            image_form=ImageForm()
    
    else:
        merchandise_form=MerchandiseForm()
        image_form=ImageForm()
    
    merchandises=Merchandise.objects.all()
    context['merchandise_form'] = merchandise_form
    context['image_form'] = image_form
    context['merchandises'] =merchandises

    return render(request, 'tengeneza_product.html', context)

def shop_now(request):
    merchandises=Merchandise.objects.all()
    return render(request, 'shop_now.html', {'merchandises':merchandises})

#def illness(request,id):
    ugonjwa=Ugonjwa.objects.get(id=1)
    if request.method=="POST":
        #getting the new values
        patient_name=request.POST['patient_name']
        ugonjwa_desc=request.POST['ugonjwa_desc']
       
        # equating the new values to the existing illness details
        ugonjwa.patient_name=patient_name
        ugonjwa.ugonjwa_desc=ugonjwa_desc
        
        # saving the illness details
        ugonjwa.save()
        # redirect to the homepage
        return redirect('index')

    return render(request,'illness.html',{"ugonjwa":ugonjwa})

def resize_image(image, size=(300,300)):
    img=Image.open(image)
    img=img.resize(size,Image.Resampling.LANCZOS)

    thumb_io=BytesIO()
    img.save(thumb_io, format=format)
    thumb_io.seek(0)

    return ContentFile(thumb_io.read(),name=image.name)

def typhoid_view(request):
    illness= get_object_or_404(Illness, name='Typhoid')

    images= Sign.objects.filter(illness=illness)
    return render(request,'typhoid.html',{"illness":illness, "images":images}) #giving the typhoid file access to the descritpion and images related to it

def cholera_view(request):
    illness= get_object_or_404(Illness, name='Cholera')

    images= Sign.objects.filter(illness=illness)

    return render(request,'cholera.html',{"illness":illness, "images":images}) #giving the cholera file access to the descritpion and images related to it

def bilharzia_view(request):
    illness= get_object_or_404(Illness, name='Bilharzia')

    images= Sign.objects.filter(illness=illness)

    return render(request,'bilharzia.html',{"illness":illness, "images":images}) #giving the bilharzia file access to the descritpion and images related to it


def malaria_view(request):
    illness= get_object_or_404(Illness, name='Malaria')

    images= Sign.objects.filter(illness=illness)

    return render(request,'malaria.html',{"illness":illness, "images":images}) #giving the malaria file access to the descritpion and images related to it

def gonorrhoea_view(request):
    illness= get_object_or_404(Illness, name='Gonorrhoea')

    images= Sign.objects.filter(illness=illness)

    return render(request,'gonorrhoea.html',{"illness":illness, "images":images}) #giving the gonorrhoea file access to the descritpion and images related to it

def syphilis_view(request):
    illness= get_object_or_404(Illness, name='Syphilis')

    images= Sign.objects.filter(illness=illness)

    return render(request,'syphilis.html',{"illness":illness, "images":images}) #giving the syphilis file access to the descritpion and images related to it

def herpes_view(request):
    illness= get_object_or_404(Illness, name='Genital_herpes')

    images= Sign.objects.filter(illness=illness)

    return render(request,'genital_herpes.html',{"illness":illness, "images":images}) #giving the herpes file access to the descritpion and images related to it

def search_view(request):
    query=request.GET.get('query','')
    results=None

    if query:
        results= Illness.objects.filter(name__icontains=query)

    return render(request,'search_results.html', {'results':results, 'query':query})

def illness_detail_view(request, illness_name):
    try:
        # Filter the illness by type and id
        illness = Illness.objects.get(name=illness_name)
    except Illness.DoesNotExist:
        raise Http404("Illness not found")

    template_name=f'{illness_name}.html'

    return render(request, template_name, {'illness': illness})

def contact(request):
    if request.method=='POST':
        form=ContactMessageForm(request.POST)
        if form.is_valid():
            contact=form.save()

        send_mail(
           'Contacting Us',
           'Thanks for reaching out, we will give feedback shortly',
           settings.DEFAULT_FROM_EMAIL,
           [form.cleaned_data["email"]],
           fail_silently=False,
        )

        messages.success(request, 'Your message has been successfully sent. Thank you for reaching out!')

        return redirect('index')

    else:
        form=ContactMessageForm()

    return render(request, 'index.html', {"form":form})

#class-based views(for serializers)
class TyphoidView(viewsets.ModelViewSet):
    queryset=Typhoid.objects.all()
    serializer_class=TyphoidSerializer