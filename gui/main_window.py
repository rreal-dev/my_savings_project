import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from savings_calculator import calcular_ahorros
import config

class SavingsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Savings Calculator")
        self.root.iconphoto(False, self._get_icon())

        # Estilo de la ventana
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configuración de la ventana principal
        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Etiqueta y entrada para el ingreso inicial
        ttk.Label(self.frame, text="Ingreso Inicial (€):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ingreso_inicial_var = tk.StringVar(value=str(config.INGRESO_INICIAL))
        self.ingreso_inicial_entry = ttk.Entry(self.frame, textvariable=self.ingreso_inicial_var, width=20)
        self.ingreso_inicial_entry.grid(row=0, column=1, sticky=tk.E, pady=5)

        # Etiqueta y entrada para el depósito mensual
        ttk.Label(self.frame, text="Depósito Mensual (€):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.deposito_mensual_var = tk.StringVar(value=str(config.DEPOSITO_MENSUAL))
        self.deposito_mensual_entry = ttk.Entry(self.frame, textvariable=self.deposito_mensual_var, width=20)
        self.deposito_mensual_entry.grid(row=1, column=1, sticky=tk.E, pady=5)

        # Etiqueta y entrada para la tasa anual
        ttk.Label(self.frame, text="Tasa Anual (%):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.tasa_anual_var = tk.StringVar(value=str(config.TASA_ANUAL * 100))
        self.tasa_anual_entry = ttk.Entry(self.frame, textvariable=self.tasa_anual_var, width=20)
        self.tasa_anual_entry.grid(row=2, column=1, sticky=tk.E, pady=5)

        # Etiqueta y entrada para la tasa de impuestos
        ttk.Label(self.frame, text="Tasa de Impuestos (%):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.tasa_impuestos_var = tk.StringVar(value=str(config.TASA_IMPUESTOS * 100))
        self.tasa_impuestos_entry = ttk.Entry(self.frame, textvariable=self.tasa_impuestos_var, width=20)
        self.tasa_impuestos_entry.grid(row=3, column=1, sticky=tk.E, pady=5)

        # Etiqueta y entrada para el costo de mantenimiento
        ttk.Label(self.frame, text="Costo Mensual de Mantenimiento (€):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.costo_mantenimiento_var = tk.StringVar(value=str(config.COSTO_MANTENIMIENTO))
        self.costo_mantenimiento_entry = ttk.Entry(self.frame, textvariable=self.costo_mantenimiento_var, width=20)
        self.costo_mantenimiento_entry.grid(row=4, column=1, sticky=tk.E, pady=5)

        # Etiqueta y entrada para el objetivo
        ttk.Label(self.frame, text="Objetivo (€):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.objetivo_var = tk.StringVar(value=str(config.SALDO_OBJETIVO))
        self.objetivo_entry = ttk.Entry(self.frame, textvariable=self.objetivo_var, width=20)
        self.objetivo_entry.grid(row=5, column=1, sticky=tk.E, pady=5)

        # Opción para seleccionar el tipo de objetivo
        self.tipo_objetivo_var = tk.StringVar(value='saldo')
        ttk.Radiobutton(self.frame, text="Saldo Objetivo", variable=self.tipo_objetivo_var, value='saldo').grid(row=6, column=0, pady=5, sticky=tk.W)
        ttk.Radiobutton(self.frame, text="Beneficio Neto Objetivo", variable=self.tipo_objetivo_var, value='beneficio').grid(row=6, column=1, pady=5, sticky=tk.W)

        # Botón para calcular
        self.calc_button = ttk.Button(self.frame, text="Calcular", command=self.calcular)
        self.calc_button.grid(row=7, column=0, columnspan=2, pady=5)

        # Botón para guardar como Excel
        self.save_button = ttk.Button(self.frame, text="Guardar como Excel", command=self.guardar_excel)
        self.save_button.grid(row=8, column=0, columnspan=2, pady=5)

    def _get_icon(self):
        icon_path = "assets/icon.png"
        return ImageTk.PhotoImage(Image.open(icon_path))

    def calcular(self):
        try:
            ingreso_inicial = float(self.ingreso_inicial_var.get())
            deposito_mensual = float(self.deposito_mensual_var.get())
            tasa_anual = float(self.tasa_anual_var.get()) / 100
            tasa_impuestos = float(self.tasa_impuestos_var.get()) / 100
            objetivo = float(self.objetivo_var.get())
            tipo_objetivo = self.tipo_objetivo_var.get()
            costo_mantenimiento = float(self.costo_mantenimiento_var.get())

            self.dataframe = calcular_ahorros(
                ingreso_inicial,
                deposito_mensual,
                tasa_anual,
                tasa_impuestos,
                objetivo,
                tipo_objetivo,
                costo_mantenimiento,
                config.NOMBRE_ARCHIVO
            )

            self.mostrar_resultados()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {e}")

    def mostrar_resultados(self):
        if self.dataframe.empty:
            messagebox.showerror("Error", "No se han generado datos. Verifique los parámetros de entrada.")
            return

        resultados = tk.Toplevel(self.root)
        resultados.title("Resultados")

        frame_resultados = ttk.Frame(resultados, padding="10")
        frame_resultados.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        columns = ["Mes", "Saldo", "Interes Bruto", "Interes Neto"]
        tree = ttk.Treeview(frame_resultados, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.E, width=100)

        for _, row in self.dataframe.iterrows():
            tree.insert("", tk.END, values=[int(row['Mes']), f"{row['Saldo']:.2f}", f"{row['Interes Bruto']:.2f}", f"{row['Interes Neto']:.2f}"])

        tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Make the table responsive
        vsb = ttk.Scrollbar(frame_resultados, orient="vertical", command=tree.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        tree.configure(yscrollcommand=vsb.set)
        
        frame_resultados.columnconfigure(0, weight=1)
        frame_resultados.rowconfigure(0, weight=1)

        # Totales
        total_ingresado = self.dataframe['Mes'].max() * float(self.deposito_mensual_var.get()) + float(self.ingreso_inicial_var.get())
        saldo_final = self.dataframe['Saldo'].iloc[-1]
        total_beneficio = saldo_final - total_ingresado
        años_necesarios = self.dataframe['Mes'].max() / 12

        frame_totales = ttk.Frame(resultados, padding="10")
        frame_totales.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame_totales, text=f"Total Ingresado: {total_ingresado:.2f} €").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(frame_totales, text=f"Total Beneficio: {total_beneficio:.2f} €").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(frame_totales, text=f"Años Necesarios: {años_necesarios:.2f}").grid(row=2, column=0, sticky=tk.W, pady=5)

    def guardar_excel(self):
        try:
            self.dataframe.to_excel(config.NOMBRE_ARCHIVO, index=False)
            messagebox.showinfo("Éxito", f"Archivo guardado como {config.NOMBRE_ARCHIVO}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

def main():
    root = ThemedTk(theme="clam")
    app = SavingsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

