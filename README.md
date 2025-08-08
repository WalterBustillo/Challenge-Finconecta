# Challenge-Finconecta
Part 1: Coding Exercises

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
    Item - str
    Quantity - Numeric
    Price Per Unit - float
    Total Spent - float
    Payment Method - str
    Location - str
    Transaction Date - date