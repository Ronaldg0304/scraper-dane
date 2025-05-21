import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime



# Telegram config
TOKEN = '7659076432:AAGX_1_GB6tO-fIG0TcgZTUO0KakVhoMNCw'
CHAT_ID = '866289125'

# Función para enviar mensaje a Telegram
def enviar_telegram(mensaje):

    print("¡Mensaje enviado correctamente!")
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': mensaje
    }
    requests.post(url, data=payload)

# URL de convocatorias del DANE
url = "https://bpso.dane.gov.co/invitations/detailed"

# Lista para almacenar invitaciones conocidas
lista_invitaciones = []

def revisar_convocatorias():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    count = 0

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        invitaciones = soup.find_all('h4')
        departamentos = soup.find_all('h5')

        nuevas = []

        for i in invitaciones:
            if 'Invitación' in i.text and i.text not in lista_invitaciones:
                lista_invitaciones.append(i.text)
                nuevas.append(i.text)

        for invitacion in nuevas:
            mensaje = f"📢 Nueva invitación publicada:\n\n{invitacion}"
            enviar_telegram(mensaje)

        for d in departamentos:
            if d.text.lower() == 'sincelejo':
                count += 1


        enviar_telegram(f"📍 Convocatorias en Sincelejo: {count} ")
        count = 0
    else:
        print("Error al acceder a la página:", response.status_code)

# Ejecutar la revisión cada hora
while True:
    hora_actual = datetime.now().strftime("%H:%M:%S")
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    revisar_convocatorias()
    enviar_telegram(f"🔁 {fecha_actual}- Ultima revisión a las {hora_actual}")
    time.sleep(3600)  # 3600 segundos = 1 hora
