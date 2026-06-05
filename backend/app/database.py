from supabase import create_client, Client

SUPABASE_URL = "https://auzhhcffmukbuvhbikit.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF1emhoY2ZmbXVrYnV2aGJpa2l0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg4MDUwMjgsImV4cCI6MjA5NDM4MTAyOH0.BU5TDK9wyszO1NGo84GaNvnw0HgNdv0ZKb48u7udvqA"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# from supabase import trae la librería de Supabase
# SUPABASE_URL y SUPABASE_KEY son las credenciales de tu base de datos, como usuario y contraseña
# create_client crea la conexión a Supabase
# supabase es el objeto que todos los demás archivos usan para hablar con la base de datos


