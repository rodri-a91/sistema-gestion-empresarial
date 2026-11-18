import ast
import json
import sys
from pathlib import Path

from datos_ejemplo import datos_factura
from facturacion.application.casos_uso import consultar_factura, emitir_factura
from facturacion.application.puertos import NotificadorFactura, RepositorioFacturas
from facturacion.application.resultados import ResultadoEmision
from facturacion.domain.entidades import Factura, LineaFactura
from facturacion.domain.impuestos import ImpuestoGeneral, ImpuestoRecargo, ImpuestoReducido
from facturacion.infrastructure.entrada_json import emitir_desde_json
from facturacion.infrastructure.entrada_lotes import emitir_lote
from facturacion.infrastructure.notificaciones import NotificadorConsola, NotificadorEmail
from facturacion.infrastructure.repositorios import RepositorioLista, RepositorioMemoria

REPOSITORIOS = (RepositorioMemoria, RepositorioLista)


class NotificadorEspia(NotificadorFactura):
    def __init__(self) -> None:
        self.llamadas: list[tuple[str, float]] = []

    def notificar(self, factura: Factura, total: float) -> None:
        self.llamadas.append((factura.numero, total))


class NotificadorQueFalla(NotificadorFactura):
    def notificar(self, factura: Factura, total: float) -> None:
        raise RuntimeError('Fallo simulado al avisar')


class RepositorioQueFalla(RepositorioFacturas):
    def guardar(self, factura: Factura) -> None:
        raise RuntimeError('Fallo simulado al guardar')

    def buscar(self, numero: str) -> Factura | None:
        return None


def crear_factura(numero: str = 'F-001') -> Factura:
    return Factura(numero, 'Comercial Aula SL', 'B12345678', (
        LineaFactura('Licencia ERP', 1, 1500.0),
        LineaFactura('Soporte', 2, 250.0),
    ))


def esperar_error(tipo: type[Exception], funcion, *args) -> None:
    try:
        funcion(*args)
    except tipo:
        return
    raise AssertionError(f'Se esperaba {tipo.__name__}')


def comprobar_dominio() -> None:
    factura = crear_factura()
    assert factura.base_imponible == 2000.0
    assert factura.calcular_total(ImpuestoGeneral()) == 2420.0
    assert factura.calcular_total(ImpuestoReducido()) == 2200.0
    assert factura.calcular_total(ImpuestoRecargo()) == 2524.0
    esperar_error(ValueError, Factura, 'F-001', 'Comercial Aula SL', 'B12345678', ())
    print('Fase 2 · dominio: base, tres totales y rechazo sin líneas OK')


def comprobar_casos_uso() -> None:
    factura = crear_factura()
    repo = RepositorioMemoria()
    resultado = emitir_factura(factura, ImpuestoRecargo(), repo,
                               NotificadorEmail('aula@example.com'))
    assert resultado == ResultadoEmision('F-001', 2524.0)
    assert consultar_factura('F-001', repo) == factura
    esperar_error(ValueError, consultar_factura, '   ', repo)
    esperar_error(LookupError, consultar_factura, 'F-999', repo)

    sin_aviso = emitir_factura(factura, ImpuestoRecargo(), RepositorioMemoria())
    assert sin_aviso.total == 2524.0
    print('Fase 3 · emitir, consultar, ausencia y emisión sin notificador OK')


def comprobar_sustitucion() -> None:
    resultado = emitir_factura(crear_factura(), ImpuestoRecargo(),
                               RepositorioMemoria(), NotificadorConsola())
    assert resultado.total == 2524.0
    print('Fase 4 · email sustituido por consola sin tocar el caso de uso OK')


def casos_json_invalidos() -> dict[str, str]:
    def con_linea(**cambios: object) -> str:
        datos = datos_factura()
        datos['lineas'][1].update(cambios)
        return json.dumps(datos)

    sin_cliente = datos_factura()
    del sin_cliente['cliente']
    sin_lineas = datos_factura()
    sin_lineas['lineas'] = []

    return {
        'JSON mal formado': '{"numero": "F-001",',
        'falta cliente': json.dumps(sin_cliente),
        'unidades "2"': con_linea(unidades='2'),
        'unidades 2.8': con_linea(unidades=2.8),
        'unidades true': con_linea(unidades=True),
        'unidades 0': con_linea(unidades=0),
        'precio negativo': con_linea(precio=-1.0),
        'precio "250"': con_linea(precio='250'),
        'precio NaN': con_linea(precio=float('nan')),
        'líneas vacías': json.dumps(sin_lineas),
    }


def comprobar_json() -> None:
    texto = json.dumps(datos_factura())
    for clase in REPOSITORIOS:
        repo = clase()
        mensaje = emitir_desde_json(texto, ImpuestoRecargo(), repo)
        assert mensaje == 'Emitida F-001: 2524.00 EUR'
        assert repo.buscar('F-001') is not None

        for nombre, invalido in casos_json_invalidos().items():
            repo = clase()
            try:
                emitir_desde_json(invalido, ImpuestoRecargo(), repo)
            except ValueError:
                pass
            else:
                raise AssertionError(f'Se aceptó: {nombre}')
            assert repo.buscar('F-001') is None, f'Se guardó F-001 en: {nombre}'
    print(f'Fase 5 · JSON válido y {len(casos_json_invalidos())} casos inválidos '
          'con ambos repositorios OK')


def comprobar_repositorio(clase: type[RepositorioFacturas]) -> None:
    repo = clase()
    assert repo.buscar('F-001') is None

    f1, f2 = crear_factura('F-001'), crear_factura('F-002')
    repo.guardar(f1)
    repo.guardar(f2)
    assert repo.buscar('F-001') == f1 and repo.buscar('F-002') == f2

    f1_nueva = Factura('F-001', 'Otro Cliente SL', 'A87654321', f1.lineas)
    repo.guardar(f1_nueva)
    assert repo.buscar('F-001') == f1_nueva
    assert repo.buscar('F-002') == f2

    assert clase().buscar('F-001') is None


def comprobar_lotes() -> None:
    for clase in REPOSITORIOS:
        comprobar_repositorio(clase)

        repo = clase()
        mensajes = emitir_lote([datos_factura('F-001'), datos_factura('F-002')],
                               ImpuestoRecargo(), repo)
        assert mensajes == ['Emitida F-001: 2524.00 EUR', 'Emitida F-002: 2524.00 EUR']

        invalida = datos_factura('F-002')
        invalida['lineas'][0]['unidades'] = 0
        repo = clase()
        esperar_error(ValueError, emitir_lote,
                      [datos_factura('F-001'), invalida, datos_factura('F-003')],
                      ImpuestoRecargo(), repo)
        assert repo.buscar('F-001') is not None
        assert repo.buscar('F-002') is None
        assert repo.buscar('F-003') is None
    print('Fase 6 · repositorios, lote F-001/F-002 y parada en el primer error OK')


def comprobar_fallos() -> None:
    espia = NotificadorEspia()
    esperar_error(RuntimeError, emitir_factura,
                  crear_factura(), ImpuestoRecargo(), RepositorioQueFalla(), espia)
    assert espia.llamadas == []

    repo = RepositorioMemoria()
    esperar_error(RuntimeError, emitir_factura,
                  crear_factura(), ImpuestoRecargo(), repo, NotificadorQueFalla())
    assert repo.buscar('F-001') is not None

    espia = NotificadorEspia()
    resultado = emitir_factura(crear_factura(), ImpuestoGeneral(), RepositorioLista(), espia)
    assert resultado.total == 2420.0 and espia.llamadas == [('F-001', 2420.0)]
    print('Fase 7 · fallo al guardar, fallo al avisar y núcleo directo OK')


PERMITIDOS = {
    'domain': ('facturacion.domain',),
    'application': ('facturacion.domain', 'facturacion.application'),
}


def modulos_importados(ruta: Path) -> list[str]:
    arbol = ast.parse(ruta.read_text(encoding='utf-8'))
    modulos: list[str] = []
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            modulos += [alias.name for alias in nodo.names]
        elif isinstance(nodo, ast.ImportFrom):
            modulos.append('.' * nodo.level + (nodo.module or ''))
    return modulos


def comprobar_imports() -> None:
    paquete = Path(__file__).parent / 'facturacion'
    for capa, permitidos in PERMITIDOS.items():
        for ruta in (paquete / capa).glob('*.py'):
            for modulo in modulos_importados(ruta):
                if modulo.split('.')[0] in sys.stdlib_module_names:
                    continue
                if not modulo.startswith(permitidos):
                    raise AssertionError(f'{capa}/{ruta.name} importa {modulo}')
    print('Fase 7 · imports: dominio y aplicación respetan las fronteras OK')


def main() -> None:
    comprobar_dominio()
    comprobar_casos_uso()
    comprobar_sustitucion()
    comprobar_json()
    comprobar_lotes()
    comprobar_fallos()
    comprobar_imports()

    print()
    texto = json.dumps(datos_factura())
    print(emitir_desde_json(texto, ImpuestoRecargo(), RepositorioMemoria(),
                            NotificadorConsola()))


if __name__ == '__main__':
    main()
