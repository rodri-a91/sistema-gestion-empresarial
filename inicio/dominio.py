from inicio.domain.impuestos import CalculadorImpuesto
from dataclasses import dataclass
from inicio.domain.identificadores import validar_cif

@dataclass(frozen=True)
class LineaFactura:
    concepto: str
    unidades: int
    precio_unitario: float

    def __post_init__(self) -> None:
        if self.unidades <= 0 or self.precio_unitario < 0:
            raise ValueError('Unidades o precio incorrectos')

    @property
    def subtotal(self) -> float:
        return round(self.unidades * self.precio_unitario, 2)

@dataclass(frozen=True)
class Factura:
    numero: str
    cliente: str
    cif: str
    lineas: tuple[LineaFactura, ...]

    def __post_init__(self) -> None:
        validar_cif(self.cif)
        if not self.numero.strip() or not self.cliente.strip():
            raise ValueError('Número y cliente obligatorios')
        if not self.lineas:
            raise ValueError('Factura sin líneas comerciales')

    @property
    def base_imponible(self) -> float:
        return round(sum(linea.subtotal for linea in self.lineas), 2)


    def calcular_total(self, calculador: CalculadorImpuesto) -> float:
        base = self.base_imponible
        return round(base + calculador.calcular_impuesto(base), 2)
