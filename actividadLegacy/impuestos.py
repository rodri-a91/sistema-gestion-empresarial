from abc import ABC, abstractmethod


class CalculadoraImpuesto(ABC):
    @abstractmethod
    def calcular_impuesto(self, base: float) -> float:
        ...

class ImpuestoGeneral(CalculadoraImpuesto):
    def calcular_impuesto(self, base):
        return round(base* 0.21, 2)

class ImpuestoReducido(CalculadoraImpuesto):
    def calcular_impuesto(self, base):
        return round(base * 0.1, 2)

class ImpuestoRecargo(CalculadoraImpuesto):
    def calcular_impuesto(self, base):
        return round(base * 0.262, 2)