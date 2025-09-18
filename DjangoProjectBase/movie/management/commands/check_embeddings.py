import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Verifica que los embeddings se recuperen correctamente desde la base de datos"

    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        for movie in movies:
            try:
                # 📥 Recupera el campo binario y conviértelo a vector numpy
                embedding_vector = np.frombuffer(movie.emb, dtype=np.float32)

                # 📊 Muestra solo los primeros 5 valores para inspección
                self.stdout.write(f"{movie.title}: {embedding_vector[:5]} ... (len={len(embedding_vector)})")

            except Exception as e:
                self.stderr.write(f"❌ Error con {movie.title}: {e}")
        self.stdout.write(self.style.SUCCESS("✅ Verificación de embeddings completada"))
        