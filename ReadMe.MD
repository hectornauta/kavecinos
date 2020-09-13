**1 - Tener instalado Python3 y añadido en el PATH de Windows**
* Bajar Python

**2 - Crear entorno**
* Moverse a /kamedias/
* Comando python -m venv entorno

**3 - Activar entorno (hacerse cada vez que se desea agregar cosas con Python)**
* Moverse a /kamedias/
* Comando .\entorno\Scripts\activate

**4 - Instalar paquetes (sólo una vez y luego de instalar y activar el entorno)**
* Moverse a kamedias/
* Comando pip install PyQt==5.9.2

**Cómo hacer las cosas**

**Hacer widgets**
* Moverse a kamedias/
* Comando designer
* Hacemos las cosas que tengamos que hacer, luego la guardamos en la carpeta UI con un nombre adecuado

**Convertir los widgets en scripts de python (debe hacerse cada vez que se modifica un widget con el designer)**
* Moverse a /kamedias/src/UI
* Comando pyuic5 -x nombre_del_widget.ui -o nombre_del_widget_UI.py

**Crear la lógica de los widgets (acá va la lógica, no en el anterior)**
* Crear un archivo llamado nombre_del_widget.py
* Emplear la lógica utilizando el archivo template.py como base
* Es aquí donde irán los eventos y las acciones que se hacen
<!---
TODO: ampliar esta parte
-->
**Probar si anduvo el widget**
* Moverse a /kamedias/src/UI
* Comando python nombre_del_widget.py
* Ver errores en la consola

**Tutoriales**
* Tutorial de todos los widgets https://coderslegacy.com/python/pyqt-qprogressbar/
* Tutorial de ZetCode http://zetcode.com/gui/pyqt5/
* Proyectos de prueba: https://github.com/learnpyqt/15-minute-apps
* Ejemplos: https://github.com/pyqt/examples
* Español 1 https://medium.com/@hektorprofe/primeros-pasos-en-pyqt-5-y-qt-designer-programas-gráficos-con-python-6161fba46060
* Español 2 https://medium.com/@hektorprofe/widgets-de-pyqt-5-1-ventanas-y-cuadros-de-diálogo-937caf847789
* Tutorial con MVC (lo que haríamos nosotros) https://www.learnpyqt.com/courses/model-views/modelview-architecture/