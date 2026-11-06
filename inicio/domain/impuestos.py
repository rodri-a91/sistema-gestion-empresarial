from abc import ABC, abstractmethod


class CalculadorImpuesto(ABC):
    @abstractmethod
    def calcular_impuesto(self, base: float) -> float:
        """Para base >= 0 del taller, devuelve la cuota >= 0, a céntimos."""
        ...

class ImpuestoGeneral(CalculadorImpuesto):
    def calcular_impuesto(self, base: float) -> float:
        return round(base * 0.21, 2)

class ImpuestoReducido(CalculadorImpuesto):
    def calcular_impuesto(self, base: float) -> float:
        return round(base * 0.10, 2)

class ImpuestoRecargo(CalculadorImpuesto):
    def calcular_impuesto(self, base: float) -> float:
        return round(base * 0.262, 2)
