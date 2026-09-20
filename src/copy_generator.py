from pathlib import Path

from src.ollama_client import generate_copy


SINGLE_IMAGE_PROMPT = """
Crea UN SOLO copy breve, natural y atractivo para Facebook e Instagram
a partir de la imagen proporcionada.

Antes de escribir el copy, analiza cuidadosamente la imagen completa.

FASE 1 — IDENTIFICACIÓN:
Identifica internamente:
- El producto, servicio o tema principal.
- Los textos importantes que aparecen en la imagen.
- Las marcas visibles.
- Los nombres de empresas o personas.
- Teléfonos, direcciones y otros datos comerciales.
- Las características visuales relevantes del producto o contenido.

IMPORTANTE:
La información puede estar presente tanto como TEXTO ESCRITO como
como ELEMENTO VISUAL.

Por ejemplo, si una marca aparece claramente en un producto,
considérala información válida aunque no exista un texto adicional
describiendo el producto.

FASE 2 — SELECCIÓN:
Selecciona únicamente la información que:
- sea claramente visible;
- sea relevante para presentar el contenido;
- pueda utilizarse sin inventar información.

Da prioridad a nombres de productos, marcas, empresas, personas,
teléfonos, direcciones y otros datos específicos visibles.

FASE 3 — REDACCIÓN:
Utiliza la información identificada para crear UN SOLO copy breve.

REGLAS DE FIDELIDAD:
- Conserva los nombres propios y marcas tal como aparecen.
- No traduzcas marcas ni nombres propios.
- No sustituyas una marca por un término genérico.
- No inventes nombres.
- No inventes información que no esté presente en la imagen.
- Si un texto no puede leerse con claridad, no lo adivines.
- No conviertas una interpretación visual dudosa en un dato específico.

REGLAS SOBRE INFORMACIÓN COMERCIAL:
- No inventes precios, promociones, descuentos, fechas, horarios,
  disponibilidad o beneficios.
- No inventes características técnicas.
- No afirmes que un producto es nuevo, exclusivo, de alta calidad
  o que está disponible si eso no puede comprobarse en la imagen.
- No agregues información comercial externa.

ESTILO:
- Escribe exclusivamente en español.
- Tono comercial, natural y fácil de leer.
- Copy breve.
- Puedes utilizar emojis relacionados directamente con el contenido.
- Puedes terminar con una llamada a la acción sencilla.
- Evita frases publicitarias genéricas que no aporten información
  comprobable.

FORMATO:
- Devuelve únicamente el copy final.
- No expliques el análisis.
- No incluyas encabezados como "Copy generado:".
"""


CAROUSEL_PROMPT = """
Las imágenes proporcionadas pertenecen al MISMO POST y forman un
ÚNICO carrusel.

Crea UN SOLO copy breve, natural y atractivo para Facebook e Instagram
basado en el conjunto completo de imágenes.

Antes de escribir el copy, analiza TODAS las imágenes.

FASE 1 — ANÁLISIS COMPLETO DEL CARRUSEL:
Identifica internamente:

- El tema o producto principal del carrusel.
- Los productos que aparecen.
- Las marcas visibles en los productos.
- Los textos importantes presentes en cualquiera de las imágenes.
- Los nombres de empresas o personas.
- Teléfonos, direcciones y otros datos comerciales.
- Las características visuales relevantes.

IMPORTANTE:
La información puede estar presente tanto como TEXTO ESCRITO como
como ELEMENTO VISUAL.

Una marca visible directamente sobre un producto debe considerarse
información válida aunque no exista una descripción escrita de ella.

Analiza las imágenes conjuntamente y utiliza la información
complementaria que aporten entre sí.

FASE 2 — SELECCIÓN DE INFORMACIÓN:
Selecciona únicamente información que:
- sea claramente visible;
- pueda comprobarse directamente en las imágenes;
- sea relevante para el copy.

Si las imágenes muestran diferentes productos del mismo carrusel,
puedes mencionarlos conjuntamente cuando exista información visual
suficiente para hacerlo.

Si varias imágenes muestran productos de diferentes marcas,
conserva las marcas correspondientes.

No ignores información visual relevante simplemente porque no esté
escrita como texto.

FASE 3 — REDACCIÓN:
Utiliza la información seleccionada para crear UN SOLO copy.

REGLAS DEL CARRUSEL:
- Analiza todas las imágenes antes de redactar.
- No generes un copy independiente para cada imagen.
- No describas cada imagen por separado.
- Integra la información relevante del conjunto.
- No inventes una relación entre productos que no pueda observarse.
- No inventes productos adicionales.

REGLAS DE FIDELIDAD:
- Conserva marcas, empresas y nombres propios tal como aparecen.
- No traduzcas marcas ni nombres propios.
- No sustituyas una marca por un término genérico.
- No inventes nombres.
- Si un texto no puede leerse con claridad, no lo adivines.
- No conviertas una interpretación visual dudosa en un dato específico.

REGLAS SOBRE INFORMACIÓN COMERCIAL:
- No inventes precios, promociones, descuentos, fechas, horarios,
  disponibilidad o beneficios.
- No inventes características técnicas.
- No afirmes que los productos son nuevos, exclusivos o de alta calidad
  si eso no puede comprobarse en las imágenes.
- No agregues información comercial externa.

ESTILO:
- Escribe exclusivamente en español.
- Tono comercial, natural y fácil de leer.
- Copy breve.
- Puedes utilizar emojis relacionados directamente con el contenido.
- Puedes terminar con una llamada a la acción sencilla.
- Evita frases publicitarias genéricas que no aporten información
  comprobable.

FORMATO:
- Devuelve únicamente UN copy final.
- No generes un copy por cada imagen.
- No expliques el análisis.
- No incluyas encabezados como "Copy generado:".
"""


def create_copy(image_paths):
    if isinstance(image_paths, (str, Path)):
        prompt = SINGLE_IMAGE_PROMPT
    else:
        prompt = CAROUSEL_PROMPT

    return generate_copy(image_paths, prompt)