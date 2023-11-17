import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
#Twitter
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from wordcloud import WordCloud
from langdetect import detect
from googletrans import Translator
#linkedin
import spacy
#github
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def cargar_cv():
    cv_filename = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")])
    cv_entry.delete(0, tk.END)
    cv_entry.insert(0, cv_filename)

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
    cv_path = cv_entry.get()

    # Aquí puedes procesar la información según tus necesidades
    # Puedes imprimir o almacenar la información en una base de datos, por ejemplo
    print("Perfil Requerido:", perfil_requerido)
    print("Redes Sociales:", redes_sociales)
    print("CV Path:", cv_path)

def extraer_datos_redes():
    # Puedes colocar aquí la lógica para extraer datos de las redes sociales
    messagebox.showinfo("Extracción de Datos", "Datos extraídos de las redes sociales")

def analizar_datos():
    # Puedes colocar aquí la lógica para analizar los datos
    """Analisis de datos Twitter"""
    with open('datos_redes_sociales.txt', 'r', encoding='utf-8') as file:
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
# Cargar el modelo de procesamiento de lenguaje natural de spaCy
nlp = spacy.load("es_core_news_sm")  # Puedes usar un modelo específico para tu idioma
 
# Texto de ejemplo: Descripción del puesto y experiencia del candidato
descripcion_puesto = "Buscamos un desarrollador de Python con experiencia en desarrollo web y al menos 2 años de experiencia."
experiencia_candidato = "Desarrollador de Python con 3 años de experiencia en desarrollo web."
 
# Procesar la descripción del puesto y la experiencia del candidato
doc_puesto = nlp(descripcion_puesto)
doc_candidato = nlp(experiencia_candidato)
 
# Función para evaluar la similitud contextual
def evaluar_similitud_contextual(doc1, doc2):
	similitud = doc1.similarity(doc2)
	return similitud
 
# Evaluar la similitud contextual entre la descripción del puesto y la experiencia del candidato
similitud_contextual = evaluar_similitud_contextual(doc_puesto, doc_candidato)
 
# Establecer un umbral de similitud
umbral_similitud = 0.7  # Puedes ajustar este umbral según tus criterios
 
# Evaluar si la experiencia del candidato es coherente con la descripción del puesto
if similitud_contextual >= umbral_similitud:
	print("La experiencia del candidato es coherente con la descripción del puesto.")
else:
	print("La experiencia del candidato no es coherente con la descripción del puesto.")
 
# Imprimir la similitud contextual (puede ser útil para fines de análisis)
print(f"Similitud Contextual: {similitud_contextual:.2f}")


"""Analisis de datos GitHub"""
# Datos de ejemplo: candidatos y requisitos del trabajo
candidatos = pd.DataFrame({
    'ID': [1, 2, 3],
    'Experiencia': [
        "Desarrollador de Python con 3 años de experiencia en desarrollo web.",
        "Ingeniero de software con experiencia en Java y C++.",
        "Programador junior con conocimientos de Python y JavaScript."
    ]
})

requisitos_puesto = "Buscamos un desarrollador de Python con experiencia en desarrollo web y al menos 2 años de experiencia."

# Preprocesamiento de texto
tfidf_vectorizer = TfidfVectorizer()
documentos = candidatos['Experiencia'].tolist() + [requisitos_puesto]
matriz_tfidf = tfidf_vectorizer.fit_transform(documentos)

# Calcular similitud de coseno entre la descripción del trabajo y las experiencias de los candidatos
similitudes = cosine_similarity(matriz_tfidf[:-1], matriz_tfidf[-1:])

# Calcular una puntuación de relevancia para cada candidato
puntuaciones_relevancia = similitudes.flatten()

# Asegurarse de que la longitud de puntuaciones_relevancia coincida con la longitud de candidatos
candidatos['Puntuacion_Relevancia'] = puntuaciones_relevancia[:len(candidatos)]

# Imprimir los resultados
print(candidatos[['ID', 'Experiencia', 'Puntuacion_Relevancia']])


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
