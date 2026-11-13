from abc import ABC, abstractmethod


class Notificador(ABC):
    @abstractmethod
    def enviar(self, destino: str, texto: str) -> None:
        pass


class SmsExterno:
    def __init__(self):
        self.enviados: list[tuple[str, str]] = []

    def publicar(self, numero: str, contenido: str) -> str:
        self.enviados.append((numero, contenido))
        return "SMS publicado"


class AdaptadorSms(Notificador):
    def __init__(self, servicio: SmsExterno):
        self.servicio = servicio

    def enviar(self, destino: str, texto: str) -> None:
        self.servicio.publicar(destino, texto)


def avisar(notificador: Notificador, destino: str) -> None:
    notificador.enviar(destino, "Pedido confirmado")
