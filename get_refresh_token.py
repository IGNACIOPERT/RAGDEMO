import os
import requests
from flask import Flask, redirect, request
from urllib.parse import urlencode

# Configuración de tu cliente OAuth 2.0
CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID'
CLIENT_SECRET = 'YOUR_GOOGLE_CLIENT_SECRET'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'  # URL de redirección
SCOPE = 'https://www.googleapis.com/auth/drive'

app = Flask(__name__)

# Paso 1: La URL de autorización
@app.route('/')
def index():
    auth_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    params = {
        'scope': SCOPE,
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'access_type': 'offline',
    }
    url = f'{auth_url}?{urlencode(params)}'
    return redirect(url)

# Paso 2: La URL de callback donde Google redirige
@app.route('/callback')
def callback():
    # Obtener el código de autorización de la URL
    code = request.args.get('code')

    # Intercambiar el código de autorización por los tokens
    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
    }

    # Realizar la solicitud POST para obtener los tokens
    response = requests.post(token_url, data=data)
    tokens = response.json()

    # Almacenar los tokens (o mostrarlos en la pantalla)
    access_token = tokens.get('access_token')
    refresh_token = tokens.get('refresh_token')

    return f'Access Token: {access_token}<br>Refresh Token: {refresh_token}'

if __name__ == '__main__':
    app.run(debug=True, port=5000)