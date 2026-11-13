from decimal import Decimal

if __name__ == "__main__":
    # Cada pantalla conoce y repite todos los pasos.
    producto = "teclado"
    peso = {"teclado": 2, "raton": 1}[producto]
    coste = Decimal(peso) * Decimal("2.00")
    etiqueta = f"{producto}: portes {coste:.2f} EUR"
    print(etiqueta)
