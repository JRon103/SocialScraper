
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
#Twitter
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
#from wordcloud import WordCloud
from langdetect import detect
from googletrans import Translator
#linkedin
import spacy
#github
#import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import requests
from bs4 import BeautifulSoup
from selenium import webdriver 
import time
from selenium.webdriver.chrome.service import Service
import json
from datetime import datetime
'''
def cargar_cv():
    cv_filename = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")])
    cv_entry.delete(0, tk.END)
    cv_entry.insert(0, cv_filename)
'''

def generar_grafico(datos):
    lenguajes = []
    cantidades = []

    for linea in datos:
        partes = linea.strip().split(': ')
        lenguaje = partes[0]
        cantidad = int(partes[1].split()[0])
        lenguajes.append(lenguaje)
        cantidades.append(cantidad)

    # Crear un diccionario con el nombre del lenguaje y la cantidad de veces
    datos = {lenguajes[i]: cantidades[i] for i in range(len(lenguajes))}
        
    # Encontrar el lenguaje con la mayor cantidad
    lenguaje_maximo = max(datos, key=datos.get)
    maxima_cantidad = datos[lenguaje_maximo]
        
    # Crear un gráfico circular
    plt.figure(figsize=(8, 8))
    plt.pie(cantidades, labels=lenguajes, autopct='%1.1f%%', startangle=140)
    plt.title('Lenguajes de programación utilizados por el candidato')

    # Agregar texto en el centro con el lenguaje más usado
    plt.text(0, 0, f'{lenguaje_maximo}\n{maxima_cantidad} proyectos', ha='center', va='center', fontsize=12, color='white')

    plt.axis('equal')  # Asegurar que el gráfico sea un círculo
    plt.show()

def siguiente_campo(event):
    focus = ventana.focus_get()
    if focus == perfil_text:
        linkedin_entry.focus_set()
    elif focus == linkedin_entry:
        github_entry.focus_set()
    elif focus == github_entry:
        twitter_entry.focus_set()
    elif focus == twitter_entry:
        analizar_datos()

def guardar_informacion():
    perfil_requerido = perfil_text.get("1.0", tk.END).strip()
    redes_sociales = {
        "LinkedIn": linkedin_entry.get(),
        "GitHub": github_entry.get(),
        "Twitter": twitter_entry.get(),
    }
    #cv_path = cv_entry.get()
    
    # Guardar el perfil requerido en un archivo de texto
    with open('perfil_requerido.txt', 'w', encoding='utf-8') as file:
        file.write(perfil_requerido)

    # Aquí puedes procesar la información según tus necesidades
    # Puedes imprimir o almacenar la información en una base de datos, por ejemplo
    print("Perfil Requerido:", perfil_requerido)
    print("Redes Sociales:", redes_sociales)
    #print("CV Path:", cv_path)
  

  #funciones para extraer informacion--------------------------------------------------------------------------
def github(link, output_file):
    URL = link
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")
    
    elements = soup.find_all('span', itemprop='programmingLanguage')
    lenguajes_count = {}
    # Extraer el texto de cada elemento encontrado
    for element in elements:
        lenguaje = element.text
        if lenguaje in lenguajes_count:
            lenguajes_count[lenguaje] += 1
        else:
            lenguajes_count[lenguaje] = 1
    
    result = ""
    for lenguaje, count in lenguajes_count.items():
        result += f"{lenguaje}: {count} veces\n"

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(result)

def twitter(link, output_file):
    url = link
    print(url)
    service = Service()
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.headless = True 
    driver = webdriver.Firefox(service=service, options=options)
    
    driver.get(url)
    
    time.sleep(8)
    
    html = driver.page_source
    
    soup = BeautifulSoup(html, "html.parser")
    spans = soup.find_all("div", {"data-testid": "tweetText"})
    
    textos = [span.find("span").text for span in spans]
    result = "\n".join(textos)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(result)

'''def linkedin(link, output_file):
    url = link
    print(url)
    service = Service()
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.headless = True 
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(url)
    
    time.sleep(5)
    
    html = driver.page_source
    
    soup = BeautifulSoup(html, "html.parser")
    script_element = soup.find("script", {"type": "application/ld+json"})
    
    if script_element:
        json_text = script_element.string
        data = json.loads(json_text)
        nombre = data["@graph"][0]["name"]
        print("Nombre:", nombre)

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, indent=2))

    driver.close()'''
def  linkedin(link, output_file):
    api_key = 'AUVMiXDdwmI0NrKONPnl8w'
    headers = {'Authorization': 'Bearer ' + api_key}
    api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/company'
    params = {
        'url': 'https://www.linkedin.com/company/google/',
        'resolve_numeric_id': 'true',
        'categories': 'include',
        'funding_data': 'include',
        'extra': 'include',
        'exit_data': 'include',
        'skills': 'include',
        'acquisitions': 'include',
        'use_cache': 'if-present',
    }
    response = requests.get(api_endpoint,
                            params=params,
                            headers=headers)
    formatted_data = json.dumps(response.json(), indent=4)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(formatted_data)
def extraer_datos_redes():

    # Obtiene los enlaces de LinkedIn, GitHub y Twitter desde las entradas de la interfaz gráfica
    # linkedinLink = linkedin_entry.get()
    githubLink = github_entry.get()
    #twitterLink = twitter_entry.get()
    # Puedes colocar aquí la lógica para extraer datos de las redes sociales
    github_output_file = 'github_result.txt'
    twitter_output_file = 'twitter_result.txt'
    linkedin_output_file = 'linkedin_result.txt'

    github(githubLink, github_output_file)
    #twitter(twitterLink, twitter_output_file)
    # linkedin(linkedinLink, linkedin_output_file)
    messagebox.showinfo("Extracción de Datos", "Datos extraídos de las redes sociales")
#----------------------------------------------------------------------------------------------------------
def analizar_datos():
    extraer_datos_redes()
    guardar_informacion()
    # Puedes colocar aquí la lógica para analizar los datos
    """Analisis de datos Twitter"""
    with open('twitter_result.txt', 'r', encoding='utf-8') as file:
        mensajes = file.readlines()

# Función para traducir un mensaje a inglés
    def traducir_a_ingles(mensaje):
        translator = Translator()
        try:
            translation = translator.translate(mensaje, src=detect(mensaje), dest='en')
            return translation.text
        except:
            return mensaje

    # Traducir todos los mensajes a inglés
    mensajes_traducidos = [traducir_a_ingles(mensaje) for mensaje in mensajes]

    # Crear un DataFrame con los mensajes traducidos
    datos = pd.DataFrame({'Texto': mensajes_traducidos})

    # Análisis de sentimientos
    datos['Sentimiento'] = datos['Texto'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)

    # Visualizar distribución de sentimientos
    plt.figure(figsize=(10, 6))
    plt.hist(datos['Sentimiento'], bins=30, edgecolor='black')
    plt.title('Distribución de Sentimientos')
    plt.xlabel('Sentimiento')
    plt.ylabel('Frecuencia')
    plt.show()

    """Analisis de datos Linkedin"""

        # Leer los datos del archivo JSON
    with open('jsonJulian.txt', 'r', encoding='utf-8') as file:
        json_data = file.read()

    # Parsear el JSON
    data = json.loads(json_data)

    # Experiencias laborales
    experiences = data.get('experiences', [])
    print (experiences)
    # Definir los pesos para los roles
    weights = {
        "Software Engineer Intern": 30,
        "Engineering Intern": 25,
        "Collaborator": 20,
        "Committee": 15,
        "Solutions Developer Engineer":30
    }

    total_weight = 0
    total_score = 0

    # Calcular la evaluación basada en las experiencias laborales
    for experience in experiences:
        title = experience.get('title')
        if title in weights:
            weight = weights[title]
            total_weight += weight
            
            # Calcular una puntuación por duración (se podría ajustar con más criterios)
            starts_at = experience.get('starts_at', {})
            ends_at = experience.get('ends_at', {})
            print(": ",starts_at)
            print("f: ",ends_at)
            if ends_at == None:
                
                # Calcular una puntuación por duración (se podría ajustar con más criterios)
                starts_at = experience.get('starts_at', {})
                ends_at = experience.get('ends_at', {})
                # Obtén la fecha y hora actuales
                fecha_actual = datetime.now()

                # Obtén el día, mes y año por separado
                dia = fecha_actual.day
                mes = fecha_actual.month
                año = fecha_actual.year

                # Imprime los valores por separado
                print("Día:", dia)
                print("Mes:", mes)
                print("Año:", año)
                duration = (año - starts_at.get('year', 0)) * 12 + \
                    (mes - starts_at.get('month', 0))
            else:
                duration = (ends_at.get('year', 0) - starts_at.get('year', 0)) * 12 + \
                    (ends_at.get('month', 0) - starts_at.get('month', 0))

            # Puntuación basada en la duración (una escala lineal simple para la demostración)
            print("duracion: ",duration)
            score = min(duration / 12, 1) * weight  # Limitar la puntuación a un máximo de weight
            total_score += score

    # Calcular la evaluación final
    evaluation = (total_score / total_weight) * 100 if total_weight > 0 else 0

    # Mostrar resultados en una gráfica
    labels = list(weights.keys())
    scores = [0] * len(labels)

    # Actualizar las puntuaciones para los roles que están presentes en las experiencias
    for experience in experiences:
        title = experience.get('title')
        if title in weights:
            index = labels.index(title)
            scores[index] = weights[title]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, scores, color='skyblue')
    plt.xlabel('Roles')
    plt.ylabel('Peso')
    plt.title('Evaluación de Roles en Experiencias Laborales')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    print(f"Evaluación del perfil: {evaluation:.2f}")


    """Analisis de datos GitHub"""
    # Leer los datos desde el archivo
    with open('github_result.txt', 'r') as archivo:
        datos = archivo.readlines()
    # Llamar a la función para generar el gráfico
    generar_grafico(datos)
    
    messagebox.showinfo("Análisis de Datos", "Datos analizados")












# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Formulario de Candidato")

# Crear y colocar los elementos en la ventana
perfil_label = tk.Label(ventana, text="Perfil Requerido:")
perfil_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

perfil_text = tk.Text(ventana, height=5, width=40)
perfil_text.grid(row=0, column=1, columnspan=2, padx=10, pady=5)
perfil_text.bind("<Return>", siguiente_campo)  # Enlazar la tecla Enter al cambio de campo


#cv_label = tk.Label(ventana, text="Cargar CV:")
#cv_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
#cv_entry = tk.Entry(ventana, width=40)
#cv_entry.grid(row=1, column=1, padx=10, pady=5)
"""
cv_button = tk.Button(ventana, text="Guardar Perfil", command=cargar_cv)
cv_button.grid(row=1, column=2, padx=5, pady=5)
"""
redes_sociales_label = tk.Label(ventana, text="Redes Sociales:")
redes_sociales_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

linkedin_label = tk.Label(ventana, text="LinkedIn:")
linkedin_label.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
linkedin_entry = tk.Entry(ventana, width=30)
linkedin_entry.grid(row=2, column=2, padx=10, pady=5)
linkedin_entry.bind("<Return>", siguiente_campo) 

github_label = tk.Label(ventana, text="GitHub:")
github_label.grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)
github_entry = tk.Entry(ventana, width=30)
github_entry.grid(row=3, column=2, padx=10, pady=5)
github_entry.bind("<Return>", siguiente_campo) 

twitter_label = tk.Label(ventana, text="Twitter:")
twitter_label.grid(row=4, column=1, sticky=tk.W, padx=10, pady=5)
twitter_entry = tk.Entry(ventana, width=30)
twitter_entry.grid(row=4, column=2, padx=10, pady=5)
twitter_entry.bind("<Return>", siguiente_campo) 

"""
extraer_button = tk.Button(ventana, text="Extraer Datos", command=extraer_datos_redes)
extraer_button.grid(row=5, column=2, padx=10, pady=5)
"""
analizar_button = tk.Button(ventana, text="Analizar Datos", command=analizar_datos)
analizar_button.grid(row=6, column=2, padx=10, pady=5)
"""
guardar_button = tk.Button(ventana, text="Guardar Información", command=guardar_informacion)
guardar_button.grid(row=6, column=2, columnspan=3, pady=10)
"""
# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()
