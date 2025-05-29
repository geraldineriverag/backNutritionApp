# NutritionApp Backend

Back-End (Django + DRF) – README.md
API REST con Django 5.2, Django REST Framework y SimpleJWT.

## Requisitos

- Python 3.10+
- PostgreSQL
- virtualenv / venv

## Instalación

1. Clona el repositorio y entra en él:  
   ```bash
   git clone https://github.com/tu-orga/nutritionapp-back.git
   cd nutritionapp-back

2. Crea & activa un entorno virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate

3. Instala dependencias:

   ```bash
   pip install -r requirements.txt

4. Copia el ejemplo de variables de entorno y ajústalas:

   ```bash
   cp .env.example .env

5. Corre migraciones y crea superusuario:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser

6. Configuración en .env
- dotenv
- SECRET_KEY=tu_secret_key
- DEBUG=True
- ALLOWED_HOSTS=localhost,127.0.0.1
- DB_NAME=nutrition_app
- DB_USER=admin_nutrition
- DB_PASSWORD=adnut2106b
- DB_HOST=localhost
- DB_PORT=5432

7. Email SMTP (opcional para notificaciones)
- EMAIL_HOST=smtp.gmail.com
- EMAIL_PORT=587
- EMAIL_HOST_USER=tu_email@gmail.com
- EMAIL_HOST_PASSWORD=tu_app_password
- EMAIL_USE_TLS=True

## Ejecutar servidor
   ```bash
   python manage.py runserver
   Visita http://127.0.0.1:8000/api/docs/ para la documentación Swagger.

