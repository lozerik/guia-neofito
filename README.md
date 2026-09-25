# Guía del Neófito

Web hecha con Flask para introducirse en el lore de cada facción de Warhammer 40.000.
## Puesta en marcha

```bash
python -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abre http://127.0.0.1:5000. La primera vez se crea `instance/lore.db` y se rellena desde `data.py`.

### Panel de administración

Para editar facciones desde el navegador (en vez de tocar `data.py` a mano) hace falta una cuenta:

```bash
flask --app app create-admin
```

Te pedirá usuario y contraseña. Con eso ya puedes entrar en `/admin/login`. La sesión se guarda como un token **JWT** en el navegador (`localStorage`) y caduca a las 8 horas.

En producción, define `JWT_SECRET_KEY` como variable de entorno con un valor aleatorio; si no, se usa una clave de desarrollo fija.

## Estructura

| Archivo | Para qué sirve |
|---|---|
| `app.py` | Rutas, búsqueda, filtros, login JWT, API JSON (lectura pública + escritura protegida), estadísticas y comandos `reseed`/`create-admin` |
| `models.py` | Modelos `Faction`, `Character`, `Book` (relaciones reales) y `User` (login) |
| `icons.py` | Emblemas heráldicos originales en SVG, uno por facción |
| `data.py` | Contenido de partida: facciones, cronología y glosario, usado para el primer `seed()` |
| `templates/` | Plantillas Jinja2, incluido el panel `admin.html` / `admin_login.html` |
| `static/style.css` | Estilos; cada facción define su color con `--f` |

## Rutas

- `/` listado por bando, con búsqueda (`?q=`) y filtro de dificultad (`?nivel=1|2|3`)
- `/faccion/<slug>` ficha de cada facción
- `/empezar` cronología, glosario y guía «¿con quién empiezo?»
- `/admin/login` y `/admin` panel de edición (requiere cuenta)
- `/api/facciones` y `/api/facciones/<slug>` — lectura pública en JSON
- `/api/facciones` (POST), `/api/facciones/<slug>` (PUT/DELETE) — escritura, requiere `Authorization: Bearer <token>`
- `/api/auth/login` (POST) y `/api/auth/whoami` (GET, protegida)
- `/api/estadisticas` — recuentos agregados con SQL (`GROUP BY` por bando y por dificultad)

## Añadir o editar una facción

- **Desde el navegador:** entra en `/admin` con tu cuenta y usa el formulario.
- **Desde código:** añade un diccionario a `FACTIONS` en `data.py` y ejecuta `flask --app app reseed` (esto borra y regenera toda la base de datos desde `data.py`, así que perderás lo que hayas creado solo desde `/admin`).

Los `rivals` son `slug` de otras facciones.

## Ideas para seguir

- Refresh tokens y expiración configurable para el login.
- Migraciones con Flask-Migrate/Alembic en vez de `db.create_all()`.
- Tests con `pytest` (ahora mismo la cobertura viene de pruebas manuales con el cliente de Flask).
- Docker + despliegue real (Render, Railway, Fly.io) con Postgres en vez de SQLite.
- Subfacciones (Capítulos de Marines, Dinastías necronas, Clanes orkos) como otra tabla relacionada.

## Aviso

Proyecto de fans sin ánimo de lucro. Warhammer 40.000 es una marca de Games Workshop. Los textos son resúmenes propios; conviene comprobar los títulos de los libros en la Black Library antes de publicar.
