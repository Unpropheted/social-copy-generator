# Social Copy Generator

Aplicación local para generar textos promocionales para redes sociales a partir de una imagen.

El proyecto utiliza un modelo multimodal de inteligencia artificial ejecutado localmente mediante Ollama. La aplicación analiza la imagen proporcionada y genera un copy en español siguiendo instrucciones definidas por el usuario.

## Características

* Análisis de imágenes mediante un modelo multimodal.
* Generación automática de copy en español.
* Procesamiento automático de imágenes grandes.
* Validación de archivos de entrada.
* Manejo de errores de conexión con Ollama.
* Guardado automático del copy generado en un archivo `.txt`.
* Ejecución completamente local, sin depender de una API externa para la generación del texto.

## Tecnologías

* Python
* Ollama
* Qwen3-VL
* Pillow
* Requests

## Estructura del proyecto

```text
social-copy-generator/
├── images/
├── outputs/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── image_processor.py
│   ├── copy_generator.py
│   ├── ollama_client.py
│   └── output.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Requisitos

* Python 3
* Ollama
* Modelo `qwen3-vl:4b-instruct`

## Instalación

Clona el repositorio y entra en la carpeta del proyecto.

Crea un entorno virtual:

```bash
python -m venv .venv
```

Activa el entorno virtual:

### macOS / Linux

```bash
source .venv/bin/activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

Descarga el modelo utilizado por el proyecto:

```bash
ollama pull qwen3-vl:4b-instruct
```

Asegúrate de que Ollama esté ejecutándose.

## Uso

Coloca una imagen en la carpeta `images/` y ejecuta:

```bash
python -m src.main "images/nombre_de_la_imagen.png"
```

La aplicación:

1. Valida la imagen.
2. Comprueba si necesita ser optimizada.
3. Genera el copy mediante Qwen3-VL.
4. Muestra el resultado en la terminal.
5. Guarda el resultado en `outputs/`.

Por ejemplo:

```text
images/AGB 1.png
```

genera:

```text
outputs/AGB 1_copy.txt
```

## Procesamiento de imágenes

Las imágenes cuya dimensión máxima supera los 1280 píxeles se redimensionan automáticamente antes de enviarse al modelo.

La imagen original no se modifica.

## Privacidad

La generación se realiza localmente mediante Ollama. Las imágenes utilizadas por el programa no necesitan enviarse a una API externa para generar el copy.

## Estado del proyecto

Proyecto en desarrollo.

Actualmente se encuentra implementado el flujo básico de:

**imagen → procesamiento → análisis multimodal → generación de copy → archivo de salida**

