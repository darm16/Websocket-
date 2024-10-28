# Recuerda ejecutar todo esto es un entorno virtual e instalar todas las dependencias. 

Las puedes instalar todas ejecuentando el comando

``` pip install -r requirements.txt ```
# Para iniciar el servidor
```uvicorn main:app --host 192.168.1.33 --port 8080 --reload ```

##### recuerda cambiar la IP tanto en el comando como en el archivo index.html (en la parte del javascript) por la IP de tu maquina.

Quedaría:
```uvicorn main:app --host 1xx.1xx.x.x --port 8080 --reload ```

## Para iniciar el cliente
simplemente abres el archivo index.html
### No olvides cambiar la ip en este archvo por la IP de tu máquina.

# Recuerda ejecutar siempre en el entorno virtual para garantizar las dependencias.