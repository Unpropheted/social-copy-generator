from datetime import datetime
from pathlib import Path


OUTPUT_DIR = Path("outputs")


def save_copy(copy, image_path):
    image_path = Path(image_path)

    OUTPUT_DIR.mkdir(exist_ok=True)

    output_path = OUTPUT_DIR / f"{image_path.stem}_copy.txt"

    output_path.write_text(
        copy,
        encoding="utf-8"
    )

    return output_path


def save_copies(copies):
    OUTPUT_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    output_path = OUTPUT_DIR / f"copys_{timestamp}.txt"

    with output_path.open("w", encoding="utf-8") as file:
        for index, (image_paths, copy) in enumerate(copies, start=1):

            file.write("=" * 50 + "\n")
            file.write(f"POST {index}\n")
            file.write("=" * 50 + "\n\n")

            if len(image_paths) == 1:
                file.write("Tipo: Publicación individual\n")
                file.write(
                    f"Imagen: {image_paths[0].name}\n\n"
                )

            else:
                file.write("Tipo: Carrusel\n")
                file.write("Imágenes:\n")

                for image_path in image_paths:
                    file.write(
                        f"- {image_path.name}\n"
                    )

                file.write("\n")

            file.write("COPY:\n\n")
            file.write(copy.strip())
            file.write("\n\n")

    return output_path