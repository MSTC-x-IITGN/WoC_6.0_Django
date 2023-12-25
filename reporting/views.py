from django.shortcuts import render, redirect
from .models import Report
from django.contrib import messages
import requests
from management.models import Volunteer

#from .models import Report
# Create your views here.

def report(request):
    if request.method == "POST":
        if Report.objects.filter(name=request.POST['name'], description=request.POST['description']).exists():
            messages.error(request, 'This report has already been recorded.')
            return redirect('report')

        user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if user_ip_address:
            ip = user_ip_address.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        data = requests.get(f"https://ipgeolocation.abstractapi.com/v1/?api_key=0440e7551b564ac39aeb19aed5a06a51&ip_address={ip}").json()
        print(ip,data)
        report = Report(
            name=request.POST['name'],
            description=request.POST['description'],
            severity=request.POST['severity'],
            lat=data['latitude'] if data['latitude'] else 23.188544,
            lon=data['longitude'] if data['longitude'] else 72.628918,
            status='R'
        )
        report.save()
        return redirect('dashboard')

    return render(request, 'report.html')


def dashboard(request):
    if request.user.is_authenticated and (Volunteer.objects.filter(user=request.user).exists()):
        reports = Report.objects.exclude(assignee=request.user.volunteer, status='I').order_by('created')
        myTask = Report.objects.filter(assignee=request.user.volunteer, status='I')
        if myTask:
            myTask = myTask[0]
            return render(request, 'dashboard.html', {'myTask':myTask, 'otherReports':reports})
    reports = Report.objects.order_by('created')
    return render(request, 'dashboard.html', {'otherReports':reports})


def acceptTask(request, rID):
    report = Report.objects.filter(reportID=rID)
    if report:
        report = report[0]
    else:
        messages.error(request, "Some Error Occured.")
        return redirect(dashboard)

    if report.assignee is not None:
        messages.error(request, "Task already assigned.")
        return redirect(dashboard)

    report.assignee = request.user.volunteer
    report.status = 'I'
    request.user.volunteer.availability = False
    request.user.volunteer.save()
    report.save()
    return redirect(dashboard)

def solveTask(request, rID):
    report = Report.objects.filter(reportID=rID)
    if report:
        report = report[0]
    else:
        messages.error(request, "Some Error Occured.")
        return redirect(dashboard)

    if report.assignee != request.user.volunteer:
        messages.error(request, "Access Denied.")
        return redirect(dashboard)

    report.status = 'S'
    request.user.volunteer.availability = True
    request.user.volunteer.save()
    report.save()
    return redirect(dashboard)