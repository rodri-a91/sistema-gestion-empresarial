def crear_informe(titulo: str, destinatario: str,
                  lineas: list[str]) -> dict:
    return {"titulo": titulo, "destinatario": destinatario,
            "lineas": lineas}

if __name__ == "__main__":
    lineas = ["Pedido P-001"]
    informe = crear_informe("Ventas", "Dirección", lineas)
    lineas.append("Dato añadido después")
    print(informe["lineas"])
