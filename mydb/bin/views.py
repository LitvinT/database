from datetime import datetime

import numpy as np
import pandas as pd
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

from .forms import LoginForm
from .models import User, Company, UpdateLog
from .serializers import UserSerializer, CompanySerializer


def upload_user_excel_file(request):
    if request.method == 'POST':
        if 'excel_file' not in request.FILES:
            return render(request, 'user_excel.html', {'error': 'Файл не выбран'})

        excel_file = request.FILES['excel_file']

        if not excel_file.name.endswith('.xlsx'):
            return render(request, 'user_excel.html')

        try:
            df = pd.read_excel(excel_file, dtype={'phone': str, 'whatsapp_link': str})
        except Exception as e:
            return render(request, 'user_excel.html', {'error': f'Ошибка при чтении файла: {e}'})

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
            user, created = User.objects.get_or_create(
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
                if not user.name and name:
                    user.name = name
                if not user.country and country:
                    user.country = country
                if not user.email and email:
                    user.email = email
                if not user.login_bitmain and login_bitmain:
                    user.login_bitmain = login_bitmain
                if not user.telegram_link and telegram_link:
                    user.telegram_link = telegram_link
                if not user.instagram_link and instagram_link:
                    user.instagram_link = instagram_link
                if not user.twitter_link and twitter_link:
                    user.twitter_link = twitter_link
                if not user.vk_link and vk_link:
                    user.vk_link = vk_link
                if not user.facebook_link and facebook_link:
                    user.facebook_link = facebook_link
                if not user.linkedin_link and linkedin_link:
                    user.linkedin_link = linkedin_link
                if not user.whatsapp_link and whatsapp_link:
                    user.whatsapp_link = whatsapp_link
                if not user.counter and counter:
                    user.counter = counter
                if not user.feedback and feedback:
                    user.feedback = feedback

                user.save()

        update_info = "Users updated on {}".format(datetime.now())
        UpdateLog.objects.create(update_info=update_info)

        return redirect(reverse('admin:index'))

    return render(request, 'user_excel.html')


def rollback_update(request, log_id):
    try:
        log = UpdateLog.objects.get(id=log_id)
        users_before_update = log.changes_before_update
        for user_data in users_before_update:
            phone = user_data['phone']
            user, created = User.objects.get_or_create(phone=phone, defaults=user_data)

            if not created:
                for field in user_data:
                    setattr(user, field, user_data[field])
                user.save()

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

            user, created = Company.objects.get_or_create(
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
                if not user.name and name:
                    user.name = name
                if not user.country and country:
                    user.country = country
                if not user.email and email:
                    user.email = email
                if not user.individual and individual:
                    user.individual = individual
                if not user.individual2 and individual2:
                    user.individual2 = individual2
                if not user.telegram_link and telegram_link:
                    user.telegram_link = telegram_link
                if not user.instagram_link and instagram_link:
                    user.instagram_link = instagram_link
                if not user.twitter_link and twitter_link:
                    user.twitter_link = twitter_link
                if not user.vk_link and vk_link:
                    user.vk_link = vk_link
                if not user.facebook_link and facebook_link:
                    user.facebook_link = facebook_link
                if not user.linkedin_link and linkedin_link:
                    user.linkedin_link = linkedin_link
                if not user.whatsapp_link and whatsapp_link:
                    user.whatsapp_link = whatsapp_link
                if not user.counter and counter:
                    user.counter = counter
                if not user.feedback and feedback:
                    user.feedback = feedback

                user.save()

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

            user, created = Company.objects.get_or_create(
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
                if not user.name and name:
                    user.name = name
                if not user.country and country:
                    user.country = country
                if not user.email and email:
                    user.email = email
                if not user.individual and individual:
                    user.individual = individual
                if not user.individual2 and individual2:
                    user.individual2 = individual2
                if not user.telegram_link and telegram_link:
                    user.telegram_link = telegram_link
                if not user.instagram_link and instagram_link:
                    user.instagram_link = instagram_link
                if not user.twitter_link and twitter_link:
                    user.twitter_link = twitter_link
                if not user.vk_link and vk_link:
                    user.vk_link = vk_link
                if not user.facebook_link and facebook_link:
                    user.facebook_link = facebook_link
                if not user.linkedin_link and linkedin_link:
                    user.linkedin_link = linkedin_link
                if not user.whatsapp_link and whatsapp_link:
                    user.whatsapp_link = whatsapp_link
                if not user.counter and counter:
                    user.counter = counter
                if not user.feedback and feedback:
                    user.feedback = feedback

                user.save()

        return redirect(reverse('admin:index'))

    return render(request, 'company_csv.html')


def upload_user_csv_file(request):
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            return render(request, 'user_csv.html', {'error': 'Файл не выбран'})

        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            return render(request, 'user_csv.html')

        try:
            df = pd.read_csv(csv_file, delimiter=',',
                             names=['name', 'country', 'email', 'phone', 'login_bitmain', 'telegram_link',
                                    'instagram_link', 'twitter_link', 'vk_link', 'facebook_link', 'linkedin_link',
                                    'whatsapp_link', 'counter', 'feedback'],
                             skiprows=1)

        except Exception as e:
            return render(request, 'user_csv.html', {'error': f'Ошибка при чтении файла: {e}'})

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

            user, created = User.objects.get_or_create(
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
                if not user.name and name:
                    user.name = name
                if not user.country and country:
                    user.country = country
                if not user.email and email:
                    user.email = email
                if not user.login_bitmain and login_bitmain:
                    user.login_bitmain = login_bitmain
                if not user.telegram_link and telegram_link:
                    user.telegram_link = telegram_link
                if not user.instagram_link and instagram_link:
                    user.instagram_link = instagram_link
                if not user.twitter_link and twitter_link:
                    user.twitter_link = twitter_link
                if not user.vk_link and vk_link:
                    user.vk_link = vk_link
                if not user.facebook_link and facebook_link:
                    user.facebook_link = facebook_link
                if not user.linkedin_link and linkedin_link:
                    user.linkedin_link = linkedin_link
                if not user.whatsapp_link and whatsapp_link:
                    user.whatsapp_link = whatsapp_link
                if not user.counter and counter:
                    user.counter = counter
                if not user.feedback and feedback:
                    user.feedback = feedback

                user.save()

        return redirect(reverse('admin:index'))

    return render(request, 'user_csv.html')


class ProtectedViewUser(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
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

