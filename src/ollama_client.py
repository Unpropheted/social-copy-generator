import base64
from pathlib import Path

import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3-vl:4b-instruct"


def generate_copy(image_paths, prompt):
    if isinstance(image_paths, (str, Path)):
        image_paths = [image_paths]

    images_base64 = []

    for image_path in image_paths:
        with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(
                image_file.read()
            ).decode("utf-8")

        images_base64.append(image_base64)

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": images_base64
            }
        ],
        "stream": False,
        "think": False,
        "options": {
            "num_ctx": 8192,
            "num_predict": 150
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=300
        )

        response.raise_for_status()

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "No se pudo conectar con Ollama. "
            "Asegúrate de que Ollama esté ejecutándose."
        )

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Ollama tardó demasiado en responder."
        )

    except requests.exceptions.HTTPError:
        raise RuntimeError(
            f"Ollama devolvió un error: {response.text}"
        )

    result = response.json()

    return result["message"]["content"]
