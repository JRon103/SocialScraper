from datetime import datetime
import json
import matplotlib.pyplot as plt

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
