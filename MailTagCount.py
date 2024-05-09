import pandas as pd
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import pickle


# Credenciales
SCOPES = ['https://mail.google.com/']
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

# Conexión a la API de Gmail
service = build('gmail', 'v1', credentials=creds)

def obtener_numero_correos_etiqueta(etiqueta_id):
    response = service.users().messages().list(userId='me', labelIds=[etiqueta_id]).execute()
    cantidad_correos = response.get('resultSizeEstimate', 0)
    return cantidad_correos

def contar_correos_etiquetas():
    etiquetas = service.users().labels().list(userId='me').execute().get('labels', [])
    etiquetas_ordenadas = sorted(etiquetas, key=lambda etiqueta: etiqueta['name'])  # Order tags by name
    
    data = []
    for etiqueta in etiquetas_ordenadas:
        etiqueta_id = etiqueta['id']
        cantidad_correos = obtener_numero_correos_etiqueta(etiqueta_id)
        data.append({'Etiqueta': etiqueta['name'], 'Cantidad de Correos': cantidad_correos})

    df = pd.DataFrame(data)
    return df

def filtrar_etiquetas(df):
    etiquetas_a_eliminar = ['CATEGORY_FORUMS', 'CATEGORY_PERSONAL', 'CATEGORY_PROMOTIONS', 'CATEGORY_SOCIAL', 
                            'CATEGORY_UPDATES', 'CHAT', 'DRAFT', 'IMPORTANT', 'SENT', 'SPAM', 'STARRED', 
                            'TRASH', 'UNREAD','Z CARTA DEL PADRE A CAMINANTES']
    df_filtrado = df[~df['Etiqueta'].isin(etiquetas_a_eliminar)]
    return df_filtrado

def contar_correos_etiquetas_total():
    etiquetas = service.users().labels().list(userId='me').execute().get('labels', [])
    
    data = []
    for etiqueta in etiquetas:
        etiqueta_id = etiqueta['id']
        cantidad_correos_etiqueta = obtener_numero_correos_etiqueta(etiqueta_id)
        if cantidad_correos_etiqueta >= 0:
            if '/' in etiqueta['name']:
                nombre_etiqueta, subetiqueta = etiqueta['name'].split('/')
                cantidad_correos_subetiqueta = obtener_numero_correos_etiqueta(etiqueta_id)
                data.append({'Etiqueta': nombre_etiqueta, 'Subetiqueta': subetiqueta, 'Cantidad de Correos': cantidad_correos_subetiqueta})
            else:
                data.append({'Etiqueta': etiqueta['name'], 'Subetiqueta': None, 'Cantidad de Correos': cantidad_correos_etiqueta})

    df = pd.DataFrame(data)
        # Agrupar por etiqueta y sumar la cantidad de correos
    df_suma = df.groupby('Etiqueta', as_index=False)['Cantidad de Correos'].sum()
        # Ordenar por orden alfabético
    df_suma = df_suma.sort_values(by='Etiqueta')
         # Renombrar la columna 'Etiqueta' por 'Caminante'
   # df_suma = df_suma.rename(columns={'Etiqueta': 'Caminante'})
    return df_suma