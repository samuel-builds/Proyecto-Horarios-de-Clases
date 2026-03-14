from typing import List
from models.materia import Materia
from models.profesor import Profesor
from utils.menu import pedir_entero, crear_menu, confirmar

class MateriasModule:
    """
    Módulo para gestionar Materias.
    Permite ver, agregar, modificar y eliminar materias.
    """
    def __init__(self, materias: List[Materia], profesores: List[Profesor]):
        """
        Inicializa Módulo de Materias.
        Guarda referencia a profesores para comprobar asociaciones.
        Eficiencia: O(1) tiempo y espacio
        """
        self.materias = materias
        self.profesores = profesores

    def menu_principal(self):
        """
        Despliega el menú del módulo y procesa selecciones.
        Eficiencia: Loop infinito O(1) iteración / O(N) menú.
        """
        while True:
            opciones = [
                "Ver la lista de materias",
                "Ver los detalles de una materia específica",
                "Ver los profesores asociados a una materia",
                "Agregar una materia a la lista",
                "Eliminar una materia de la lista",
                "Modificar el número de secciones de la materia"
            ]
            seleccion = crear_menu("Módulo de Materias", opciones, funcion_volver=True)
            if seleccion is None:
                break
            elif seleccion == 1:
                self.ver_lista()
            elif seleccion == 2:
                self.ver_especifico()
            elif seleccion == 3:
                self.ver_profesores()
            elif seleccion == 4:
                self.agregar()
            elif seleccion == 5:
                self.eliminar()
            elif seleccion == 6:
                self.modificar_secciones()

    def ver_lista(self):
        """Muestra todas las materias. O(M) iteraciones."""
        if not self.materias:
            print("No hay materias registradas.")
            return
        for m in self.materias:
            print(m)

    def ver_especifico(self):
        """Busca y muestra materia por código. O(M) búsuqeda."""
        codigo = input("Ingrese el código de la materia: ").upper()
        materia = next((m for m in self.materias if m.codigo == codigo), None)
        if materia:
            print("Materia encontrada:")
            print(materia)
        else:
            print("Materia no encontrada.")

    def ver_profesores(self):
        """Muestra profesores que dan el código de materia. O(P) iteración."""
        codigo = input("Ingrese el código de la materia: ").upper()
        # Verificar si la materia existe
        if not any(m.codigo == codigo for m in self.materias):
            print("La materia no existe en el sistema.")
            return
            
        print(f"Profesores que imparten la materia {codigo}:")
        encontrados = False
        for p in self.profesores:
            if codigo in p.materias:
                print(f"- {p.nombre} {p.apellido} (Cédula: {p.cedula})")
                encontrados = True
        
        if not encontrados:
            print("Ningún profesor tiene asignada esta materia.")

    def agregar(self):
        """Crea y agrega nueva materia. O(1)."""
        codigo = input("Código: ").strip().upper()
        if any(m.codigo == codigo for m in self.materias):
            print("Error: Ya existe una materia con ese código.")
            return
            
        nombre = input("Nombre: ")
        secciones = pedir_entero("Número de secciones: ", min_val=0)
        
        self.materias.append(Materia(codigo, nombre, secciones))
        print("Materia agregada exitosamente.")

    def eliminar(self):
        """
        Elimina materia y notifica en caso de que profesores se queden con 0 materias.
        Eficiencia: O(M) para eliminar, O(P) para recorrer profesores. Total: O(M + P)
        """
        codigo = input("Código de la materia a eliminar: ").upper()
        materia = next((m for m in self.materias if m.codigo == codigo), None)
        if not materia:
            print("Materia no encontrada.")
            return
            
        # Revisar profesores
        profesores_afectados = []
        for p in self.profesores:
            if codigo in p.materias:
                if len(p.materias) == 1:
                    profesores_afectados.append(p)
                    
        if profesores_afectados:
            nombres = [f"{p.nombre} {p.apellido}" for p in profesores_afectados]
            print(f"ADVERTENCIA: Eliminar esta materia dejará a los siguientes profesores sin materias en su lista: {', '.join(nombres)}")
            if not confirmar("¿Desea continuar con la eliminación de todos modos?"):
                return
                
        # Procede a eliminarla de la lista de materias y de las listas de profesores
        self.materias.remove(materia)
        for p in self.profesores:
            if codigo in p.materias:
                p.eliminar_materia(codigo)
                
        print("Materia eliminada exitosamente del sistema y de las listas de los profesores.")

    def modificar_secciones(self):
        """
        Modifica total de secciones. Si se fija a 0, emite advertencia extra. O(M) para ubicar.
        """
        codigo = input("Código de la materia: ").upper()
        materia = next((m for m in self.materias if m.codigo == codigo), None)
        if not materia:
            print("Materia no encontrada.")
            return
            
        print(f"Secciones actuales: {materia.secciones}")
        nuevas = pedir_entero("Ingrese el nuevo número de secciones: ", min_val=0)
        
        if nuevas == 0:
            print("ADVERTENCIA: Fijar el número de secciones a 0 indica que la materia no se oferta en el trimestre actual.")
            if not confirmar("¿Está seguro de que desea fijar las secciones a 0?"):
                return
                
        materia.secciones = nuevas
        print("Número de secciones modificado.")
