from werkzeug.security import check_password_hash, generate_password_hash

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Faction(db.Model):
    """Una facción del universo de Warhammer 40.000."""

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    side = db.Column(db.String(20), nullable=False, index=True)  # imperio | caos | xenos
    tagline = db.Column(db.String(200), nullable=False)
    color = db.Column(db.String(7), nullable=False)  # color de acento (#rrggbb)
    tone = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)  # 1 fácil ... 3 veteranos
    position = db.Column(db.Integer, nullable=False, default=0)

    # Listas de texto simples: siguen como JSON, no necesitan tabla propia.
    summary = db.Column(db.JSON, nullable=False, default=list)
    key_points = db.Column(db.JSON, nullable=False, default=list)
    rivals = db.Column(db.JSON, nullable=False, default=list)  # slugs de otras facciones

    # Personajes y libros SÍ tienen entidad propia: relación uno-a-muchos real,
    # en vez de guardarlos como texto suelto dentro de la facción.
    characters = db.relationship(
        "Character", back_populates="faction", cascade="all, delete-orphan",
        order_by="Character.position",
    )
    books = db.relationship(
        "Book", back_populates="faction", cascade="all, delete-orphan",
        order_by="Book.position",
    )

    def to_dict(self):
        return {
            "slug": self.slug,
            "name": self.name,
            "side": self.side,
            "tagline": self.tagline,
            "tone": self.tone,
            "difficulty": self.difficulty,
            "summary": self.summary,
            "key_points": self.key_points,
            "characters": [c.name for c in self.characters],
            "reading": [b.title for b in self.books],
            "rivals": self.rivals,
        }

    def __repr__(self):
        return f"<Faction {self.slug}>"


class Character(db.Model):
    """Un personaje destacado de una facción."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    position = db.Column(db.Integer, nullable=False, default=0)

    faction_id = db.Column(db.Integer, db.ForeignKey("faction.id"), nullable=False)
    faction = db.relationship("Faction", back_populates="characters")

    def __repr__(self):
        return f"<Character {self.name}>"


class Book(db.Model):
    """Una lectura recomendada para introducirse en una facción."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    position = db.Column(db.Integer, nullable=False, default=0)

    faction_id = db.Column(db.Integer, db.ForeignKey("faction.id"), nullable=False)
    faction = db.relationship("Faction", back_populates="books")

    def __repr__(self):
        return f"<Book {self.title}>"


class User(db.Model):
    """Cuenta de administración: quien puede editar facciones desde /admin."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
