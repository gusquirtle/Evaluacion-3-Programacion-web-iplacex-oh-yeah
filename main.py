"""Encargo 3 - Programación Web: ejercicios con Flask."""

import os

from flask import Flask, abort, redirect, render_template, request, session, url_for

app = Flask(__name__)
# Esta clave predeterminada es solo para ejecutar el ejercicio de forma local.
# En un servidor real se debe definir FLASK_SECRET_KEY en el entorno.
app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY", "clave-solo-para-desarrollo-local"
)


def calcular_promedio(notas):
    """Calcula el promedio aritmético de tres notas."""
    return sum(notas) / len(notas)


def esta_aprobado(promedio, asistencia):
    """Aprueba con promedio >= 40 y asistencia >= 75%."""
    return promedio >= 40 and asistencia >= 75


def obtener_nombre_mas_largo(nombres):
    """Obtiene el nombre más largo; en un empate, devuelve el primero."""
    return max(nombres, key=len)


@app.get("/")
def inicio():
    """Menú de la aplicación."""
    return render_template("index.html")


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    """Recibe tres notas y la asistencia; muestra su resultado."""
    datos = {campo: "" for campo in ("nota1", "nota2", "nota3", "asistencia")}
    error = None

    if request.method == "POST":
        datos = {campo: request.form.get(campo, "").strip() for campo in datos}
        try:
            notas = [float(datos[f"nota{i}"]) for i in range(1, 4)]
            asistencia = float(datos["asistencia"])
        except ValueError:
            error = "Ingresa las tres notas y la asistencia usando valores numéricos."
        else:
            if not all(10 <= nota <= 70 for nota in notas):
                error = "Cada nota debe estar entre 10 y 70."
            elif not 0 <= asistencia <= 100:
                error = "La asistencia debe estar entre 0 y 100 %."
            else:
                promedio = calcular_promedio(notas)
                aprobado = esta_aprobado(promedio, asistencia)
                session["resultado_notas"] = {
                    "promedio": round(promedio, 2),
                    "asistencia": asistencia,
                    "estado": "APROBADO" if aprobado else "REPROBADO",
                }
                return redirect(url_for("resultado", tipo="notas"))

    return render_template("ejercicio1.html", datos=datos, error=error)


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    """Recibe tres nombres diferentes; identifica el de más letras."""
    datos = {campo: "" for campo in ("nombre1", "nombre2", "nombre3")}
    error = None

    if request.method == "POST":
        datos = {campo: request.form.get(campo, "").strip() for campo in datos}
        nombres = list(datos.values())

        if not all(nombre and nombre.isalpha() for nombre in nombres):
            error = "Escribe tres nombres, usando solo letras y sin espacios."
        elif len({nombre.casefold() for nombre in nombres}) != 3:
            error = "Los tres nombres deben ser diferentes."
        else:
            mayor = obtener_nombre_mas_largo(nombres)
            session["resultado_nombres"] = {
                "nombre": mayor,
                "cantidad": len(mayor),
            }
            return redirect(url_for("resultado", tipo="nombres"))

    return render_template("ejercicio2.html", datos=datos, error=error)


@app.get("/resultado/<tipo>")
def resultado(tipo):
    """Página de resultados, con parámetro en la URL."""
    if tipo not in ("notas", "nombres"):
        abort(404)

    clave = "resultado_notas" if tipo == "notas" else "resultado_nombres"
    datos = session.get(clave)
    if datos is None:
        return redirect(url_for("inicio"))

    return render_template("resultado.html", tipo=tipo, datos=datos)


if __name__ == "__main__":
    app.run(debug=True)
