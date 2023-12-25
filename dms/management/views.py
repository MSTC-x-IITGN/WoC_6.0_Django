from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import OrganizationForm,VolunteerForm, ResourceForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *

# Create your views here.

def userlogin(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('userlogin')

    return render(request, 'userlogin.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        if User.objects.filter(username=request.POST['email']).exists():
            messages.error(request, "E-mail already exists.")
            return redirect('register')

        if request.POST['password'] != request.POST['confpassword']:
            messages.error(request, "The passwords entered do not match.")
            return redirect('register')

        if len(request.POST['password']) < 8:
            messages.error(request, "Password length is too short.")
            return redirect('register')

        user = User(first_name=request.POST['name'], username=request.POST['email'], password=request.POST['password'])
        request.session['username'] = user.username
        user.save()

        if request.POST['type'] == "volunteer":
            return redirect('volregister')
        else:
            return redirect('orgregister')

    return render(request, 'userreg.html')


def volregister(request):
    form = VolunteerForm()
    user = User.objects.get(username=request.session['username'])
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
                volunteer = form.save(commit=False)
                volunteer.user = user
                volunteer.save()
                login(request, user)
                return redirect('index')
        else:
            return render(request, 'register.html', {'form':form, 'type':'Volunteer'})
    return render(request, 'register.html', {'form':form, 'type':'Volunteer'})



def orgregister(request):
    if request.user.is_authenticated:
        return redirect('index')

    user = User.objects.get(username=request.session['username'])
    form = OrganizationForm()
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
                org = form.save(commit=False)
                org.user = user
                org.save()
                login(request, user)
                return redirect('index')
        else:
            return render(request, 'register.html', {'form':form})

    return render(request, 'register.html', {'form':form, 'type':'Organization'})


def userlogout(request):
    logout(request)
    return redirect('index')


def resources(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if Volunteer.objects.filter(user=request.user).exists():
        resources = Resource.objects.filter(organization=request.user.volunteer.organization)
    else:
        resources = Resource.objects.filter(organization=request.user.organization)
    return render(request, 'resources.html', {'resources':resources})


def addResource(request):
    if request.user.is_authenticated:
        try:
            user = request.user.organization
        except:
            messages.error(request, 'Cannot Add Resource')
            return redirect('resources')
    else:
        messages.error(request, 'Cannot view resources')
        return redirect('index')

    form = ResourceForm()
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
                resource = form.save(commit=False)
                resource.organization = request.user.organization
                resource = form.save()
                return redirect('resources')
        else:
            return render(request, 'resourceform.html', {'form':form})
    return render(request, 'resourceform.html', {'form':form, 'type':'Add'})


def editResource(request, rID):
    if request.user.is_authenticated:
        try:
            user = request.user.organization
        except:
            messages.error(request, 'Cannot Add Resource')
            return redirect('resources')
    else:
        messages.error(request, 'Cannot view resources')
        return redirect('index')

    try:
        resource = Resource.objects.filter(resourceID=rID, organization=request.user.organization)[0]
    except:
        messages.error(request, 'Resource does not exist.')
        return redirect('resources')

    form = ResourceForm(instance=resource)
    if request.method == 'POST':
        form = ResourceForm(request.POST, instance=resource)
        if form.is_valid():
                resource = form.save()
                return redirect('resources')
        else:
            return render(request, 'resourceform.html', {'form':form})

    return render(request, 'resourceform.html', {'form':form, 'type':'Edit'})


def delResource(request, rID):
    try:
        user = request.user.organization
    except:
        messages.error(request, 'Cannot Delete Resource')
        return redirect('resources')

    Resource.objects.filter(resourceID=rID, organization=request.user.organization).delete()

    return redirect('resources')


def volunteers(request):
    if not request.user.is_authenticated:
        return redirect('index')

    if Volunteer.objects.filter(user=request.user).exists():
        volunteers = Volunteer.objects.filter(organization=request.user.volunteer.organization)
    else:
        volunteers = Volunteer.objects.filter(organization=request.user.organization)

    return render(request, 'volunteers.html', {'volunteers':volunteers})