# Challenge-Finconecta
## Part 1: Coding Exercises

Instala las librerías necesarias:
    pip install -r requirements.txt


Info sobre la data:

Se descargó el dataset de kaggle: "https://www.kaggle.com/datasets/ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training/data" el cual luego se llamó "sample_data.csv"

Este dataset contiene 8 columnas y 10 000 filas
Las columnas son:

    Transaction ID - Identificador único por transacción
    Item - Nombre del ítem de la transacción
    Quantity - Cantidad por ítem en la transacción
    Price Per Unit - Precio unitario del ítem
    Total Spent - Total de la transacción
    Payment Method - Método de pago
    Location - Locación de donde ocurrio la transacción
    Transaction Date - Fecha de la transacción

Se espera que las columnas tengan los siguientes formatos:

    Transaction ID - Object
    Item - Object
    Quantity - Numeric
    Price Per Unit - float
    Total Spent - float
    Payment Method - Object
    Location - Object
    Transaction Date - date

## ETL Pipeline

Tenemos un código modular, con un entorno de test y conigurable. 

en un archivo .env se tiene todas las configuraciones iniciales para poder lograr el flujo

en la carpeta:
/config
se tiene un archivo pyhon **setting.py** para las configuraciones iniciales para acceder a los demás entornos como ser mongoDB.

En la carpeta /src/util tenemos 2 archivos python:
**logging_config.py**: La configuración inicial para el archivo de log
**validador.py**: Un validador para confirmar el tipo de datos transformados

### Data

La data se encuentra en la carpeta:
/data
Está con el nombre:
sample_data.csv

### ETL

Tenemos todo el proceso ETL en en la carpeta:
/src
En la carpeta tenemos 4 archivos python,
**extract.py**: Para extraer la data desed el archivo csv
**transform.py**: Donde estáel proceso de transformación de data al modelo deseado
**load.py**: Cargar la data a una base de datos Mongodb
**main.py**: Ejecutar todo el proceso ETL

### Test

Finalmente tenemos un la carpta /test 3 archivos python:
**test_extract.py**: Para hacer el test de la extracción de la data
**test_load.py**: Para hacer el test de la carga de la data
**test_transform.py**: Para hacer el test de la carga a mongoDB

## Airflow

Para utilizar el orquestador Airflow se tiene todos los archivos en una carpeta aparte, llamada /AIRFLOW.

Para utilizar AIRFLOW se utilizo un sub sistema de linux (ubuntu 20.04) en una máquina windows. 

Para que funcione se copiaron los archivos de la capeta mencionada en la dirección: 

"\wsl.localhost\Ubuntu-20.04\home\wbustillo\airflow-with-wsl"

en la parte carpeta /dag se tiene un archivo llamado **test.py** que cumple la función del **main.py** del proceso ETL.

Los pasos del proceso ETL, las variables de configuración están en la carpeta /plugin

### Iniciar airflow

Abrir 2 CMD e introducir los siguientes comandos:

1ro:

wsl -d ubuntu-20.04
cd $HOME
source airflow_env/bin/activate
cd $AIRFLOW_HOME
airflow scheduler

2d0:

wsl -d ubuntu-20.04
cd $HOME
source airflow_env/bin/activate
cd $AIRFLOW_HOME
airflow webserver

En el explorador se puede ingresar a airflow en **localhost:808**

En los dags se busca **test** y ahí se tiene el flujo de trabajo

