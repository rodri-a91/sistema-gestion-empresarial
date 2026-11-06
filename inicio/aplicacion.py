from dominio import Factura
from notificaciones import NotificadorFactura
from persistencia import RepositorioFacturas

from inicio.domain.impuestos import CalculadorImpuesto


def emitir_factura(
    factura: Factura,
    calculador: CalculadorImpuesto,
    repositorio: RepositorioFacturas,
    notificador: NotificadorFactura | None = None,
) -> float:
    total = factura.calcular_total(calculador)
    repositorio.guardar(factura)
    if notificador is not None:
        notificador.notificar(factura, total)
    return total
