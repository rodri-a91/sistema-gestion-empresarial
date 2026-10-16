from abc import ABC, abstractmethod

from dominio import Factura


class RepositorioFactura(ABC):
    @abstractmethod
    def guardar(self, factura: Factura) -> None:
        ...
    @abstractmethod
    def buscar(self, numero: str) -> Factura | None:
        ...


class RepositorioMemoria(RepositorioFactura):
    def __init__(self) -> None:
        self.facturas: dict[str, Factura] = {}

    def guardar(self, factura: Factura) -> None:
        self.facturas[factura.numero] = factura

    def buscar(self, numero: str) -> Factura | None:
        return self._facturas.get(numero)


class RepositorioLista(RepositorioFactura):
    def __init__(self) -> None:
        self._facturas: list[Factura] = []

    def guardar(self, factura: Factura) -> None:
        self._facturas = [f for f in self._facturas if f.numero != factura.numero]
        self._facturas.append(factura)

    def buscar(self, numero: str) -> Factura | None:
        for factura in self._facturas:
            if factura.numero == numero:
                return factura

        return None