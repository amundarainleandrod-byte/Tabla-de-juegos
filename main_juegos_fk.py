import database_juegos_fk

# Crear dos categoryzes
q1 = database_juegos_fk.crear_category("category de fps")
q2 = database_juegos_fk.crear_category("category de platformer")

# Crear preguntas ya asignadas a un category (FK)
p1 = database_juegos_fk.crear_pregunta(q1, "Cual es el año de lanzamiento del primer call of duty?",2003)
p2 = database_juegos_fk.crear_pregunta(q1, "Quien es el villano principal de Call Of Duty Black Ops 2", 'Raul Menendez')
p3 = database_juegos_fk.crear_pregunta(q2, "Quien es el actor de voz de Mario en la franquicia Mario Bros?", '	Charles Martinet')

# Leer la relacion con un JOIN: un category con sus muchas preguntas
database_juegos_fk.leer_category()

# Filtrar por la FK
database_juegos_fk.leer_preguntas_de_category(q1)

# Cerrar la conexion al terminar
database_juegos_fk.db.close()
