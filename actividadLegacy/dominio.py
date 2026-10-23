from dataclasses import dataclass

from validadores import validar_cif


@dataclass(frozen=True)
class LineaFactura:
    concepto: str
    unidades: int
    precio_unitario: float

    def __post_init__(self) -> None:
        if self.unidades <= 0 or self.precio_unitario < 0:
            raise ValueError("Unidades o precio incorrecto")

    @property
    def subtotal(self):
        return round(self.unidades * self.precio_unitario, 2)


@dataclass(frozen=True)
class Factura:
    numero: str
    cliente: str
    cif: str
    linea: tuple[LineaFactura, ...]

    def __post_init__(self) -> None:
        validar_cif(self.cif)
        if not self.numero.strip() or not self.cliente.strip():
            raise ValueError("Número de factura o cliente incorrectos")
        if not self.linea:
            raise ValueError("Línea de factura vacía")

    @property
    def base_imponible(self) -> float:
        return round(sum(linea.subtotal for linea in self.linea), 2)
