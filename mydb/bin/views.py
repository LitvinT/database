from django.shortcuts import render, redirect, reverse
from .models import User
import pandas as pd
import numpy as np  # Добавляем модуль numpy для обработки NaN значений

def upload_excel_file(request):
    if request.method == 'POST':
        if 'excel_file' not in request.FILES:
            return render(request, 'upload.html', {'error': 'Файл не выбран'})

        excel_file = request.FILES['excel_file']

        # Проверка на расширение файла
        if not excel_file.name.endswith('.xlsx'):
            return render(request, 'your_app/upload.html')  # Replace 'your_app' with the actual app name if needed

        # Загрузка файла Excel в DataFrame
        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            return render(request, 'upload.html', {'error': f'Ошибка при чтении файла: {e}'})

        # Заменяем NaN значения на пустую строку
        df.replace({np.nan: ''}, inplace=True)

        # Проходим по DataFrame и создаем записи в базе данных
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
                }
            )

            # Если пользователь уже существует, заполним его данные только если они отсутствуют
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

                user.save()

        # Выполняем редирект на страницу admin
        return redirect(reverse('admin:index'))

    return render(request, 'upload.html')
