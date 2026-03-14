from models.materia import Materia
from models.profesor import Profesor
from typing import Optional

class SeccionHorario:
    """
    Clase que representa una sección programada (o no) de una materia en un bloque de horario.
    """
    def __init__(self, materia: Materia, profesor: Optional[Profesor], bloque_tiempo: str, estado: str = "programada"):
        """
        Inicializa una nueva instancia de SeccionHorario.
        El estado puede ser "programada", "cerrada" (sin profesor) o "sin_salon".
        Eficiencia: O(1) tiempo y O(1) espacio.
        """
        self.materia = materia
        self.profesor = profesor
        self.bloque_tiempo = bloque_tiempo
        self.estado = estado  # programada, cerrada, sin_salon

    def __str__(self) -> str:
        """
        Devuelve una representación en cadena de la sección.
        Eficiencia: O(1)
        """
        profesor_nombre = f"{self.profesor.nombre} {self.profesor.apellido}" if self.profesor else "N/A"
        return f"[{self.bloque_tiempo}] {self.materia.codigo} - Prof: {profesor_nombre} ({self.estado})"
