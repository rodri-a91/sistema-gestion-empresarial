from abc import ABC, abstractmethod

from dominio import Factura


class NotificadorFactura(ABC):
    @abstractmethod
    def notificar(self, factura: Factura, total: float) -> None: ...


class ExportadorFactura(ABC):
    @abstractmethod
    def exportar(self, factura: Factura) -> str: ...


class NotificadorEmail(NotificadorFactura):
    def __init__(self, destino: str) -> None:
        self.destino = destino

    def notificar(self, factura: Factura, total: float) -> None:
        print(f"Enviando {factura} de {total:2f}€ a {self.destino}")


class NotificadorConsola(NotificadorFactura):
    def notificar(self, factura: Factura, total: float) -> None:
        print(f"Notificiación: {factura} de {total:2f}€")


class ExportadorTexto(ExportadorFactura):
    def exportar(self, factura: Factura) -> str:
        return f"Número de factura: {factura.numero}\nCliente: {factura.cliente}\nBase imponible: {factura.base_imponible}"