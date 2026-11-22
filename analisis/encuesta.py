"""Lee las respuestas de la encuesta y calcula las frecuencias que usa el informe.

Uso: python analisis/encuesta.py   (desde la raíz del repo)
No lee ni imprime nombre, apellido ni correo.
"""
import json
from collections import Counter
from pathlib import Path

import openpyxl

RAIZ = Path(__file__).resolve().parent.parent
XLSX = RAIZ / "Actividad física, salud y tecnología (40 a 59 años) (Respuestas).xlsx"

# Opciones del formulario (para separar respuestas múltiples aunque tengan comas)
OPCIONES = {
    6: ["Hipertensión (presión alta)", "Diabetes", "Colesterol o triglicéridos altos", "Artrosis o artritis",
        "Enfermedad respiratoria (asma, EPOC)", "Enfermedad del corazón", "Hipotiroidismo", "Depresión o ansiedad"],
    10: ["En el trabajo", "En traslados (auto, micro, metro)", "Viendo televisión o usando el celular o computador",
         "Durante las comidas", "Descansando o durmiendo siesta"],
    12: ["Falta de tiempo", "No sé bien qué ejercicios hacer", "Cansancio o falta de energía", "Falta de motivación",
         "Dolor, lesiones o problemas de salud", "Costo (gimnasio, clases, implementos)",
         "No tengo lugares cercanos o seguros", "No tengo con quién hacerlo"],
    13: ["Cuidar o mejorar mi salud", "Indicación de un médico", "Bajar de peso o verme mejor", "Tener más energía",
         "Reducir el estrés", "Hacerlo acompañado(a)", "Ver mi progreso o tener metas claras",
         "Una rutina guiada y fácil de seguir"],
    15: ["Le pregunto a un médico u otro profesional de salud", "Busco en Google", "Veo videos en YouTube",
         "Redes sociales (Facebook, Instagram, TikTok)", "Le pregunto a familiares o amigos",
         "Uso aplicaciones de salud o ejercicio",
         "Le pregunto a un asistente de inteligencia artificial (ChatGPT u otro)", "No suelo buscar información"],
    18: ["Fuerza física", "Equilibrio", "Niveles de energía"],
    23: ["Hago ejercicio regularmente", "Cuido mi alimentación", "Me hago controles médicos",
         "Tomo medicamentos o suplementos", "Duermo y descanso mejor"],
}


def separar(col, valor):
    """Devuelve las opciones marcadas; lo que no calza con una opción va como 'Otro: ...'."""
    if not valor:
        return []
    resto = valor
    marcadas = []
    for op in sorted(OPCIONES[col], key=len, reverse=True):
        if op in resto:
            marcadas.append(op)
            resto = resto.replace(op, "")
    resto = resto.replace(",", " ").strip()
    if resto:
        marcadas.append("Otro: " + resto)
    return marcadas


def cargar():
    ws = openpyxl.load_workbook(XLSX, read_only=True).active
    filas = list(ws.iter_rows(min_row=2, values_only=True))
    return [dict(enumerate(f)) for f in filas if f[0] is not None]


def main():
    r = cargar()
    n = len(r)
    out = {"n": n, "fechas": [min(x[0] for x in r).isoformat(), max(x[0] for x in r).isoformat()]}
    simples = {4: "edad", 5: "cronica", 7: "ocupacion", 9: "sentado", 11: "rutina_suficiente", 14: "impedimento",
               16: "confianza", 17: "nota_cambios", 19: "afectan", 21: "preocupacion", 22: "toma_medidas",
               24: "conoce_recomendacion", 26: "tiempo_ideal"}
    for col, nombre in simples.items():
        c = Counter(x[col] for x in r if x.get(col))
        out[nombre] = {"base": sum(c.values()), "conteo": dict(c.most_common())}
    multiples = {6: "cuales_cronicas", 10: "momentos_sentado", 12: "razones", 13: "motivaciones", 15: "fuentes",
                 18: "en_que_cambios", 23: "medidas"}
    for col, nombre in multiples.items():
        vieron = [x for x in r if x.get(col)]
        c = Counter(op for x in vieron for op in separar(col, x[col]))
        out[nombre] = {"base": len(vieron), "conteo": dict(c.most_common())}

    # Cruces que se citan en el informe
    trabajo_completo = [x for x in r if x[7] == "Trabajo a tiempo completo"]
    out["cruces"] = {
        "tiempo_en_tiempo_completo": sum(1 for x in trabajo_completo if x[14] == "Falta de tiempo"),
        "tiempo_total": sum(1 for x in r if x[14] == "Falta de tiempo"),
        "rutina_no_basta_y_sin_medidas": sum(1 for x in r if x[11] == "No" and x[22] == "No"),
        "rutina_no_basta": sum(1 for x in r if x[11] == "No"),
        "cronica_rutina_no_basta": sum(1 for x in r if x[5] == "Sí" and x[11] == "No"),
        "sin_cronica_rutina_no_basta": sum(1 for x in r if x[5] == "No" and x[11] == "No"),
        "medidas_con_ejercicio": sum(1 for x in r if x.get(23) and "Hago ejercicio regularmente" in x[23]),
        "notan_cambios_50_59": sum(1 for x in r if x[4] in ("50 a 54 años", "55 a 59 años") and x[17] == "Sí"),
        "personas_50_59": sum(1 for x in r if x[4] in ("50 a 54 años", "55 a 59 años")),
        "trabajan": sum(1 for x in r if str(x[7]).startswith("Trabajo")),
    }
    print(json.dumps(out, ensure_ascii=False, indent=1))
    (RAIZ / "analisis" / "resultados.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
