import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

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
