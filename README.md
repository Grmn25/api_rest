# API ECOMMERCE FLASK

## Configuración del Entorno de Desarrollo

1. Cree un entorno virtual de Python utilizando una de las siguientes opciones:

   - Utilizando `virtualenv`:
     ```bash
     pip install virtualenv
     ```

   - Utilizando `venv` (dependiendo de su versión de Python):
     ```bash
     pip install venv
     ```

2. Active el entorno virtual de Python:
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En consola Git:
     ```bash
     . venv/Scripts/activate
     ```

## Instalación de Dependencias

3. Instale las dependencias del proyecto desde el archivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt

## Instalación y configuración de base de datos

4. Instale PostgreSQL y configure su base de datos.

5. En el archivo .env, proporcione la información necesaria para la conexión a la base de datos. Debe configurar las siguientes variables de entorno:
  ```
  DB_HOST=nombre_de_host
  DB_USER=nombre_de_usuario
  DB_PASSWORD=contraseña
  DB_NAME=nombre_de_base_de_datos
  ```
## Levantar API
6. Ejecutar el siguiente comando:
    ```
    uvicorn app.main:app --reload
  ```
