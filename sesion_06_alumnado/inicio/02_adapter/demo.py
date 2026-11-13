from abc import ABC, abstractmethod


class Notificador(ABC):
    @abstractmethod
    def enviar(self, destino: str, texto: str) -> None:
        pass


class CorreoAntiguo:
    def __init__(self):
        self.enviados: list[dict[str, str]] = []

    def send_message(self, payload: dict) -> str:
        self.enviados.append(payload)
        return "Envío correcto"


class AdaptadorCorreo(Notificador):
    def __init__(self, servicio: CorreoAntiguo):
        self.servicio = servicio

    def enviar(self, destino: str, texto: str) -> None:
        payload = {"to": destino, "body": texto}
        self.servicio.send_message(payload)


def avisar(notificador: Notificador, destino: str) -> None:
    notificador.enviar(destino, "Pedido confirmado")
