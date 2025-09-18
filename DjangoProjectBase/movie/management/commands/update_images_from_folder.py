import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Update movie images in the database from local folder (media/movie/images/)"

    def handle(self, *args, **kwargs):
        # 📂 Carpeta donde están guardadas las imágenes
        images_folder = os.path.join('media', 'movie', 'images')

        if not os.path.exists(images_folder):
            self.stderr.write(f"❌ Folder '{images_folder}' not found.")
            return

        updated_count = 0
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies in DB.")

        for movie in movies:
            try:
                # Nombre esperado de la imagen
                image_filename = f"m_{movie.title}.png"
                image_path_full = os.path.join(images_folder, image_filename)

                if os.path.exists(image_path_full):
                    # Guardar ruta relativa en el campo de la DB
                    movie.image = os.path.join('movie/images', image_filename)
                    movie.save()
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f"✅ Updated image for: {movie.title}"))
                else:
                    self.stderr.write(f"⚠️ No image found for: {movie.title}")

            except Exception as e:
                self.stderr.write(f"❌ Failed for {movie.title}: {str(e)}")

        self.stdout.write(self.style.SUCCESS(f"🎉 Finished updating {updated_count} movies with images."))
