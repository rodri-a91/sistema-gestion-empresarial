from abc import ABC, abstractmethod

from inicio.dominio import Factura


class RepositorioFacturas(ABC):
    @abstractmethod
    def guardar(self, factura: Factura) -> None:
        """Guarda por número; el mismo número reemplaza el dato anterior."""
        ...

    @abstractmethod
    def buscar(self, numero: str) -> Factura | None:
        """Devuelve lo guardado o None si no existe."""
        ...

    from abc import ABC, abstractmethod


from dominio import Factura


class NotificadorFactura(ABC):
    @abstractmethod
    def notificar(self, factura: Factura, total: float) -> None: ...


class ExportadorFactura(ABC):
    @abstractmethod
    def exportar(self, factura: Factura) -> str: ...
