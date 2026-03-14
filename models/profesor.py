from typing import List

class Profesor:
    """
    Clase que representa a un profesor en el sistema.
    Almacena su cédula, nombre, apellido, email, carga máxima y las materias que puede impartir.
    """
    def __init__(self, cedula: int, nombre: str, apellido: str, email: str, max_carga: int, materias: List[str]):
        """
        Inicializa una nueva instancia de Profesor.
        Eficiencia: O(1) tiempo (referencia a la lista) y O(1) espacio.
        """
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.max_carga = max_carga
        self.materias = materias if materias is not None else []

    def puede_impartir(self, codigo_materia: str) -> bool:
        """
        Verifica si el profesor puede impartir una materia dada su código.
        Eficiencia: O(N) donde N es el número de materias que imparte el profesor.
        """
        return codigo_materia in self.materias

    def agregar_materia(self, codigo_materia: str):
        """
        Agrega una materia a la lista de materias que puede impartir.
        Eficiencia: O(1) tiempo amortizado (append a lista).
        """
        if codigo_materia not in self.materias:
            self.materias.append(codigo_materia)

    def eliminar_materia(self, codigo_materia: str):
        """
        Elimina una materia de la lista que puede impartir.
        Eficiencia: O(N) donde N es el número de materias por búsqueda y eliminación.
        """
        if codigo_materia in self.materias:
            self.materias.remove(codigo_materia)

    def __str__(self) -> str:
        """
        Devuelve una representación en cadena del profesor.
        Eficiencia: O(N) por la conversión de la lista de materias.
        """
        return f"{self.cedula} - {self.nombre} {self.apellido} (Carga Max: {self.max_carga}) [Materias: {', '.join(self.materias)}]"
