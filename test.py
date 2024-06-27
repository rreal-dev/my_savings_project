# Parameters
deposito_inicial = 80000
tasa_anual = 0.04
tasa_impuestos = 0.1911  # Updated tax rate
años = 5
costo_mensual = 16.90

# Monthly rate adjusted for taxes
tasa_mensual = tasa_anual / 12
tasa_mensual_ajustada = tasa_mensual * (1 - tasa_impuestos)
meses = años * 12

# Initialize balance
saldo = deposito_inicial

# Calculate compound interest over the period and account for monthly cost
for _ in range(meses):
    interes_bruto = saldo * tasa_mensual
    interes_neto = interes_bruto * (1 - tasa_impuestos)
    saldo += interes_neto - costo_mensual

# Net benefit
beneficio_neto = saldo - deposito_inicial
saldo, beneficio_neto

print(f"Saldo Final: {saldo:.2f} €, Beneficio Neto: {beneficio_neto:.2f} €")
