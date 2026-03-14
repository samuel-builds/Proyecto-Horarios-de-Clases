from typing import List
import matplotlib.pyplot as plt
from models.profesor import Profesor
from models.materia import Materia
from models.horario import SeccionHorario
from modules.generacion_mod import BLOQUES_HORARIOS

class EstadisticasModule:
    """
    Módulo opcional (bonus) para la visualización de estadísticas utilizando Matplotlib.
    """
    def __init__(self, horario: List[SeccionHorario], profesores: List[Profesor], materias: List[Materia]):
        """ Inicializa las estadísticas con los datos generados. O(1). """
        self.horario = horario
        self.profesores = profesores
        self.materias = materias

    def graficar_salones_ocupados(self):
        """
        Gráfica de barras mostrando la cantidad de salones ocupados en cada bloque.
        Eficiencia: O(S + B) calculos pre-grafica.
        """
        if not self.horario:
            print("No hay horario generado para graficar.")
            return
            
        ocupacion = {b: 0 for b in BLOQUES_HORARIOS}
        for s in self.horario:
            if s.estado == "programada":
                ocupacion[s.bloque_tiempo] += 1
                
        bloques = [b.split(' ')[-3:] for b in ocupacion.keys()] # simplificar etiquetas (solo horas)
        labels = [" ".join(x) for x in bloques]
        valores = list(ocupacion.values())
        
        plt.figure(figsize=(12, 6))
        plt.bar(labels, valores, color='skyblue')
        plt.title('Salones ocupados por hora')
        plt.xlabel('Bloques Horarios')
        plt.ylabel('Salones')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def graficar_carga_profesores(self):
        """
        Porcentaje (histograma/barras) de su max carga asignada.
        """
        if not self.horario:
            print("No hay horario para graficar.")
            return
            
        cargas = {p.cedula: 0 for p in self.profesores}
        for s in self.horario:
            if s.profesor and s.estado == "programada":
                cargas[s.profesor.cedula] += 1
                
        nombres = []
        porcentajes = []
        for p in self.profesores:
            if p.max_carga > 0:
                pct = (cargas[p.cedula] / p.max_carga) * 100
            else:
                pct = 0
            nombres.append(p.nombre[:3] + " " + p.apellido[:3])
            porcentajes.append(pct)
            
        plt.figure(figsize=(14, 6))
        plt.bar(nombres, porcentajes, color='green')
        plt.title('Porcentaje de la Carga Máxima Asignada por Profesor')
        plt.xlabel('Profesores (Resumen)')
        plt.ylabel('Porcentaje de carga asignada (%)')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

    def graficar_secciones_cerradas(self):
        """
        Porcentaje de secciones cerradas (por falta profes) sobre total exigido.
        """
        if not self.horario:
            print("No hay horario para graficar.")
            return
            
        secciones_originales = {m.codigo: m.secciones for m in self.materias if m.secciones > 0}
        cerradas_cont = {m.codigo: 0 for m in self.materias}
        for s in self.horario:
            if s.estado == "cerrada":
                cerradas_cont[s.materia.codigo] += 1
                
        codigos = []
        pcts = []
        for cod, totals in secciones_originales.items():
            cerr = cerradas_cont[cod]
            pcts.append((cerr / totals) * 100)
            codigos.append(cod)
            
        plt.figure(figsize=(12, 6))
        plt.plot(codigos, pcts, marker='o', color='red', linestyle='dashed')
        plt.title('Porcentaje de Secciones Cerradas por Materia')
        plt.xlabel('Código de Materia')
        plt.ylabel('% Cerradas')
        plt.xticks(rotation=90)
        plt.grid()
        plt.tight_layout()
        plt.show()
