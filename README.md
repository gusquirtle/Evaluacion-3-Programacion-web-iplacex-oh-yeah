# Encargo 3 – Programación Web (Flask)

Proyecto para la Evaluación de la Unidad N.° 3 de Programación Web (IPLACEX), basado en `TA_6.docx`.

## Requisitos

- Python 3.9 o superior.
- Flask 3.x (incluido en `requirements.txt`).

## Estructura

```text
TA6_Flask_IPLACEX/
├── main.py
├── requirements.txt
├── README.md
├── ENLACE_GITHUB.txt
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── ejercicio1.html
│   ├── ejercicio2.html
│   └── resultado.html
├── static/
│   └── styles.css
└── tests/
    └── test_app.py
```

`base.html` es una plantilla compartida; las cuatro páginas que puede ver el usuario son: menú principal, ejercicio 1, ejercicio 2 y resultados.

## Instalación en Windows (PowerShell)

Abrir la carpeta del proyecto en una terminal y ejecutar:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Si PowerShell impide la activación, se puede usar directamente:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

En Linux o macOS, el entorno se activa con `source .venv/bin/activate`.

Visitar en el navegador: **http://127.0.0.1:5000/**

El servidor usa el modo de depuración solo para las pruebas locales del curso. No se debe publicar con `debug=True`.

## Ejercicios

**Ejercicio 1:** recibe tres notas entre 10 y 70 y asistencia entre 0 y 100. Muestra el promedio y el estado **APROBADO** cuando el promedio es `>= 40` y la asistencia `>= 75`; en caso contrario, muestra **REPROBADO**. Calcula el promedio sin ponderaciones adicionales y lo presenta con dos decimales.

**Ejercicio 2:** recibe tres nombres diferentes, compuestos solo por letras (sin espacios). Muestra el nombre con mayor cantidad de caracteres y esa cantidad. Si hay empate, muestra el primero ingresado; el enunciado no especifica cómo resolver empates.

## Rutas

| Ruta | Método | Uso |
| --- | --- | --- |
| `/` | GET | Menú principal |
| `/ejercicio1` | GET, POST | Mostrar y procesar notas |
| `/ejercicio2` | GET, POST | Mostrar y procesar nombres |
| `/resultado/notas` | GET | Mostrar promedio y aprobación |
| `/resultado/nombres` | GET | Mostrar nombre más largo |

Los formularios utilizan POST. Si los datos son válidos, la aplicación redirige a una página de resultados usando una ruta con parámetro (`<tipo>`). Se guarda el resultado en la sesión del navegador para no colocarlo en la URL. Se usa `abort(404)` si se solicita un tipo de resultado inexistente.

## Pruebas

Desde la carpeta del proyecto, ejecutar:

```powershell
python -m unittest discover -s tests -v
```

## Entrega en Blackboard y GitHub

1. Comprueba que el menú, ambos formularios y sus resultados funcionan.
2. Crea un repositorio propio en GitHub. Desde la carpeta del proyecto, ejecuta:

   ```bash
   git init
   git add .
   git commit -m "Entrega evaluacion 3 Flask"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
   git push -u origin main
   ```

   Sustituye `TU_USUARIO` y `TU_REPOSITORIO` por los valores reales. Si Git solicita autenticación, utiliza el método que GitHub indique para tu cuenta.
3. Reemplaza el contenido de `ENLACE_GITHUB.txt` por la URL **real** del repositorio.
4. Comprime la carpeta del proyecto como `.zip` o `.rar`, **sin incluir `.venv`**.
5. Entrega el archivo comprimido y el archivo de texto con el enlace en Blackboard. **No basta con entregar solo el enlace.**

## Observación

La rúbrica indica cuatro páginas aunque las instrucciones específicas mencionan al menos tres archivos HTML. La implementación incluye cuatro páginas visibles y una plantilla base compartida para cubrir ambos criterios.
