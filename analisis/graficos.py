"""Genera los gráficos de la encuesta con la paleta de la presentación.

Uso: python analisis/graficos.py   (después de analisis/encuesta.py)
Salida: informe/assets/images/*.pdf (informe) y analisis/png/*.png (presentación)
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

RAIZ = Path(__file__).resolve().parent.parent
DATOS = json.loads((RAIZ / "analisis" / "resultados.json").read_text(encoding="utf-8"))
SAL_PDF = RAIZ / "informe" / "assets" / "images"
SAL_PNG = RAIZ / "analisis" / "png"
SAL_PDF.mkdir(parents=True, exist_ok=True)
SAL_PNG.mkdir(parents=True, exist_ok=True)

# Paleta de la presentación Envejecer Mejor
VERDE = "#78963A"      # barras
ROSADO = "#D9628F"     # barra destacada
TEXTO = "#3F5520"      # oliva oscuro para etiquetas
TEXTO_SUAVE = "#55722A"
GUIA = "#B4D97A"       # verde claro para la línea base

plt.rcParams.update({
    "font.family": ["Calibri", "Carlito", "DejaVu Sans"],
    "font.size": 10.5,
    "text.color": TEXTO,
    "axes.labelcolor": TEXTO,
    "xtick.color": TEXTO_SUAVE,
    "ytick.color": TEXTO,
    "pdf.fonttype": 42,
})

ETIQUETAS = {
    "Le pregunto a un médico u otro profesional de salud": "Médico u otro profesional",
    "Busco en Google": "Google",
    "Veo videos en YouTube": "YouTube",
    "Redes sociales (Facebook, Instagram, TikTok)": "Redes sociales",
    "Le pregunto a un asistente de inteligencia artificial (ChatGPT u otro)": "Asistente de IA",
    "Uso aplicaciones de salud o ejercicio": "Aplicaciones de salud",
    "No suelo buscar información": "No suelo buscar",
    "Le pregunto a familiares o amigos": "Familiares o amigos",
    "Viendo televisión o usando el celular o computador": "Frente a pantallas",
    "En traslados (auto, micro, metro)": "En traslados",
    "Descansando o durmiendo siesta": "Descansando o siesta",
    "Otro: Después de almuerzo": "Después de almuerzo",
    "Costo (gimnasio, clases, implementos)": "Costo",
    "Dolor, lesiones o problemas de salud": "Dolor o lesiones",
    "Cansancio o falta de energía": "Cansancio",
    "No tengo lugares cercanos o seguros": "Sin lugares cercanos",
    "No sé bien qué ejercicios hacer": "No sé qué ejercicios hacer",
    "Enfermedades crónicas (diabetes, presión alta, corazón)": "Enfermedades crónicas",
    "Perder independencia (depender de otros)": "Perder independencia",
    "Caídas o problemas de equilibrio": "Caídas o equilibrio",
    "Dolor de articulaciones o espalda": "Dolor de articulaciones",
    "Labores del hogar o cuidado de familiares": "Hogar o cuidado",
    "Trabajo independiente o emprendimiento": "Independiente",
    "Trabajo a tiempo completo": "Tiempo completo",
    "Trabajo part-time": "Part-time",
    "Una rutina guiada y fácil de seguir": "Rutina guiada",
    "Me impiden hacer algunas cosas": "Me impiden hacer cosas",
    "Entre 2 horas y media y 5 horas a la semana": "2 h 30 a 5 h (OMS)",
    "Entre 1 y 2 horas a la semana": "1 a 2 h",
    "Menos de 1 hora a la semana": "Menos de 1 h",
    "Más de 5 horas a la semana": "Más de 5 h",
}


def pct(v, base):
    return str(round(100 * v / base))


def barras(ax, clave, orden=None, destacar=(), titulo=None):
    d = DATOS[clave]
    base, conteo = d["base"], d["conteo"]
    items = [(k, conteo.get(k, 0)) for k in orden] if orden else list(conteo.items())
    items = items[::-1]  # el primero queda arriba
    nombres = [ETIQUETAS.get(k, k) for k, _ in items]
    tope = base
    for i, (k, v) in enumerate(items):
        color = ROSADO if k in destacar else VERDE
        if v > 0:
            ax.add_patch(FancyBboxPatch((0, i - 0.32), v, 0.64,
                                        boxstyle="round,pad=0,rounding_size=0.1",
                                        mutation_aspect=1 / (tope / 6), linewidth=0, facecolor=color))
        ax.text(v + tope * 0.015, i, f"{v}  ({pct(v, base)} %)", va="center", ha="left",
                fontsize=10, color=TEXTO)
    ax.set_yticks(range(len(items)), nombres)
    ax.set_xlim(0, tope * 1.25)
    ax.set_ylim(-0.6, len(items) - 0.4)
    ax.set_xticks([])
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(GUIA)
    ax.spines["left"].set_linewidth(1.5)
    ax.tick_params(axis="y", length=0, pad=6)
    if titulo:
        ax.set_title(f"{titulo}  ·  {base} personas", loc="left", fontsize=11,
                     fontweight="bold", color=TEXTO, pad=8)


def figura(nombre, paneles, alto_por_barra=0.34, ancho=6.3):
    filas = [len(p["orden"]) if p.get("orden") else len(DATOS[p["clave"]]["conteo"]) for p in paneles]
    alto = sum(f * alto_por_barra + 0.7 for f in filas)
    fig, axes = plt.subplots(len(paneles), 1, figsize=(ancho, alto),
                             gridspec_kw={"height_ratios": [f + 1.4 for f in filas]})
    if len(paneles) == 1:
        axes = [axes]
    for ax, p in zip(axes, paneles):
        barras(ax, p["clave"], p.get("orden"), p.get("destacar", ()), p.get("titulo"))
    fig.tight_layout(h_pad=1.6)
    fig.savefig(SAL_PDF / f"{nombre}.pdf", bbox_inches="tight")
    fig.savefig(SAL_PNG / f"{nombre}.png", dpi=250, bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("ok", nombre)


EDADES = ["40 a 44 años", "45 a 49 años", "50 a 54 años", "55 a 59 años"]
SENTADO = ["Menos de 4 horas", "Entre 4 y 6 horas", "Entre 7 y 9 horas", "10 horas o más"]
AFECTAN = ["Nada", "Un poco", "Bastante", "Me impiden hacer algunas cosas"]
IDEAL = ["Menos de 1 hora a la semana", "Entre 1 y 2 horas a la semana",
         "Entre 2 horas y media y 5 horas a la semana", "Más de 5 horas a la semana", "No sé"]
CONOCE = ["Sí, la conozco", "Tengo una idea general", "No la conozco"]
CONFIANZA = ["Muy confiable", "Bastante confiable", "Poco confiable", "No suelo buscar información"]
IMPEDIMENTOS = ["Falta de motivación", "Falta de tiempo", "Cansancio o falta de energía",
                "Dolor, lesiones o problemas de salud"]

if __name__ == "__main__":
    figura("perfil", [
        {"clave": "edad", "orden": EDADES, "titulo": "Edad"},
        {"clave": "ocupacion", "titulo": "Actividad principal"},
    ])
    figura("sedentarismo", [
        {"clave": "sentado", "orden": SENTADO, "titulo": "Horas diarias sentado o en reposo"},
        {"clave": "momentos_sentado", "titulo": "Momentos en que ocurre (selección múltiple)"},
    ])
    figura("barreras", [
        {"clave": "impedimento", "orden": IMPEDIMENTOS, "titulo": "Mayor impedimento para hacer más ejercicio",
         "destacar": ("Falta de motivación", "Falta de tiempo")},
        {"clave": "razones", "titulo": "Razones del poco ejercicio (rutina insuficiente o duda)"},
    ])
    figura("motivaciones", [
        {"clave": "motivaciones", "titulo": "Qué los motivaría a moverse (hasta 3 opciones)",
         "destacar": ("Cuidar o mejorar mi salud",)},
    ])
    figura("fuentes", [
        {"clave": "fuentes", "titulo": "Dónde buscan información de salud (selección múltiple)",
         "destacar": ("Busco en Google", "Le pregunto a un médico u otro profesional de salud")},
        {"clave": "confianza", "orden": CONFIANZA, "titulo": "Qué tan confiable les parece esa información"},
    ])
    figura("cambios", [
        {"clave": "en_que_cambios", "titulo": "En qué notan cambios",
         "destacar": ("Niveles de energía",)},
        {"clave": "afectan", "orden": AFECTAN, "titulo": "Cuánto les afectan esos cambios"},
    ])
    figura("preocupaciones", [
        {"clave": "preocupacion", "titulo": "Lo que más les preocupa de envejecer"},
        {"clave": "medidas", "titulo": "Medidas que toman (quienes dicen prevenir)",
         "destacar": ("Hago ejercicio regularmente",)},
    ])
    figura("recomendacion", [
        {"clave": "conoce_recomendacion", "orden": CONOCE,
         "titulo": "¿Conoce la recomendación de ejercicio para su edad?"},
        {"clave": "tiempo_ideal", "orden": IDEAL, "titulo": "Tiempo de actividad física que consideran ideal",
         "destacar": ("Entre 2 horas y media y 5 horas a la semana",)},
    ])
