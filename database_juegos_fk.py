import sqlite3

"""Inicializacion de la Base de datos (DB) con sqlite3 (SQL crudo) - RELACION FK (1:N)"""
# Creando (Si no existe) y conectandose a la DB
db = sqlite3.connect("db_fk_sqlite.sqlite3")
cursor = db.cursor()

# Importante: sqlite3 no aplica las FK ni el ON DELETE CASCADE hasta que se lo pidas
cursor.execute("PRAGMA foreign_keys = ON")

# Un category tiene MUCHAS preguntas (1:N) -> la FK vive en la tabla hija (question)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS category(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS question(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texto TEXT NOT NULL,
        correcta INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE
    )
""")


def _obtener_category(category_id):
    cursor.execute("SELECT id FROM category WHERE id = ?", (category_id,))
    return cursor.fetchone()


# --- C: CREAR (Insertar registros) ---
def crear_category(titulo):
    cursor.execute("INSERT INTO category (titulo) VALUES (?)", (titulo,))
    db.commit()
    print(f"category '{titulo}' agregado con éxito.")
    return cursor.lastrowid


def crear_pregunta(category_id, texto, correcta):
    if _obtener_category(category_id) is None:
        print(f"No existe un category con ID {category_id}.")
        return
    cursor.execute(
        "INSERT INTO question (texto, correcta, category_id) VALUES (?, ?, ?)",
        (texto, correcta, category_id),
    )
    db.commit()
    print(f"Pregunta agregada al category con ID {category_id}.")
    return cursor.lastrowid


# --- R: LEER (Consultar registros) ---
def leer_category():
    # LEFT JOIN para traer los categoryzes aunque no tengan preguntas
    cursor.execute("""
        SELECT category.id, category.titulo, question.id, question.texto, question.correcta
        FROM category
        LEFT JOIN question ON question.category_id = category.id
        ORDER BY category.id, question.id
    """)
    print("\n--- Lista de categoryzes (con sus preguntas) ---")
    category_actual = None
    for category_id, titulo, p_id, texto, correcta in cursor.fetchall():
        # El ORDER BY agrupa las preguntas del mismo category: el titulo se imprime una sola vez
        if category_id != category_actual:
            print(f"category #{category_id}: {titulo}")
            category_actual = category_id
        if p_id is not None:
            print(f"   - #{p_id} {texto} | Correcta: {correcta}")
    print("------------------------------------------\n")


def leer_preguntas_de_category(category_id):
    cursor.execute(
        "SELECT id, texto FROM question WHERE category_id = ? ORDER BY id", (category_id,)
    )
    print(f"\n--- Preguntas del category con ID {category_id} ---")
    for p_id, texto in cursor.fetchall():
        print(f"#{p_id} {texto}")
    print("-------------------------------------\n")


# --- U: ACTUALIZAR (Modificar registros) ---
def actualizar_category(category_id, nuevo_titulo):
    if _obtener_category(category_id) is None:
        print(f"No existe un category con ID {category_id}.")
        return
    cursor.execute("UPDATE category SET titulo = ? WHERE id = ?", (nuevo_titulo, category_id))
    db.commit()
    print(f"category con ID {category_id} actualizado.")


def mover_pregunta(pregunta_id, nuevo_category_id):
    # Cambiar la FK: la pregunta pasa a pertenecer a otro category
    if _obtener_category(nuevo_category_id) is None:
        print(f"No existe un category con ID {nuevo_category_id}.")
        return
    cursor.execute(
        "UPDATE question SET category_id = ? WHERE id = ?", (nuevo_category_id, pregunta_id)
    )
    db.commit()
    print(f"Pregunta #{pregunta_id} movida al category con ID {nuevo_category_id}.")


# --- D: ELIMINAR (Borrar registros) ---
def eliminar_pregunta(pregunta_id):
    cursor.execute("DELETE FROM question WHERE id = ?", (pregunta_id,))
    db.commit()
    print(f"Pregunta #{pregunta_id} eliminada.")


def eliminar_category(category_id):
    # El ON DELETE CASCADE de la FK borra tambien las preguntas del category
    cursor.execute("DELETE FROM category WHERE id = ?", (category_id,))
    db.commit()
    print(f"category con ID {category_id} eliminado (y sus preguntas).")
