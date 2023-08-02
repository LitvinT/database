import json
import requests

url = 'http://127.0.0.1:62717/api/v1/users/'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkwOTg5NDQzLCJpYXQiOjE2OTA5ODkxNDMsImp0aSI6IjNiZDE4ZDM3ZDk4ZDQ0NjY5ZWVhNGM2MjQ1YWRlN2Y1IiwidXNlcl9pZCI6MX0.-iVlTDMS3Cv-CR29k5MY6EbmHGp9g3rcMvn43YFGbg0'
headers = {'Authorization': f'Bearer {token}'}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    formatted_data = json.dumps(data, indent=4)

    # Записываем данные в файл "users_data.json"
    with open('users_data.json', 'w') as file:
        file.write(formatted_data)

    print('Данные успешно сохранены в файл "users_data.json"')
else:
    print('Ошибка при запросе к API:', response.status_code)
