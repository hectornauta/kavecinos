**1 - Tener instalado Python3 y añadido en el PATH de Windows**
* Bajar Python

**2 - Crear entorno**
* Moverse a /kavecinos/
* Comando python -m venv entorno

**3 - Activar entorno (hacerse cada vez que se desea agregar cosas con Python)**
* Moverse a /kavecinos/
* Comando .\entorno\Scripts\activate

**4 - Instalar paquetes (sólo una vez y luego de instalar y activar el entorno)**
* Moverse a /kavecinos/
* Comando pip install PyQt5
* Comando pip install matplotlib
* Comando pip install pyqt5-tools (si se desea desarollar la aplicación)

**5 - Cómo ejecutar el programa**
* Moverse a /kavecinos/
* Activar entorno virtual
* Moverse a /kavecinos/src
* Comando python .\QT_Main.py

**Creación de widgets**
* Moverse a /kavecinos/src/UI
* Comando pyuic5 -x widget.ui -o widget_UI.py

**Desarrollo de la lógica de un widget**
* Crear un archivo llamado widget.py
* Es aquí donde irán los eventos y las acciones que se hacen en el mismo

**Probar si anduvo el widget**
* Moverse a /kavecinos/src/UI
* Comando python nombre_del_widget.py
* Ver errores en la consola

