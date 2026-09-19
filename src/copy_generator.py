from src.ollama_client import generate_copy


PROMPT = """
Crea un copy breve y atractivo para Facebook e Instagram basado en la imagen.

El objetivo es presentar el producto principal de forma comercial y natural.

REGLAS:
- Escribe exclusivamente en español.
- Identifica y menciona el producto principal que aparece en la imagen.
- Describe únicamente características visuales que puedan observarse directamente.
- Puedes hacer que el texto sea atractivo, pero no inventes información comercial.
- No inventes precios, promociones, descuentos, fechas, horarios, teléfonos, redes sociales, beneficios ni características que no aparezcan en la imagen.
- No inventes productos adicionales.
- Conserva los nombres de marcas y las direcciones visibles en la imagen.
- Si aparecen sucursales, puedes incluirlas.
- Puedes utilizar emojis relacionados directamente con el contenido.
- Termina con una llamada a la acción sencilla, sin agregar información nueva.
- No hagas afirmaciones sobre calidad, disponibilidad, precio o beneficios que no puedan comprobarse en la imagen.

Devuelve únicamente el copy final.
"""


def create_copy(image_path):
    return generate_copy(image_path, PROMPT)
