class CorreoAntiguo:
    def send_message(self, payload: dict[str, str]) -> str:
        return f'Enviado a {payload["to"]}'

def avisar(servicio: CorreoAntiguo, destino: str) -> str:
    # El cliente depende del formato del proveedor.
    return servicio.send_message({"to": destino, "body": "Pedido confirmado"})

if __name__ == "__main__":
    print(avisar(CorreoAntiguo(), "aula@ejemplo.test"))
