from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.mail import send_mail
from Send_Message_CSV.settings import EMAIL_HOST_USER
import csv
import datetime
import pytz
import pandas as pd


# Create your views here
class CSV(View):
    def get(self,request):
        return render(request,"csv.html")
    def post(self,request):
        try:
            message = str(request.POST.get('message'))
            email = str(request.POST.get('email'))
            phone = int(request.POST.get('phone'))
            country = str(request.POST.get('country'))
            date = request.POST.get('date')
            # fields=["Message","Email","Phone","Country","Schedule On"]
            row = [message,email,phone,country,date]
            file=open("sample.csv","a")
            ref=csv.writer(file)
            ref.writerow(row)
            file.close()
            messages.success(request,"Data Inserted Succcessfully Into CSV...")
            return redirect('csv')
        except ValueError:
            messages.error(request,"Please Provide Valid Phone Number...")
            return redirect('csv')
class EMAIL(View):
    def get(self,request):
        df=pd.read_csv("sample.csv")
        return render(request,"email.html",{'rows': df.to_dict('records')})
    def post(self,request):
        todays_date=datetime.datetime.now().date()
        df = pd.read_csv("sample.csv")
        data=df.to_dict('records')
        list=[]
        for x in data:
            list.append(x)
        for x in list:
            try:
                if str(todays_date) == str(x['Schedule']):
                    send_mail("No subject in CSV file", x['Message'], EMAIL_HOST_USER, [x['Email']])
                    continue
                else:
                    continue
            except:
                messages.error(request,"Invalid Emails In Todays Schedule...")
                return redirect('email')
        messages.success(request, "Email Has Been Sent On Todays Schedule...")
        return redirect('email')


def delete(request):
    name=request.GET.get('email')
    file=open('sample.csv', 'r')
    reader = csv.reader(file)
    lines = list()
    for row in reader:
        lines.append(row)
        for field in row:
            if field == name:
                lines.remove(row)
    with open('sample.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    return redirect('email')


class SMS(View):
    def get(self,request):
        df = pd.read_csv("sample.csv")
        return render(request, "sms.html", {'rows': df.to_dict('records')})
    def post(self,request):
        todays_date = datetime.datetime.now().date()
        df = pd.read_csv("sample.csv")
        data = df.to_dict('records')
        list = []
        for x in data:
            list.append(x)
        for x in list:
            try:
                if str(todays_date) == str(x['Schedule']):
                    if x['Country']=='INDIA':
                        ind = datetime.datetime.now()
                        hrs = ind.hour
                        mins = ind.minute
                        secs = ind.second
                        zero = datetime.timedelta(seconds=secs + mins * 60 + hrs * 3600)
                        st = ind - zero  # this take me to 0 hours.
                        time1 = st + datetime.timedelta(seconds=10 * 3600)  # this gives 10 AM
                        time2 = st + datetime.timedelta(seconds=17 * 3600)  # this gives 5 PM
                        print(time1)
                        print(time2)
                        if ind >= time1 or ind <= time2:
                            import requests
                            url = "https://www.fast2sms.com/dev/bulk"
                            payload = {
                                'sender_id': "FSTSMS",
                                'message': x['Message'],
                                'language': 'english',
                                'route': 'p',
                                'numbers': int(x['Phone'])
                            }
                            headers = {
                                'authorization': "fZYBQRum4eoMVFSp8jCGKcvNJX3hzLAak1ixO657d9IqHlTbDsNlbRn2drgWqC0mf469B35IuDyaOosZ",
                                'Content-Type': "application/x-www-form-urlencoded",
                                'Cache-Control': "no-cache",
                            }
                            response = requests.request("POST", url, data=payload, headers=headers)
                            response.json()
                            print(response.text)
                            continue
                    else:
                        country = pytz.timezone('America/New_York')
                        usa = datetime.datetime.now(country)
                        print(usa)
                        hrs = usa.hour
                        mins = usa.minute
                        secs = usa.second
                        zero = datetime.timedelta(seconds=secs + mins * 60 + hrs * 3600)
                        st = usa - zero  # this take me to 0 hours.
                        time1 = st + datetime.timedelta(seconds=10 * 3600)  # this gives 10 AM
                        time2 = st + datetime.timedelta(seconds=17 * 3600)  # this gives 5 PM
                        print(time1)
                        print(time2)
                        if usa >= time1 or usa <= time2:
                            import requests
                            url = "https://www.fast2sms.com/dev/bulk"
                            payload = {
                                'sender_id': "FSTSMS",
                                'message': x['Message'],
                                'language': 'english',
                                'route': 'p',
                                'numbers': int(x['Phone'])
                            }
                            headers = {
                                'authorization': "fZYBQRum4eoMVFSp8jCGKcvNJX3hzLAak1ixO657d9IqHlTbDsNlbRn2drgWqC0mf469B35IuDyaOosZ",
                                'Content-Type': "application/x-www-form-urlencoded",
                                'Cache-Control': "no-cache",
                            }
                            response = requests.request("POST", url, data=payload, headers=headers)
                            response.json()
                            print(response.text)
                            continue
                else:
                    continue
            except:
                messages.error(request, "Error In Sending SMS's On Todays Schedule...")
                return redirect('sms')
        messages.error(request, "SMS Sent On Todays Schedule...")
        return redirect('sms')









