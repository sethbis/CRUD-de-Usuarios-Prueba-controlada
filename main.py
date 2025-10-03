from fastapi import FastAPI
from sqlmodel import SQLModel
from typing import Optional
import random

app = FastAPI()

# --- Modelos de Datos ---
class Usuario(SQLModel):
    id: int
    nombre_usuario: str
    contrasena: str
    email: Optional[str] = None
    is_active: bool

class UsuarioLogin(SQLModel):
    nombre_usuario: str
    contrasena: str

class CrearUsuario(SQLModel):
    nombre_usuario: str
    contrasena: str
    email: Optional[str] = None

    def crear_usuario_nuevo(self):
        return {
            "id": random.randint(10000, 99999),
            "nombre_usuario": self.nombre_usuario,
            "contrasena": self.contrasena,  
            "email": self.email,
            "is_active": True
        }

usuarios_db = [
    {"id": 10001, "nombre_usuario": "admin", "contrasena": "123", "email": None, "is_active": True},
    {"id": 10002, "nombre_usuario": "a", "contrasena": "g1", "email": None, "is_active": True}
]

# --- Endpoints ---
@app.get("/")
def leer_raiz():
    return {"Hello": "World"}

@app.post("/login")
def iniciar_sesion_post(usuario_data: UsuarioLogin):
    nombre_usuario = usuario_data.nombre_usuario
    contrasena = usuario_data.contrasena
    for u in usuarios_db:
        if u["nombre_usuario"] == nombre_usuario and u["contrasena"] == contrasena:
            return {"mensaje": "Login correcto", "usuario": u["nombre_usuario"]}
    return {"mensaje": "Credenciales inválidas"}

@app.post("/users")
def crear_usuario(usuario: CrearUsuario):
    nuevo = usuario.crear_usuario_nuevo()
    usuarios_db.append(nuevo)
    return {"mensaje": "Usuario creado", "usuario": nuevo}

@app.get("/users")
def listar_usuarios():
    return {"usuarios": usuarios_db}

@app.get("/users/{usuario_id}")
def obtener_usuario(usuario_id: int):
    for u in usuarios_db:
        if u.get("id") == usuario_id:
            return u
    return {"mensaje": f"Usuario con id {usuario_id} no encontrado"}

@app.put("/users/{usuario_id}")
def actualizar_usuario(usuario_id: int, datos: dict):
    for u in usuarios_db:
        if u.get("id") == usuario_id:
            # No actualizamos la contraseña con este método por seguridad
            u.update({k: v for k, v in datos.items() if k != "contrasena"})
            return {"mensaje": "Usuario actualizado", "usuario": u}
    return {"mensaje": "Usuario no encontrado"}

@app.delete("/users/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    for u in usuarios_db:
        if u.get("id") == usuario_id:
            usuarios_db.remove(u)
            return {"mensaje": "Usuario eliminado"}
    return {"mensaje": "Usuario no encontrado"}