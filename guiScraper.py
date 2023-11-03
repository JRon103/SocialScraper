import tkinter as tk
import requests
from bs4 import BeautifulSoup

def github(link):
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

    return result

def twitter(link):
    page = link
    soup = BeautifulSoup(page, "html.parser")
    spans = soup.find_all("div", {"data-testid": "tweetText"})
    
    textos = [span.find("span").text for span in spans]
    
    return "\n".join(textos)

def mostrar_informacion():
    if opcion_var.get() == 1:
        link = textbox2.get("1.0", "end-1c")
        resultado = github(link)
    elif opcion_var.get() == 2:
        link = textbox3.get("1.0", "end-1c")
        resultado = twitter(link)
    else:
        resultado = "Selecciona una opción válida"
    
    label_info.config(text=resultado)

# Crear una ventana principal
ventana = tk.Tk()
ventana.title("Interfaz con Tkinter")

# Etiquetas
label1 = tk.Label(ventana, text="Texto 1:")
label2 = tk.Label(ventana, text="URL de GitHub:")
label3 = tk.Label(ventana, text="URL de Twitter:")

label1.grid(row=0, column=0)
label2.grid(row=1, column=0)
label3.grid(row=2, column=0)

# Cuadros de texto
textbox1 = tk.Text(ventana, height=1, width=30)
textbox2 = tk.Text(ventana, height=1, width=30)
textbox3 = tk.Text(ventana, height=1, width=30)

textbox1.grid(row=0, column=1)
textbox2.grid(row=1, column=1)
textbox3.grid(row=2, column=1)

# Opción para elegir el sitio web (GitHub o Twitter)
opcion_var = tk.IntVar()
opcion_var.set(1)
opcion_github = tk.Radiobutton(ventana, text="GitHub", variable=opcion_var, value=1)
opcion_twitter = tk.Radiobutton(ventana, text="Twitter", variable=opcion_var, value=2)

opcion_github.grid(row=3, column=0)
opcion_twitter.grid(row=3, column=1)

# Botón para mostrar información
boton_mostrar = tk.Button(ventana, text="Mostrar Información", command=mostrar_informacion)
boton_mostrar.grid(row=4, column=0, columnspan=2)

# Etiqueta para mostrar información
label_info = tk.Label(ventana, text="", wraplength=300, justify="left")
label_info.grid(row=5, column=0, columnspan=2)

ventana.mainloop()
