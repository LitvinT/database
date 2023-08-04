from datetime import datetime
import numpy as np
import pandas as pd
from django.shortcuts import render, redirect, reverse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from .models import Client, Company, UpdateLog
from .serializers import ClientSerializer, CompanySerializer


def upload_client_excel_file(request):
    if request.method == 'POST':
        if 'excel_file' not in request.FILES:
            return render(request, 'client_excel.html', {'error': 'Файл не выбран'})

        excel_file = request.FILES['excel_file']

        if not excel_file.name.endswith('.xlsx'):
            return render(request, 'client_excel.html')

        try:
            df = pd.read_excel(excel_file, dtype={'phone': str, 'whatsapp_link': str})
        except Exception as e:
            return render(request, 'cleint_excel.html', {'error': f'Ошибка при чтении файла: {e}'})

        df.replace({np.nan: ''}, inplace=True)

        for _, row in df.iterrows():
            name = row.get('name', '')
            country = row.get('country', '')
            email = row.get('email', '')
            phone = row.get('phone', '')
            login_bitmain = row.get('login_bitmain', '')
            telegram_link = row.get('telegram_link', '')
            instagram_link = row.get('instagram_link', '')
            twitter_link = row.get('twitter_link', '')
            vk_link = row.get('vk_link', '')
            facebook_link = row.get('facebook_link', '')
            linkedin_link = row.get('linkedin_link', '')
            whatsapp_link = row.get('whatsapp_link', '')
            counter = row.get('counter', '')
            feedback = row.get('feedback', '')

            # Создаем пользователя, пропустив создание, если такой номер телефона уже существует
            client, created = Client.objects.get_or_create(
                phone=phone,
                defaults={
                    'name': name,
                    'country': country,
                    'email': email,
                    'login_bitmain': login_bitmain,
                    'telegram_link': telegram_link,
                    'instagram_link': instagram_link,
                    'twitter_link': twitter_link,
                    'vk_link': vk_link,
                    'facebook_link': facebook_link,
                    'linkedin_link': linkedin_link,
                    'whatsapp_link': whatsapp_link,
                    'counter': counter,
                    'feedback': feedback
                }
            )

            if not created:
                if not client.name and name:
                    client.name = name
                if not client.country and country:
                    client.country = country
                if not client.email and email:
                    client.email = email
                if not client.login_bitmain and login_bitmain:
                    client.login_bitmain = login_bitmain
                if not client.telegram_link and telegram_link:
                    client.telegram_link = telegram_link
                if not client.instagram_link and instagram_link:
                    client.instagram_link = instagram_link
                if not client.twitter_link and twitter_link:
                    client.twitter_link = twitter_link
                if not client.vk_link and vk_link:
                    client.vk_link = vk_link
                if not client.facebook_link and facebook_link:
                    client.facebook_link = facebook_link
                if not client.linkedin_link and linkedin_link:
                    client.linkedin_link = linkedin_link
                if not client.whatsapp_link and whatsapp_link:
                    client.whatsapp_link = whatsapp_link
                if not client.counter and counter:
                    client.counter = counter
                if not client.feedback and feedback:
                    client.feedback = feedback

                client.save()

        update_info = "Clients updated on {}".format(datetime.now())
        UpdateLog.objects.create(update_info=update_info)

        return redirect(reverse('admin:index'))

    return render(request, 'client_excel.html')


def rollback_update(request, log_id):
    try:
        log = UpdateLog.objects.get(id=log_id)
        clients_before_update = log.changes_before_update
        for client_data in clients_before_update:
            phone = client_data['phone']
            client, created = Client.objects.get_or_create(phone=phone, defaults=client_data)

            if not created:
                for field in client_data:
                    setattr(client, field, client_data[field])
                client.save()

        log.delete()
    except UpdateLog.DoesNotExist:
        pass

    return redirect('view_update_logs')


def view_update_logs(request):
    logs = UpdateLog.objects.all().order_by('-timestamp')
    return render(request, 'view_update_logs.html', {'logs': logs})


def upload_company_excel_file(request):
    if request.method == 'POST':
        if 'excel_file' not in request.FILES:
            return render(request, 'company_excel.html', {'error': 'Файл не выбран'})

        excel_file = request.FILES['excel_file']

        if not excel_file.name.endswith('.xlsx'):
            return render(request, 'company_excel.html')

        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            return render(request, 'company_excel.html', {'error': f'Ошибка при чтении файла: {e}'})

        df.replace({np.nan: ''}, inplace=True)

        for _, row in df.iterrows():
            name = row.get('name', '')
            country = row.get('country', '')
            email = row.get('email', '')
            phone = row.get('phone', '')
            individual = row.get('individual', '')
            individual2 = row.get('individual2', '')
            telegram_link = row.get('telegram_link', '')
            instagram_link = row.get('instagram_link', '')
            twitter_link = row.get('twitter_link', '')
            vk_link = row.get('vk_link', '')
            facebook_link = row.get('facebook_link', '')
            linkedin_link = row.get('linkedin_link', '')
            whatsapp_link = row.get('whatsapp_link', '')
            counter = row.get('counter', '')
            feedback = row.get('feedback', '')

            company, created = Company.objects.get_or_create(
                phone=phone,
                defaults={
                    'name': name,
                    'country': country,
                    'email': email,
                    'individual': individual,
                    'individual2': individual2,
                    'telegram_link': telegram_link,
                    'instagram_link': instagram_link,
                    'twitter_link': twitter_link,
                    'vk_link': vk_link,
                    'facebook_link': facebook_link,
                    'linkedin_link': linkedin_link,
                    'whatsapp_link': whatsapp_link,
                    'counter': counter,
                    'feedback': feedback
                }
            )

            if not created:
                if not company.name and name:
                    company.name = name
                if not company.country and country:
                    company.country = country
                if not company.email and email:
                    company.email = email
                if not company.individual and individual:
                    company.individual = individual
                if not company.individual2 and individual2:
                    company.individual2 = individual2
                if not company.telegram_link and telegram_link:
                    company.telegram_link = telegram_link
                if not company.instagram_link and instagram_link:
                    company.instagram_link = instagram_link
                if not company.twitter_link and twitter_link:
                    company.twitter_link = twitter_link
                if not company.vk_link and vk_link:
                    company.vk_link = vk_link
                if not company.facebook_link and facebook_link:
                    company.facebook_link = facebook_link
                if not company.linkedin_link and linkedin_link:
                    company.linkedin_link = linkedin_link
                if not company.whatsapp_link and whatsapp_link:
                    company.whatsapp_link = whatsapp_link
                if not company.counter and counter:
                    company.counter = counter
                if not company.feedback and feedback:
                    company.feedback = feedback

                company.save()

        return redirect(reverse('admin:index'))

    return render(request, 'company_excel.html')


def upload_company_csv_file(request):
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            return render(request, 'company_csv.html', {'error': 'Файл не выбран'})

        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            return render(request, 'company_csv.html')

        try:
            df = pd.read_csv(csv_file, delimiter=',',
                             names=['name', 'country', 'email', 'phone', 'individual', 'individual2', 'telegram_link',
                                    'instagram_link', 'twitter_link', 'vk_link', 'facebook_link', 'linkedin_link',
                                    'whatsapp_link', 'counter', 'feedback'],
                             skiprows=1)

        except Exception as e:
            return render(request, 'company_csv.html', {'error': f'Ошибка при чтении файла: {e}'})

        df.replace({np.nan: ''}, inplace=True)

        for index, row in df.iterrows():
            name = row['name']
            country = row['country']
            email = row['email']
            phone = row['phone']
            individual = row['individual']
            individual2 = row['individual2']
            telegram_link = row['telegram_link']
            instagram_link = row['instagram_link']
            twitter_link = row['twitter_link']
            vk_link = row['vk_link']
            facebook_link = row['facebook_link']
            linkedin_link = row['linkedin_link']
            whatsapp_link = row['whatsapp_link']
            counter = row['counter']
            feedback = row['feedback']

            company, created = Company.objects.get_or_create(
                phone=phone,
                defaults={
                    'name': name,
                    'country': country,
                    'email': email,
                    'individual': individual,
                    'individual2': individual2,
                    'telegram_link': telegram_link,
                    'instagram_link': instagram_link,
                    'twitter_link': twitter_link,
                    'vk_link': vk_link,
                    'facebook_link': facebook_link,
                    'linkedin_link': linkedin_link,
                    'whatsapp_link': whatsapp_link,
                    'counter': counter,
                    'feedback': feedback
                }
            )

            if not created:
                if not company.name and name:
                    company.name = name
                if not company.country and country:
                    company.country = country
                if not company.email and email:
                    company.email = email
                if not company.individual and individual:
                    company.individual = individual
                if not company.individual2 and individual2:
                    company.individual2 = individual2
                if not company.telegram_link and telegram_link:
                    company.telegram_link = telegram_link
                if not company.instagram_link and instagram_link:
                    company.instagram_link = instagram_link
                if not company.twitter_link and twitter_link:
                    company.twitter_link = twitter_link
                if not company.vk_link and vk_link:
                    company.vk_link = vk_link
                if not company.facebook_link and facebook_link:
                    company.facebook_link = facebook_link
                if not company.linkedin_link and linkedin_link:
                    company.linkedin_link = linkedin_link
                if not company.whatsapp_link and whatsapp_link:
                    company.whatsapp_link = whatsapp_link
                if not company.counter and counter:
                    company.counter = counter
                if not company.feedback and feedback:
                    company.feedback = feedback

                company.save()

        return redirect(reverse('admin:index'))

    return render(request, 'company_csv.html')


def upload_client_csv_file(request):
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            return render(request, 'client_csv.html', {'error': 'Файл не выбран'})

        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            return render(request, 'client_csv.html')

        try:
            df = pd.read_csv(csv_file, delimiter=',',
                             names=['name', 'country', 'email', 'phone', 'login_bitmain', 'telegram_link',
                                    'instagram_link', 'twitter_link', 'vk_link', 'facebook_link', 'linkedin_link',
                                    'whatsapp_link', 'counter', 'feedback'],
                             skiprows=1)

        except Exception as e:
            return render(request, 'client_csv.html', {'error': f'Ошибка при чтении файла: {e}'})

        df.replace({np.nan: ''}, inplace=True)

        for index, row in df.iterrows():
            name = row['name']
            country = row['country']
            email = row['email']
            phone = row['phone']
            login_bitmain = row['login_bitmain']
            telegram_link = row['telegram_link']
            instagram_link = row['instagram_link']
            twitter_link = row['twitter_link']
            vk_link = row['vk_link']
            facebook_link = row['facebook_link']
            linkedin_link = row['linkedin_link']
            whatsapp_link = row['whatsapp_link']
            counter = row['counter']
            feedback = row['feedback']

            client, created = Client.objects.get_or_create(
                phone=phone,
                defaults={
                    'name': name,
                    'country': country,
                    'email': email,
                    'login_bitmain': login_bitmain,
                    'telegram_link': telegram_link,
                    'instagram_link': instagram_link,
                    'twitter_link': twitter_link,
                    'vk_link': vk_link,
                    'facebook_link': facebook_link,
                    'linkedin_link': linkedin_link,
                    'whatsapp_link': whatsapp_link,
                    'counter': counter,
                    'feedback': feedback
                }
            )

            if not created:
                if not client.name and name:
                    client.name = name
                if not client.country and country:
                    client.country = country
                if not client.email and email:
                    client.email = email
                if not client.login_bitmain and login_bitmain:
                    client.login_bitmain = login_bitmain
                if not client.telegram_link and telegram_link:
                    client.telegram_link = telegram_link
                if not client.instagram_link and instagram_link:
                    client.instagram_link = instagram_link
                if not client.twitter_link and twitter_link:
                    client.twitter_link = twitter_link
                if not client.vk_link and vk_link:
                    client.vk_link = vk_link
                if not client.facebook_link and facebook_link:
                    client.facebook_link = facebook_link
                if not client.linkedin_link and linkedin_link:
                    client.linkedin_link = linkedin_link
                if not client.whatsapp_link and whatsapp_link:
                    client.whatsapp_link = whatsapp_link
                if not client.counter and counter:
                    client.counter = counter
                if not client.feedback and feedback:
                    client.feedback = feedback

                client.save()

        return redirect(reverse('admin:index'))

    return render(request, 'client_csv.html')


class ProtectedViewClient(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProtectedViewCompany(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(LoginView):
    form_class = LoginForm
    template_name = 'bin/index.html'


#ricky dicky doo dah grimes boom shakalaka boom shaka
