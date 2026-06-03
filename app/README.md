fastapi
uvicorn
supabase==2.3.0
gotrue==1.3.0

--- corre pip install -r requirements.txt en la terminal y quita esta línea 6. Para inicializar el servidor usa uvicorn app.main:app --reload y en el port que te diga que esta corriendo ponle /docs al final

es necesario y recomendado usar un entorno virtual

python -m venv .venv
.venv\Scripts\activate
