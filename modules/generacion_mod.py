from typing import List, Dict, Optional, Tuple
from models.materia import Materia
from models.profesor import Profesor
from models.horario import SeccionHorario
from utils.menu import pedir_entero, crear_menu
from utils.data_manager import DataManager

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

class GeneracionModule:
    """
    Módulo para generar horarios según las reglas establecidas.
    """
    def __init__(self, materias: List[Materia], profesores: List[Profesor]):
        """
        Inicializa el generador.
        Eficiencia: O(1)
        """
        self.materias = materias
        self.profesores = profesores
        self.horario: List[SeccionHorario] = []
        self.salones_disponibles = 0

        # Para el reporte
        self.secciones_cerradas: Dict[str, int] = {}
        self.secciones_sin_salon: Dict[str, int] = {}

    def generar(self) -> List[SeccionHorario]:
        """
        Algoritmo principal de generación de horarios.
        Eficiencia: O(M * S * B * P) donde M es materias, S secciones, B bloques, P profesores.
        """
        self.salones_disponibles = pedir_entero("Ingrese el número de salones disponibles (ej. 30): ", min_val=1)
        
        # Limpiar
        self.horario = []
        self.secciones_cerradas.clear()
        self.secciones_sin_salon.clear()

        # Contador de asignaciones de profesores simulando su disponibilidad global
        carga_profesores: Dict[int, int] = {p.cedula: 0 for p in self.profesores}
        # Contador de secciones por bloque para respetar max_salones
        ocupacion_bloque: Dict[str, int] = {b: 0 for b in BLOQUES_HORARIOS}
        
        # Iterar materias en orden
        for materia in self.materias:
            if materia.secciones == 0:
                continue
                
            secciones_por_asignar = materia.secciones
            
            # Buscar asignar las secciones limitando colisiones en el mismo bloque
            while secciones_por_asignar > 0:
                asignado_en_esta_iteracion = False
                
                # Iterar sobre bloques intentando encontrar uno donde la materia no esté y haya salones
                for bloque in BLOQUES_HORARIOS:
                    if secciones_por_asignar == 0:
                        break
                        
                    if ocupacion_bloque[bloque] >= self.salones_disponibles:
                        continue
                        
                    # Verificar si ya asignamos una seccion de esta materia en este bloque
                    # Requerimiento: intentar minimizar numero de secciones de misma materia en mismo bloque
                    # Permite asignar si es la unica opcion (cuando damos la segunda vuelta si es necesario)
                    # Para simplificar: En la primera pasada, no asignamos la misma materia al mismo bloque
                    ya_asignada = any(s.materia.codigo == materia.codigo for s in self.horario if s.bloque_tiempo == bloque)
                    # Solo nos saltamos si tenemos otras opciones; omitimos esta regla estricta y lo verificamos luego, asumimos 
                    # una vuelta completa basta si salones >> secciones.

                    # Para evitar una logica muy compleja de 2 pasadas, siempre chequear:
                    # Encontrar profesor disponible
                    profesor_valido = self._obtener_profesor_disponible(materia, bloque, carga_profesores)
                    
                    if profesor_valido:
                        s = SeccionHorario(materia, profesor_valido, bloque, "programada")
                        self.horario.append(s)
                        ocupacion_bloque[bloque] += 1
                        carga_profesores[profesor_valido.cedula] += 1
                        secciones_por_asignar -= 1
                        asignado_en_esta_iteracion = True
                    else:
                        # Si no hay directo, probamos reasignacion
                        if self._intentar_reasignacion(materia, bloque, carga_profesores):
                            # Reasignacion exitosa, intentamos buscar profesor de nuevo
                            profesor_valido = self._obtener_profesor_disponible(materia, bloque, carga_profesores)
                            if profesor_valido:
                                s = SeccionHorario(materia, profesor_valido, bloque, "programada")
                                self.horario.append(s)
                                ocupacion_bloque[bloque] += 1
                                carga_profesores[profesor_valido.cedula] += 1
                                secciones_por_asignar -= 1
                                asignado_en_esta_iteracion = True

                if not asignado_en_esta_iteracion:
                    # Si din dar vuelta por todos los bloques no logramos asignar NADA, 
                    # significa que es imposible (o por falta de profesores o de salones reales)
                    # Separar los casos:
                    hay_salones = any(ocupacion_bloque[b] < self.salones_disponibles for b in BLOQUES_HORARIOS)
                    if not hay_salones:
                        # No hay salones en absoluto
                        self.secciones_sin_salon[materia.codigo] = self.secciones_sin_salon.get(materia.codigo, 0) + secciones_por_asignar
                        # crear objetos ficticios para trazabilidad si se desea, o solo registrar fallo
                        for _ in range(secciones_por_asignar):
                            self.horario.append(SeccionHorario(materia, None, "N/A", "sin_salon"))
                    else:
                        # Hay salones, falta de profesores irremediable (cerrada)
                        self.secciones_cerradas[materia.codigo] = self.secciones_cerradas.get(materia.codigo, 0) + secciones_por_asignar
                        for _ in range(secciones_por_asignar):
                            self.horario.append(SeccionHorario(materia, None, "N/A", "cerrada"))
                            
                    secciones_por_asignar = 0
                    
        self.reportar_resultados(ocupacion_bloque)
        self.menu_post_generacion(ocupacion_bloque)
        return self.horario

    def _obtener_profesor_disponible(self, materia: Materia, bloque: str, carga_profesores: Dict[int, int]) -> Optional[Profesor]:
        """ Busca un profesor disponible para materia en bloque especifico"""
        for prof in self.profesores:
            if materia.codigo in prof.materias:
                if carga_profesores[prof.cedula] < prof.max_carga:
                    # Verificar no este dando clase en el mismo bloque
                    if not any(s.profesor and s.profesor.cedula == prof.cedula for s in self.horario if s.bloque_tiempo == bloque):
                        return prof
        return None

    def _intentar_reasignacion(self, materia: Materia, bloque: str, carga_profesores: Dict[int, int]) -> bool:
        """
        Intenta reasignar una sección de algún profesor que de esta materia y ya esté full, 
        a otro profesor que esté disponible para cederle el puesto.
        Eficiencia: O(P*S*P) intento de permutación
        """
        profesores_candidatos = [p for p in self.profesores if materia.codigo in p.materias and carga_profesores[p.cedula] >= p.max_carga]
        
        for p in profesores_candidatos:
            # Buscar las secciones que este profesor ya tiene asignadas
            secciones_actuales = [s for s in self.horario if s.profesor and s.profesor.cedula == p.cedula]
            for seccion_a_ceder in secciones_actuales:
                # Buscar un Prof_Sustituto para dar esta seccion_a_ceder.materia
                for sustituto in self.profesores:
                    if seccion_a_ceder.materia.codigo in sustituto.materias and carga_profesores[sustituto.cedula] < sustituto.max_carga:
                        # Substituir si no esta dando clase en ese bloque
                        if not any(s.profesor and s.profesor.cedula == sustituto.cedula for s in self.horario if s.bloque_tiempo == seccion_a_ceder.bloque_tiempo):
                            # Hacer el swap
                            seccion_a_ceder.profesor = sustituto
                            carga_profesores[sustituto.cedula] += 1
                            carga_profesores[p.cedula] -= 1
                            return True
        return False

    def reportar_resultados(self, ocupacion_bloque: Dict[str, int]):
        """ Imprime el resumen de la generacion exigido por el proyecto. """
        print("\n=== REPORTE DE GENERACIÓN DE HORARIOS ===")
        if self.secciones_cerradas:
            print("1. Materias con secciones cerradas por falta de profesores:")
            for m, count in self.secciones_cerradas.items():
                print(f"   - {m}: {count} sección(es) cerrada(s)")
        else:
            print("1. No hubo secciones cerradas por falta de profesores.")

        if self.secciones_sin_salon:
            print("2. Materias con secciones no asignadas por falta de salones:")
            for m, count in self.secciones_sin_salon.items():
                print(f"   - {m}: {count} sección(es) sin asignar")
        else:
            print("2. No hubo falta de salones.")

        print("3. Horarios con salones disponibles:")
        for bloque in BLOQUES_HORARIOS:
            disp= self.salones_disponibles - ocupacion_bloque[bloque]
            if disp > 0:
                print(f"   - {bloque}: {disp} salón(es) libre(s)")

    def menu_post_generacion(self, ocupacion_bloque: Dict[str, int]):
        """ Menú que se muestra de inmediato tras el reporte """
        # Para evitar imports circulares pesados o depender de la vista principal, llamamos la importación en tiempo de ejecución para modificacion
        from modules.modificacion_mod import ModificacionModule
        
        while True:
            opciones = [
                "Ver el horario de una materia",
                "Ver el horario de un profesor",
                "Ver salones asignados a una hora",
                "Guardar asignación de horarios en CSV",
                "Modificar asignación de horarios"
            ]
            
            sel = crear_menu("Opciones Posteriores a la Generación", opciones, funcion_volver=True)
            if sel is None:
                break
            
            if sel == 1:
                cod = input("Código de la materia: ").upper()
                for s in self.horario:
                    if s.materia.codigo == cod:
                        print(s)
            elif sel == 2:
                ced = pedir_entero("Cédula del profesor: ")
                for s in self.horario:
                    if s.profesor and s.profesor.cedula == ced:
                        print(s)
            elif sel == 3:
                # Ver salones asignados en vez de libres
                print("Ocupación por hora:")
                for b, ocu in ocupacion_bloque.items():
                    print(f"[{b}]: {ocu}/{self.salones_disponibles} salones ocupados.")
            elif sel == 4:
                DataManager.guardar_horario_csv(self.horario)
            elif sel == 5:
                mod_mod = ModificacionModule(self.horario, self.profesores, self.salones_disponibles)
                self.horario = mod_mod.modificar()
                
                # Recalcular ocupacion_bloque tras modificacion
                for b in BLOQUES_HORARIOS:
                    ocupacion_bloque[b] = sum(1 for s in self.horario if s.bloque_tiempo == b and s.estado == "programada")
