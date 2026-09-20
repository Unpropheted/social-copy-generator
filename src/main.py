import sys
from pathlib import Path

from src.copy_generator import create_copy
from src.image_processor import validate_image, prepare_image
from src.output import save_copy, save_copies


IMAGE_DIR = Path("images")

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}


def process_image(image_path):
    is_valid, error_message = validate_image(image_path)

    if not is_valid:
        raise ValueError(error_message)

    prepared_image = prepare_image(image_path)

    copy = create_copy(prepared_image)

    return copy


def process_post(image_paths):
    prepared_images = []

    for image_path in image_paths:
        is_valid, error_message = validate_image(image_path)

        if not is_valid:
            raise ValueError(error_message)

        prepared_image = prepare_image(image_path)
        prepared_images.append(prepared_image)

    copy = create_copy(prepared_images)

    return copy


def process_images():
    posts = []

    # Imágenes individuales directamente dentro de images/
    individual_images = sorted(
        path for path in IMAGE_DIR.iterdir()
        if path.is_file()
        and path.suffix.lower() in ALLOWED_EXTENSIONS
        and not path.stem.endswith("_small")
    )

    for image_path in individual_images:
        posts.append([image_path])

    # Carpetas: cada carpeta representa un post/carrusel
    post_directories = sorted(
        path for path in IMAGE_DIR.iterdir()
        if path.is_dir()
    )

    for post_directory in post_directories:
        images = sorted(
            path for path in post_directory.iterdir()
            if path.is_file()
            and path.suffix.lower() in ALLOWED_EXTENSIONS
            and not path.stem.endswith("_small")
        )

        if images:
            posts.append(images)

    if not posts:
        raise ValueError(
            "No se encontraron imágenes ni posts en la carpeta images."
        )

    copies = []
    errors = []

    for index, post_images in enumerate(posts, start=1):
        if len(post_images) == 1:
            print(
                f"\n[{index}/{len(posts)}] "
                f"Procesando: {post_images[0].name}"
            )
        else:
            print(
                f"\n[{index}/{len(posts)}] "
                f"Procesando carrusel con "
                f"{len(post_images)} imágenes:"
            )

            for image_path in post_images:
                print(f"  - {image_path.name}")

        try:
            if len(post_images) == 1:
                copy = process_image(post_images[0])

            else:
                copy = process_post(post_images)

            copies.append((post_images, copy))

            print("✓ Copy generado")

        except (ValueError, RuntimeError) as error:
            errors.append((post_images, str(error)))

            print(f"✗ Error: {error}")

    return copies, errors


def main():
    if len(sys.argv) >= 2:
        image_path = sys.argv[1]

        try:
            copy = process_image(image_path)
            output_path = save_copy(copy, image_path)

        except ValueError as error:
            print(f"Error: {error}")
            return

        except RuntimeError as error:
            print(f"Error: {error}")
            return

        print("\n--- COPY GENERADO ---\n")
        print(copy)
        print(f"\nCopy guardado en: {output_path}")

        return

    try:
        copies, errors = process_images()

    except ValueError as error:
        print(f"Error: {error}")
        return

    output_path = save_copies(copies)

    print("\n========================================")
    print("PROCESAMIENTO COMPLETADO")
    print("========================================")

    print(f"\nPosts procesados: {len(copies)}")
    print(f"Errores: {len(errors)}")
    print(f"Documento generado: {output_path}")

    if errors:
        print("\n--- POSTS CON ERROR ---")

        for image_paths, error in errors:
            if len(image_paths) == 1:
                print(f"\nImagen: {image_paths[0].name}")

            else:
                print("\nCarrusel:")

                for image_path in image_paths:
                    print(f"  - {image_path.name}")

            print(f"  Error: {error}")


if __name__ == "__main__":
    main()
