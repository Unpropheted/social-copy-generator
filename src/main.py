import sys
from pathlib import Path

from src.copy_generator import create_copy
from src.image_processor import validate_image, prepare_image
from src.output import save_copy, save_copies


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


def discover_posts(site_directory):
    posts = []

    # Imágenes directamente dentro del sitio:
    # cada imagen representa una publicación individual.
    individual_images = sorted(
        path for path in site_directory.iterdir()
        if path.is_file()
        and path.suffix.lower() in ALLOWED_EXTENSIONS
        and not path.stem.endswith("_small")
    )

    for image_path in individual_images:
        posts.append([image_path])

    # Carpetas "carrete": cada una representa un único carrusel.
    carousel_directories = sorted(
        path for path in site_directory.iterdir()
        if path.is_dir()
        and path.name.lower().startswith("carrete")
    )

    for carousel_directory in carousel_directories:
        images = sorted(
            path for path in carousel_directory.iterdir()
            if path.is_file()
            and path.suffix.lower() in ALLOWED_EXTENSIONS
            and not path.stem.endswith("_small")
        )

        if images:
            posts.append(images)

    return posts


def discover_sites(main_directory):
    main_directory = Path(main_directory)

    if not main_directory.exists():
        raise ValueError(
            f"La carpeta no existe: {main_directory}"
        )

    if not main_directory.is_dir():
        raise ValueError(
            f"La ruta no corresponde a una carpeta: {main_directory}"
        )

    sites = []

    site_directories = sorted(
        path for path in main_directory.iterdir()
        if path.is_dir()
    )

    for site_directory in site_directories:
        posts = discover_posts(site_directory)

        if posts:
            sites.append(
                (site_directory.name, posts)
            )

    if not sites:
        raise ValueError(
            "No se encontraron sitios con imágenes "
            "en la carpeta principal."
        )

    return sites

def print_site_structure(main_directory):
    sites = discover_sites(main_directory)

    print("\n========================================")
    print("ESTRUCTURA DETECTADA")
    print("========================================")

    for site_name, posts in sites:
        print(f"\nSITIO: {site_name}")

        for index, post_images in enumerate(posts, start=1):

            if len(post_images) == 1:
                print(f"  Publicación {index}: Individual")
                print(f"    - {post_images[0].name}")

            else:
                print(f"  Publicación {index}: Carrusel")

                for image_path in post_images:
                    print(f"    - {image_path.name}")


def process_sites(main_directory):
    sites = discover_sites(main_directory)

    results = []
    errors = []

    total_posts = sum(
        len(posts)
        for _, posts in sites
    )

    current_post = 0

    for site_name, posts in sites:
        print(f"\n{'=' * 50}")
        print(f"SITIO: {site_name}")
        print(f"{'=' * 50}")

        for post_images in posts:
            current_post += 1

            if len(post_images) == 1:
                print(
                    f"\n[{current_post}/{total_posts}] "
                    f"Publicación individual:"
                )
                print(f"  - {post_images[0].name}")

            else:
                print(
                    f"\n[{current_post}/{total_posts}] "
                    f"Carrusel con "
                    f"{len(post_images)} imágenes:"
                )

                for image_path in post_images:
                    print(f"  - {image_path.name}")

            try:
                if len(post_images) == 1:
                    copy = process_image(post_images[0])
                else:
                    copy = process_post(post_images)

                results.append(
                    (site_name, post_images, copy)
                )

                print("✓ Copy generado")

            except (ValueError, RuntimeError) as error:
                errors.append(
                    (site_name, post_images, str(error))
                )

                print(f"✗ Error: {error}")

    return results, errors


def main():
    if len(sys.argv) != 2:
        print(
            "Uso:\n"
            "\n"
            "Para una imagen:\n"
            'python -m src.main "/ruta/imagen.jpg"\n'
            "\n"
            "Para una carpeta principal:\n"
            'python -m src.main "/ruta/CARPETA_PRINCIPAL"'
        )
        return

    input_path = Path(sys.argv[1])

    # ----------------------------------------
    # MODO 1: una sola imagen
    # ----------------------------------------
    if input_path.is_file():
        try:
            copy = process_image(input_path)
            output_path = save_copy(copy, input_path)

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

    # ----------------------------------------
    # MODO 2: carpeta principal
    # ----------------------------------------
    if input_path.is_dir():
        try:
            results, errors = process_sites(input_path)

        except ValueError as error:
            print(f"Error: {error}")
            return

        output_path = save_copies(results)

        print("\n========================================")
        print("PROCESAMIENTO COMPLETADO")
        print("========================================")

        print(f"\nPosts procesados: {len(results)}")
        print(f"Errores: {len(errors)}")
        print(f"Documento generado: {output_path}")

        if errors:
            print("\n--- POSTS CON ERROR ---")

            for site_name, image_paths, error in errors:
                print(f"\nSitio: {site_name}")

                if len(image_paths) == 1:
                    print(f"Imagen: {image_paths[0].name}")

                else:
                    print("Carrusel:")

                    for image_path in image_paths:
                        print(f"  - {image_path.name}")

                print(f"Error: {error}")

        return

    print(f"Error: la ruta no existe: {input_path}")


if __name__ == "__main__":
    main()