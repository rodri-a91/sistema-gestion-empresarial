def enviar_correo(numero: str) -> None:
    print(f"Correo: {numero}")

def actualizar_pantalla(numero: str) -> None:
    print(f"Pantalla: {numero}")

def confirmar(numero: str) -> None:
    # Cada interesado nuevo obliga a editar esta función.
    enviar_correo(numero)
    actualizar_pantalla(numero)

if __name__ == "__main__":
    confirmar("P-001")
