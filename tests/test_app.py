"""Pruebas de los ejercicios y las rutas principales."""

import unittest

from main import app, calcular_promedio, esta_aprobado, obtener_nombre_mas_largo


class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_menu_y_formularios_cargan(self):
        for ruta in ("/", "/ejercicio1", "/ejercicio2"):
            with self.subTest(ruta=ruta):
                self.assertEqual(self.client.get(ruta).status_code, 200)

    def test_resultado_notas_aprobado(self):
        respuesta = self.client.post(
            "/ejercicio1",
            data={"nota1": "55", "nota2": "65", "nota3": "45", "asistencia": "86"},
            follow_redirects=True,
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(b"55.00", respuesta.data)
        self.assertIn(b"APROBADO", respuesta.data)

    def test_aprobacion_en_limite(self):
        respuesta = self.client.post(
            "/ejercicio1",
            data={"nota1": "40", "nota2": "40", "nota3": "40", "asistencia": "75"},
            follow_redirects=True,
        )
        self.assertIn(b"APROBADO", respuesta.data)

    def test_promedio_no_se_redondea_para_aprobar(self):
        self.assertFalse(esta_aprobado(calcular_promedio([39.99, 39.99, 40.01]), 95))

    def test_reprobacion_por_asistencia(self):
        respuesta = self.client.post(
            "/ejercicio1",
            data={"nota1": "60", "nota2": "50", "nota3": "70", "asistencia": "74"},
            follow_redirects=True,
        )
        self.assertIn(b"REPROBADO", respuesta.data)

    def test_reprobacion_por_promedio(self):
        respuesta = self.client.post(
            "/ejercicio1",
            data={"nota1": "30", "nota2": "40", "nota3": "40", "asistencia": "100"},
            follow_redirects=True,
        )
        self.assertIn(b"REPROBADO", respuesta.data)

    def test_notas_fuera_de_rango(self):
        respuesta = self.client.post(
            "/ejercicio1",
            data={"nota1": "71", "nota2": "30", "nota3": "40", "asistencia": "90"},
        )
        self.assertIn(b"entre 10 y 70", respuesta.data)

    def test_asistencia_fuera_de_rango(self):
        respuesta = self.client.post(
            "/ejercicio1",
            data={"nota1": "60", "nota2": "30", "nota3": "40", "asistencia": "101"},
        )
        self.assertIn(b"entre 0 y 100", respuesta.data)

    def test_ejercicio2_nombre_mas_largo(self):
        respuesta = self.client.post(
            "/ejercicio2",
            data={"nombre1": "Felipe", "nombre2": "Juan", "nombre3": "Gustavo"},
            follow_redirects=True,
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(b"Gustavo", respuesta.data)
        self.assertIn(b"7", respuesta.data)

    def test_ejercicio2_nombres_repetidos(self):
        respuesta = self.client.post(
            "/ejercicio2",
            data={"nombre1": "Ana", "nombre2": "ANA", "nombre3": "Pedro"},
        )
        self.assertIn(b"deben ser diferentes", respuesta.data)

    def test_ejercicio2_nombres_con_numeros(self):
        respuesta = self.client.post(
            "/ejercicio2",
            data={"nombre1": "Ana3", "nombre2": "Luis", "nombre3": "Pedro"},
        )
        self.assertIn(b"solo letras", respuesta.data)

    def test_resultado_sin_sesion_redirige_al_inicio(self):
        respuesta = self.client.get("/resultado/notas")
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(respuesta.location, "/")

    def test_resultado_tipo_inexistente_404(self):
        self.assertEqual(self.client.get("/resultado/otro").status_code, 404)

    def test_funciones(self):
        self.assertEqual(calcular_promedio([55, 65, 45]), 55)
        self.assertTrue(esta_aprobado(40, 75))
        self.assertFalse(esta_aprobado(39.99, 80))
        self.assertEqual(obtener_nombre_mas_largo(["Ana", "María", "Pedro"]), "María")


if __name__ == "__main__":
    unittest.main()
