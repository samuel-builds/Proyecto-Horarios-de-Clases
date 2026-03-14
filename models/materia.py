class Materia:
    """
    Clase que representa una materia en el sistema.
    Almacena su código, nombre y el número de secciones a asignar.
    """
    def __init__(self, codigo: str, nombre: str, secciones: int):
        """
        Inicializa una nueva instancia de Materia.
        Eficiencia: O(1) tiempo y O(1) espacio.
        """
        self.codigo = codigo
        self.nombre = nombre
        self.secciones = secciones

    def __str__(self) -> str:
        """
        Devuelve una representación en cadena de la materia.
        Eficiencia: O(1)
        """
        return f"{self.codigo} - {self.nombre} (Secciones: {self.secciones})"
