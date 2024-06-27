import pandas as pd

def calcular_ahorros(ingreso_inicial, deposito_mensual, tasa_anual, tasa_impuestos, objetivo, tipo_objetivo, costo_mantenimiento, nombre_archivo):
    """
    Calcula el saldo acumulado con interés compuesto ajustado por impuestos y genera un archivo Excel.

    :param ingreso_inicial: Cantidad inicial ahorrada (en euros)
    :param deposito_mensual: Cantidad mensual ahorrada (en euros)
    :param tasa_anual: Tasa de interés anual (en decimal, por ejemplo, 0.0375 para 3.75%)
    :param tasa_impuestos: Tasa de impuestos anual sobre los intereses (en decimal, por ejemplo, 0.19 para 19%)
    :param objetivo: Saldo o beneficio neto objetivo a alcanzar (en euros)
    :param tipo_objetivo: Tipo de objetivo ('saldo' o 'beneficio')
    :param costo_mantenimiento: Costo mensual de mantenimiento de la cuenta (en euros)
    :param nombre_archivo: Nombre del archivo Excel a generar
    """
    # Constantes
    tasa_mensual = tasa_anual / 12
    tasa_mensual_ajustada = tasa_mensual * (1 - tasa_impuestos)

    # Inicialización de variables
    saldo = ingreso_inicial
    meses = 0
    historial = []

    # Simulación de ahorro mensual
    while (tipo_objetivo == 'saldo' and saldo < objetivo) or (tipo_objetivo == 'beneficio' and saldo - ingreso_inicial - (meses * deposito_mensual) < objetivo):
        meses += 1
        interes_bruto = saldo * tasa_mensual
        interes_neto = interes_bruto * (1 - tasa_impuestos)
        saldo += deposito_mensual + interes_neto - costo_mantenimiento
        historial.append((meses, saldo, interes_bruto, interes_neto))

    if not historial:  # Si historial está vacío, agregar al menos una fila
        historial.append((0, ingreso_inicial, 0, 0))

    # Crear DataFrame
    df = pd.DataFrame(historial, columns=['Mes', 'Saldo', 'Interes Bruto', 'Interes Neto'])

    # Redondear valores a dos decimales
    df['Saldo'] = df['Saldo'].round(2)
    df['Interes Bruto'] = df['Interes Bruto'].round(2)
    df['Interes Neto'] = df['Interes Neto'].round(2)

    # Guardar en archivo Excel
    df.to_excel(nombre_archivo, index=False)

    return df
