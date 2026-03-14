from typing import List
from models.profesor import Profesor
from utils.menu import pedir_entero, crear_menu, confirmar

class ProfesoresModule:
    """
    Módulo para gestionar Profesores.
    Permite ver, agregar, eliminar y modificar materias a profesores.
    """
    def __init__(self, profesores: List[Profesor], materias_codigos: List[str]):
        """
        Inicializa Módulo de Profesores.
        Eficiencia: O(1) tiempo y espacio
        """
        self.profesores = profesores
        self.materias_codigos = materias_codigos

    def menu_principal(self):
        """
        Despliega el menú de CRUD de profesores.
        Eficiencia: O(N) por las llamadas a crear_menu
        """
        while True:
            opciones = [
                "Ver la lista de profesores",
                "Ver un profesor específico",
                "Agregar un profesor",
                "Eliminar un profesor",
                "Modificar materias de un profesor"
            ]
            seleccion = crear_menu("Módulo de Profesores", opciones, funcion_volver=True)
            if seleccion is None:
                break
            
            if seleccion == 1:
                self.ver_lista()
            elif seleccion == 2:
                self.ver_especifico()
            elif seleccion == 3:
                self.agregar()
            elif seleccion == 4:
                self.eliminar()
            elif seleccion == 5:
                self.modificar_materias()

    def ver_lista(self):
        """
        Muestra la lista de profesores.
        Eficiencia: O(P) donde P es el número de profesores.
        """
        if not self.profesores:
            print("No hay profesores registrados.")
            return
        
        for p in self.profesores:
            print(p)

    def ver_especifico(self):
        """
        Busca y muestra un profesor por su cédula.
        Eficiencia: O(P) por búsqueda lineal.
        """
        cedula = pedir_entero("Ingrese la cédula del profesor: ")
        for p in self.profesores:
            if p.cedula == cedula:
                print("Profesor encontrado:")
                print(p)
                return
        print("Profesor no encontrado.")

    def agregar(self):
        """
        Agrega un nuevo profesor a la lista instanciando un objeto Profesor.
        Eficiencia: O(1) tiempo (O(N) por input)
        """
        cedula = pedir_entero("Cédula: ")
        # Validar cédula repetida
        if any(p.cedula == cedula for p in self.profesores):
            print("Error: Ya existe un profesor con esa cédula.")
            return

        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        email = input("Email: ")
        max_carga = pedir_entero("Max Carga: ")
        
        nuevo_profesor = Profesor(cedula, nombre, apellido, email, max_carga, [])
        self.profesores.append(nuevo_profesor)
        print("Profesor agregado exitosamente.")

    def eliminar(self):
        """
        Elimina a un profesor mediante la cédula.
        Avisa si una materia se queda sin profesores que puedan darla.
        Eficiencia: O(P * M) donde P=profesores, M=materias del profesor eliminado
        """
        cedula = pedir_entero("Ingrese cédula del profesor a eliminar: ")
        profesor = next((p for p in self.profesores if p.cedula == cedula), None)
        
        if not profesor:
            print("Profesor no encontrado.")
            return

        # Verificar si alguna materia queda huérfana
        materias_en_riesgo = []
        for mat in profesor.materias:
            # Hay otro profesor que da esta materia?
            if sum(1 for p in self.profesores if mat in p.materias) == 1:
                materias_en_riesgo.append(mat)
                
        if materias_en_riesgo:
            print(f"ADVERTENCIA: Eliminar a este profesor dejará las siguientes materias sin profesores: {', '.join(materias_en_riesgo)}")
            if not confirmar("¿Está seguro que desea eliminar a este profesor?"):
                return
                
        self.profesores.remove(profesor)
        print("Profesor eliminado.")

    def modificar_materias(self):
        """
        Permite agregar o quitar materias asignadas a un profesor.
        Avisa si quitar materia deja la misma sin profesores.
        Eficiencia: O(P) por búsqueda de profesor, O(1) modificar.
        """
        cedula = pedir_entero("Cédula del profesor: ")
        profesor = next((p for p in self.profesores if p.cedula == cedula), None)
        
        if not profesor:
            print("Profesor no encontrado.")
            return
            
        print(f"Materias actuales: {profesor.materias}")
        opciones = ["Agregar materia", "Quitar materia"]
        sel = crear_menu("Modificar Materias", opciones, funcion_volver=True)
        
        if sel == 1:
            cod = input("Código de la materia a agregar: ").upper()
            if cod not in self.materias_codigos:
                print("Ese código de materia no existe en el sistema.")
            else:
                profesor.agregar_materia(cod)
                print("Materia agregada al profesor.")
                
        elif sel == 2:
            cod = input("Código de la materia a quitar: ").upper()
            if cod in profesor.materias:
                # Verificar riesgo huerfano
                if sum(1 for p in self.profesores if cod in p.materias) == 1:
                    print(f"ADVERTENCIA: Quitar esta materia dejaría a {cod} sin profesores que la puedan dar.")
                    if not confirmar("¿Desea quitarla de todos modos?"):
                        return
                        
                profesor.eliminar_materia(cod)
                print("Materia eliminada del profesor.")
            else:
                print("El profesor no tiene esa materia asignada.")
