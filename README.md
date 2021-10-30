# Grupo 2
* SGARBI, DONNA 15934/1
* Valentin Colato 15655/7
* Nazareno Moresco 16041/5
* Franco Bebczuk 16360/7

# Proyecto de Software - Aplicación de ejemplo

Aplicación de ejemplo para la cátedra de Proyecto de Software de la Facultad de Informática de la U.N.L.P.

## Iniciar ambiente

### Requisitos

- python3
- virtualenv

### Ejecución

```bash
$ virtualenv -p python3 venv
# Para iniciar el entorno virtual
$ . venv/bin/activate
# Instalar las dependencias dentro del entorno virtual
$ pip install -r requirements.txt
# En el directorio raiz
$ FLASK_ENV=development python run.py
```

Para salir del entorno virtal, ejecutar:

```bash
$ deactivate
```

## Estructura de carpetas del proyecto

```bash
config            # Módulo de donde se obtienen las variables de configuración
helpers           # Módulo donde se colocan funciones auxiliares para varias partes del código
models            # Módulo con la lógica de negocio de la aplicación y la conexión a la base de datos
resources         # Módulo con los controladores de la aplicación (parte web)
templates         # Módulo con los templates
db.py             # Instancia de base de datos
__init__.py       # Instancia de la aplicación y ruteo
```

## Migraciones

Si necesitas agregar una nueva columna o tabla en la base de datos, como por ejemplo agregar un atributo en el modelo, deberías crear una migracion para este cambio.
Una migracion podria verse como la actualizacion de los cambios en el modelo a la base de datos.

Una vez realizado nuestro cambio en el modelo ejecutaremos el siguiente comando:
* `flask db migrate`

Y listo, eso creará los archivos necesarios para que se corran las migraciones.

#### Consideraciones sobre migraciones

Tener en cuenta que por la implementacion actual, cada vez que se inicia la aplicacion se corre las migraciones.
Esto es un "hack" para no modificar el script de deploy del servidor en produccion.

Realmente solo es necesario que se ejecute cuando hay nuevas migraciones, no siempre.
Otra consideracion es que las migraciones deben versionarse, es parte del codigo fuente.

Si hay algun error en la migracion basta con borrar el archivo que se genera por esta, pero solo si ya se ejecuto, la base de datos va a tener este cambio lo que puede traer problemas. En este caso habria que hacer algun equivalente a un "rollback" ( dehacer los cambios, en flask-migrate se llama downgrade )

## Setup de la aplicacion

.env de ejemplo
```
LOCAL_DB_HOST = localhost
LOCAL_DB_USER = user
LOCAL_DB_PASS = pass
LOCAL_DB_NAME = proyecto

FLASK_ENV=development
```

### Pylint

Usamos pylint para formatear el estilo del código para correrlo hacer `pylint ./app`

### Seed

Hace poco se utilizaba como seed, para popular la bd, un script SQL que se levantaba desde PhpMyAdmin, la desgracia no tardo mucho en presentarse, se podría hallar mas expresividad en una papa que en ese script, es por eso que presentamos el nuevo, moderno y elegante seed de python.
Ventajas:
  * Mas expresividad.
  * El script se llama desde la inicializacion.
  * Resistente a registros prexistentes
