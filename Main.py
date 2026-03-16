"""
Autor: Samuel Hernandez, Leonardo Zambrano, Manuel 
Proyecto: Horarios de Clases
Materia: Algoritmos y Programación (BPTSP05)

Punto de entrada principal para el Sistema de Horarios.
"""
import sys
from utils.menu import crear_menu
from utils.data_manager import DataManager
from modules.profesores_mod import ProfesoresModule
from modules.materias_mod import MateriasModule
from modules.generacion_mod import GeneracionModule
# Estadisticas es opcional e importamos a demanda si instalan matplotlib

class Aplicacion:
    """ Clase principal que orquesta la ejecución del programa. """
    def __init__(self):
        """ Inicializar listas vacías en O(1). """
        self.materias = []
        self.profesores = []
        self.horario = []

    def ejecutar(self):
        """ Ciclo principal del sistema. O(1) tiempo del loop. """
        while True:
            opciones = [
                "Crear listas en blanco",
                "Descargar los datos de la API de Github",
                "Cargar un horario en CSV (Archivo: horario.csv)"
            ]
            sel = crear_menu("Sistema de Planificación de Horarios", opciones, funcion_volver=False)
            
            if sel == 1:
                self.materias = []
                self.profesores = []
                # Pasamos directo al menu principal de módulos
                self._menu_modulos()
            
            elif sel == 2:
                self.materias, self.profesores = DataManager.descargar_datos()
                self._menu_modulos()
                
            elif sel == 3:
                self.horario, self.materias, self.profesores = DataManager.cargar_horario_csv()
                # Pasar directo a ver el resultado del horario
                if self.horario:
                    gen_mod = GeneracionModule(self.materias, self.profesores)
                    gen_mod.horario = self.horario
                    
                    try:
                        print("Recalculando datos de la asignación leída...")
                        salones = 30
                        gen_mod.salones_disponibles = salones
                        ocu_bloques = {}
                        
                        from modules.generacion_mod import BLOQUES_HORARIOS
                        full_ocu = {b: 0 for b in BLOQUES_HORARIOS}
                        
                        for s in self.horario:
                            if s.estado == "programada":
                                full_ocu[s.bloque_tiempo] = full_ocu.get(s.bloque_tiempo, 0) + 1

                        gen_mod.reportar_resultados(full_ocu)
                        gen_mod.menu_post_generacion(full_ocu)
                    except Exception as e:
                        print(f"Error procesando CSV: {e}")
                else:
                    print("Error: No se pudo cargar el horario o el archivo está vacío.")

    def _menu_modulos(self):
        while True:
            opciones = [
                "Módulo de Profesores",
                "Módulo de Materias",
                "Módulo de Generación de horarios",
                "Módulo de Estadísticas (Bonus)",
                "Guardar datos actuales",
            ]
            sel = crear_menu("Menú de Módulos Fundamentales", opciones, funcion_volver=True)
            
            if sel is None:  # Volver al inicio principal
                break
                
            elif sel == 1:
                codigos = [m.codigo for m in self.materias]
                profesores_mod = ProfesoresModule(self.profesores, codigos)
                profesores_mod.menu_principal()
                
            elif sel == 2:
                materias_mod = MateriasModule(self.materias, self.profesores)
                materias_mod.menu_principal()
                
            elif sel == 3:
                if not self.materias or not self.profesores:
                    print("Error: No hay materias o profesores cargados.")
                    continue
                gen_mod = GeneracionModule(self.materias, self.profesores)
                self.horario = gen_mod.generar()
                
            elif sel == 4:
                try:
                    import matplotlib.pyplot as plt
                    from modules.estadisticas_mod import EstadisticasModule
                    
                    if not self.horario:
                        print("Aún no ha generado un horario. ¡Hagalo primero!")
                        continue
                        
                    est_mod = EstadisticasModule(self.horario, self.profesores, self.materias)
                    opciones_est = [
                        "Graficar salones ocupados por hora",
                        "Graficar porcentaje de carga de profesores",
                        "Graficar porcentaje de secciones cerradas"
                    ]
                    
                    sub = crear_menu("Módulo de Estadísticas", opciones_est, funcion_volver=True)
                    if sub == 1: est_mod.graficar_salones_ocupados()
                    elif sub == 2: est_mod.graficar_carga_profesores()
                    elif sub == 3: est_mod.graficar_secciones_cerradas()
                        
                except ImportError:
                    print("\n[!] Advertencia: La librería 'matplotlib' no está instalada.")
                    print("Instálela ejecutando: pip install matplotlib")
                except Exception as e:
                    print(f"Ocurrió un error con las gráficas: {e}")
                    
            elif sel == 5:
                # Opcional si quisieran guardar base de datos
                print("Nota: El proyecto dice explícitamente guardar el horario desde el menú de generación.")
                pass


if __name__ == "__main__":
    try:
        app = Aplicacion()
        app.ejecutar()
    except KeyboardInterrupt:
        print("\nSaliendo del programa...")
        sys.exit(0)
