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
        print(f"[EMAIL SIMULADO] {self.destino}: {factura.numero}, {total:.2f} EUR")


class NotificadorConsola(NotificadorFactura):
    def notificar(self, factura: Factura, total: float) -> None:
        print(f"[CONSOLA] {factura.numero}: {total:.2f} EUR")


class ExportadorTexto(ExportadorFactura):
    def exportar(self, factura: Factura) -> str:
        return (
            f"{factura.numero} | {factura.cliente} | "
            f"base {factura.base_imponible:.2f} EUR"
        )
