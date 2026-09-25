import os
import unicodedata
from datetime import timedelta
from pathlib import Path

import click
from flask import Flask, abort, jsonify, render_template, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)

import data
import icons
from models import Book, Character, Faction, User, db

BASE_DIR = Path(__file__).resolve().parent


def normalize(text: str) -> str:
    """Minúsculas y sin tildes, para que «tiranidos» encuentre «Tiránidos»."""
    text = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def seed():
    for position, faction_data in enumerate(data.FACTIONS):
        payload = dict(faction_data)
        character_names = payload.pop("characters", [])
        book_titles = payload.pop("reading", [])

        faction = Faction(position=position, **payload)
        faction.characters = [
            Character(name=name, position=i) for i, name in enumerate(character_names)
        ]
        faction.books = [
            Book(title=title, position=i) for i, title in enumerate(book_titles)
        ]
        db.session.add(faction)
    db.session.commit()


def create_app():
    app = Flask(__name__)
    (BASE_DIR / "instance").mkdir(exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASE_DIR / 'instance' / 'lore.db'}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.json.ensure_ascii = False  # que la API devuelva tildes tal cual

    # En producción, define JWT_SECRET_KEY como variable de entorno.
    # Sin ella, se genera una de desarrollo (los tokens dejan de valer al reiniciar).
    app.config["JWT_SECRET_KEY"] = os.environ.get(
        "JWT_SECRET_KEY", "clave-de-desarrollo-cambiame-en-produccion-por-una-aleatoria"
    )
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)

    db.init_app(app)
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()
        if db.session.scalar(db.select(db.func.count(Faction.id))) == 0:
            seed()

    @app.context_processor
    def inject_globals():
        return {"SIDES": data.SIDES, "LEVELS": data.LEVELS, "ICONS": icons.ICONS}

    # ------------------------------------------------------------------ páginas
    @app.route("/")
    def index():
        q = request.args.get("q", "").strip()
        nivel = request.args.get("nivel", type=int)

        factions = db.session.scalars(db.select(Faction).order_by(Faction.position)).all()
        if q:
            needle = normalize(q)
            factions = [
                f for f in factions if needle in normalize(f.name) or needle in normalize(f.tagline)
            ]
        if nivel in data.LEVELS:
            factions = [f for f in factions if f.difficulty == nivel]

        grouped = {key: [f for f in factions if f.side == key] for key in data.SIDES}
        return render_template("index.html", grouped=grouped, q=q, nivel=nivel, total=len(factions))

    @app.route("/faccion/<slug>")
    def faction(slug):
        f = db.session.scalar(db.select(Faction).where(Faction.slug == slug))
        if f is None:
            abort(404)

        same_side = db.session.scalars(
            db.select(Faction).where(Faction.side == f.side).order_by(Faction.position)
        ).all()
        i = same_side.index(f)
        prev_f = same_side[i - 1] if i > 0 else None
        next_f = same_side[i + 1] if i < len(same_side) - 1 else None

        rivals = []
        if f.rivals:
            rivals = db.session.scalars(
                db.select(Faction).where(Faction.slug.in_(f.rivals)).order_by(Faction.position)
            ).all()

        return render_template("faction.html", f=f, prev_f=prev_f, next_f=next_f, rivals=rivals)

    @app.route("/empezar")
    def start():
        tastes = []
        for label, slug in data.TASTES:
            f = db.session.scalar(db.select(Faction).where(Faction.slug == slug))
            if f:
                tastes.append((label, f))
        return render_template(
            "start.html", timeline=data.TIMELINE, glossary=data.GLOSSARY, tastes=tastes
        )

    @app.route("/admin/login")
    def admin_login_page():
        return render_template("admin_login.html")

    @app.route("/admin")
    def admin_page():
        factions = db.session.scalars(db.select(Faction).order_by(Faction.position)).all()
        return render_template("admin.html", factions=factions)

    # ------------------------------------------------------------------ Auth (JWT)
    @app.route("/api/auth/login", methods=["POST"])
    def login():
        body = request.get_json(silent=True) or {}
        username = (body.get("username") or "").strip()
        password = body.get("password") or ""

        user = db.session.scalar(db.select(User).where(User.username == username))
        if user is None or not user.check_password(password):
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

        token = create_access_token(identity=user.username)
        return jsonify({"access_token": token, "username": user.username})

    # ------------------------------------------------------------------ API JSON (lectura, pública)
    @app.route("/api/facciones")
    def api_factions():
        factions = db.session.scalars(db.select(Faction).order_by(Faction.position)).all()
        return jsonify([f.to_dict() for f in factions])

    @app.route("/api/facciones/<slug>")
    def api_faction(slug):
        f = db.session.scalar(db.select(Faction).where(Faction.slug == slug))
        if f is None:
            return jsonify({"error": "Facción no encontrada"}), 404
        return jsonify(f.to_dict())

    @app.route("/api/estadisticas")
    def api_stats():
        """Agregados calculados en la base de datos, no en Python."""
        por_bando = db.session.execute(
            db.select(Faction.side, db.func.count(Faction.id)).group_by(Faction.side)
        ).all()
        por_dificultad = db.session.execute(
            db.select(Faction.difficulty, db.func.count(Faction.id)).group_by(Faction.difficulty)
        ).all()
        totales = {
            "total_facciones": db.session.scalar(db.select(db.func.count(Faction.id))),
            "total_personajes": db.session.scalar(db.select(db.func.count(Character.id))),
            "total_libros": db.session.scalar(db.select(db.func.count(Book.id))),
        }

        return jsonify({
            "facciones_por_bando": {side: n for side, n in por_bando},
            "facciones_por_dificultad": {nivel: n for nivel, n in por_dificultad},
            **totales,
        })

    # ------------------------------------------------------------------ API JSON (escritura, protegida)
    def _apply_faction_fields(faction: Faction, body: dict):
        for field in ("name", "side", "tagline", "color", "tone"):
            if field in body:
                setattr(faction, field, body[field])
        if "difficulty" in body:
            faction.difficulty = int(body["difficulty"])
        for field in ("summary", "key_points", "rivals"):
            if field in body:
                value = body[field]
                faction.__setattr__(field, value if isinstance(value, list) else [
                    line.strip() for line in str(value).splitlines() if line.strip()
                ])
        if "characters" in body:
            names = body["characters"]
            if not isinstance(names, list):
                names = [line.strip() for line in str(names).splitlines() if line.strip()]
            faction.characters = [Character(name=n, position=i) for i, n in enumerate(names)]
        if "reading" in body:
            titles = body["reading"]
            if not isinstance(titles, list):
                titles = [line.strip() for line in str(titles).splitlines() if line.strip()]
            faction.books = [Book(title=t, position=i) for i, t in enumerate(titles)]

    @app.route("/api/facciones", methods=["POST"])
    @jwt_required()
    def api_create_faction():
        body = request.get_json(silent=True) or {}
        slug = (body.get("slug") or "").strip()
        if not slug:
            return jsonify({"error": "Falta el slug"}), 400
        if db.session.scalar(db.select(Faction).where(Faction.slug == slug)):
            return jsonify({"error": "Ya existe una facción con ese slug"}), 409

        max_pos = db.session.scalar(db.select(db.func.max(Faction.position))) or 0
        faction = Faction(
            slug=slug, name=body.get("name", slug), side=body.get("side", "imperio"),
            tagline=body.get("tagline", ""), color=body.get("color", "#b8964f"),
            tone=body.get("tone", ""), difficulty=int(body.get("difficulty", 1)),
            position=max_pos + 1, summary=[], key_points=[], rivals=[],
        )
        _apply_faction_fields(faction, body)
        db.session.add(faction)
        db.session.commit()
        return jsonify(faction.to_dict()), 201

    @app.route("/api/facciones/<slug>", methods=["PUT"])
    @jwt_required()
    def api_update_faction(slug):
        faction = db.session.scalar(db.select(Faction).where(Faction.slug == slug))
        if faction is None:
            return jsonify({"error": "Facción no encontrada"}), 404
        body = request.get_json(silent=True) or {}
        _apply_faction_fields(faction, body)
        db.session.commit()
        return jsonify(faction.to_dict())

    @app.route("/api/facciones/<slug>", methods=["DELETE"])
    @jwt_required()
    def api_delete_faction(slug):
        faction = db.session.scalar(db.select(Faction).where(Faction.slug == slug))
        if faction is None:
            return jsonify({"error": "Facción no encontrada"}), 404
        db.session.delete(faction)
        db.session.commit()
        return jsonify({"ok": True})

    @app.route("/api/auth/whoami")
    @jwt_required()
    def whoami():
        return jsonify({"username": get_jwt_identity()})

    @app.errorhandler(404)
    def not_found(_):
        return render_template("404.html"), 404

    # ------------------------------------------------------------------ CLI
    @app.cli.command("reseed")
    def reseed():
        """Borra facciones/personajes/libros y los vuelve a llenar desde data.py."""
        db.session.execute(db.delete(Faction))
        db.session.commit()
        seed()
        click.echo("Base de datos regenerada desde data.py")

    @app.cli.command("create-admin")
    @click.option("--username", prompt=True)
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
    def create_admin(username, password):
        """Crea o actualiza la contraseña de una cuenta de administración."""
        user = db.session.scalar(db.select(User).where(User.username == username))
        if user is None:
            user = User(username=username)
            db.session.add(user)
        user.set_password(password)
        db.session.commit()
        click.echo(f"Cuenta «{username}» lista. Ya puedes entrar por /admin/login")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
