from inicio.domain.impuestos import CalculadorImpuesto
from inicio.dominio import Factura
from inicio.persistencia import RepositorioFacturas

from .puertos import NotificadorFactura, RepositorioFacturas  # noqa: F811
from .resultado import ResultadoEmision


def emitir_factura(
    factura: Factura,
    calculador: CalculadorImpuesto,
    repositorio: RepositorioFacturas,
    notificador: NotificadorFactura | None = None,
) -> ResultadoEmision:
    total = factura.calcular_total(calculador)
    repositorio.guardar(factura)
    if notificador is not None:
        notificador.notificar(factura, total)
    return ResultadoEmision(factura.numero, total)


def consultar_factura(numero: str, repositorio: RepositorioFacturas) -> Factura:
    if not numero.strip():
        raise ValueError("El número es obligatorio")
    factura = repositorio.buscar(numero)
    if factura is None:
        raise LookupError("Factura no encontrada")

    return factura
