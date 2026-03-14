from typing import List
from models.profesor import Profesor
from models.horario import SeccionHorario
from utils.menu import pedir_entero, crear_menu

# Constante replicada (debería exportarse desde modelo o util, pero con copiar vale para el nivel del script)
BLOQUES_HORARIOS = [
    "Lunes y Miércoles 7:00 - 8:30", "Lunes y Miércoles 8:45 - 10:15",
    "Lunes y Miércoles 10:30 - 12:00", "Lunes y Miércoles 12:15 - 1:45",
    "Lunes y Miércoles 2:00 - 3:30", "Lunes y Miércoles 3:45 - 5:15",
    "Lunes y Miércoles 5:30 - 7:00",
    "Martes y Jueves 7:00 - 8:30", "Martes y Jueves 8:45 - 10:15",
    "Martes y Jueves 10:30 - 12:00", "Martes y Jueves 12:15 - 1:45",
    "Martes y Jueves 2:00 - 3:30", "Martes y Jueves 3:45 - 5:15",
    "Martes y Jueves 5:30 - 7:00"
]

class ModificacionModule:
    """
    Módulo para modificar los horarios ya generados.
    Permite cambiar profesor o bloque horario de una sección específica.
    """
    def __init__(self, horario: List[SeccionHorario], profesores: List[Profesor], salones_totales: int):
        """ Inicializa el modificador. Eficiencia: O(1) """
        self.horario = horario
        self.profesores = profesores
        self.salones_totales = salones_totales

    def modificar(self) -> List[SeccionHorario]:
        """ Control principal de modificación. Eficiencia: O(S * Menú) """
        while True:
            materia_cod = input("1. Ingrese el código de la materia (o escriba SALIR para volver): ").upper()
            if materia_cod == "SALIR":
                break
                
            # Buscar secciones de esa materia
            secciones_materia = [s for s in self.horario if s.materia.codigo == materia_cod]
            if not secciones_materia:
                print("No hay secciones programadas (o existentes) para esa materia.")
                continue
                
            print("\nSecciones encontradas:")
            for i, s in enumerate(secciones_materia, 1):
                print(f"{i}. {s}")
                
            idx = pedir_entero("2. Seleccione el número de la sección a modificar: ", 1, len(secciones_materia))
            seccion_elegida = secciones_materia[idx - 1]
            
            # Opciones de cambio
            sel = crear_menu("Opciones de Modificación", ["Cambiar profesor de la sección", "Cambiar el horario de la sección"], funcion_volver=True)
            if sel == 1:
                self._cambiar_profesor(seccion_elegida)
            elif sel == 2:
                self._cambiar_horario(seccion_elegida)
                
        return self.horario

    def _cambiar_profesor(self, seccion: SeccionHorario):
        """ Cambia profesor validando disponibilidad. Eficiencia: O(P) """
        # Disponibles: dan la materia + no pasaron carga max + no ocupan este bloque
        cargas = self._calcular_cargas()
        disponibles = []
        for p in self.profesores:
            if seccion.materia.codigo in p.materias:
                if cargas.get(p.cedula, 0) < p.max_carga:
                    if not any(s.profesor and s.profesor.cedula == p.cedula for s in self.horario if s.bloque_tiempo == seccion.bloque_tiempo and s != seccion):
                        disponibles.append(p)
                        
        if not disponibles:
            print("No hay otros profesores disponibles para esta materia y bloque.")
            return
            
        print("Profesores disponibles:")
        for i, p in enumerate(disponibles, 1):
            print(f"{i}. {p.nombre} {p.apellido} (Cédula: {p.cedula})")
            
        selec = pedir_entero("Seleccione el número del nuevo profesor: ", 1, len(disponibles))
        nuevo_profesor = disponibles[selec - 1]
        
        # Eliminar si estaba cerrada, y asignar
        seccion.profesor = nuevo_profesor
        seccion.estado = "programada"
        print("Profesor cambiado con éxito.")

    def _cambiar_horario(self, seccion: SeccionHorario):
        """ Cambia bloque horario validando salones y profesor. Eficiencia: O(B + P) """
        ocupacion = self._calcular_ocupacion()
        
        print("Bloques disponibles (con salones libres):")
        bloques_libres = []
        for i, b in enumerate(BLOQUES_HORARIOS, 1):
            if ocupacion.get(b, 0) < self.salones_totales:
                bloques_libres.append(b)
                print(f"{len(bloques_libres)}. {b} ({self.salones_totales - ocupacion.get(b, 0)} salones libres)")
                
        if not bloques_libres:
            print("No hay bloques con salones disponibles.")
            return
            
        sel_bloque = pedir_entero("Seleccione el nuevo bloque horario: ", 1, len(bloques_libres))
        nuevo_bloque = bloques_libres[sel_bloque - 1]
        
        # Luego el profesor...
        cargas = self._calcular_cargas()
        disponibles = []
        for p in self.profesores:
            if seccion.materia.codigo in p.materias:
                # Si es el mismo profesor, carga no importa pues se mueve, si es otro debe tener carga libre
                # Aquí para ser precisos: mostramos lista de profes disponibles a esa nueva hora
                if cargas.get(p.cedula, 0) < p.max_carga or (seccion.profesor and p.cedula == seccion.profesor.cedula):
                    if not any(s.profesor and s.profesor.cedula == p.cedula for s in self.horario if s.bloque_tiempo == nuevo_bloque and s != seccion):
                        disponibles.append(p)
                        
        if not disponibles:
            print(f"ADVERTENCIA: No hay profesores que puedan darla en el bloque {nuevo_bloque}. Abortando cambio.")
            return

        print("\nProfesores disponibles para la nueva hora:")
        for i, p in enumerate(disponibles, 1):
            print(f"{i}. {p.nombre} {p.apellido}")
            
        sel_prof = pedir_entero("Seleccione el profesor para este nuevo horario: ", 1, len(disponibles))
        
        seccion.bloque_tiempo = nuevo_bloque
        seccion.profesor = disponibles[sel_prof - 1]
        seccion.estado = "programada"
        print("Horario y profesor actualizados con éxito.")

    def _calcular_cargas(self):
        """ Eficiencia O(S) """
        cargas = {}
        for s in self.horario:
            if s.profesor and s.estado == "programada":
                cargas[s.profesor.cedula] = cargas.get(s.profesor.cedula, 0) + 1
        return cargas

    def _calcular_ocupacion(self):
        """ Eficiencia O(S) """
        ocu = {}
        for s in self.horario:
            if s.estado == "programada":
                ocu[s.bloque_tiempo] = ocu.get(s.bloque_tiempo, 0) + 1
        return ocu
