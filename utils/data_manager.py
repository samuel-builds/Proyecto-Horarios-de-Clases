import json
import csv
import urllib.request
import urllib.error
from typing import List, Dict, Tuple, Optional
from models.materia import Materia
from models.profesor import Profesor
from models.horario import SeccionHorario

API_BASE_URL = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-2/main/"

class DataManager:
    """
    Clase responsable de la lectura y escritura de datos.
    Descarga desde la API y graba/lee en formato CSV.
    """

    @staticmethod
    def descargar_datos() -> Tuple[List[Materia], List[Profesor]]:
        """
        Descarga los datos de materias y profesores de la API de Github.
        Eficiencia: O(M + P) para decodificar los JSON e instanciar Materia (M) y Profesores (P).
        """
        materias = []
        profesores = []
        try:
            # Descargar materias
            print("Descargando materias2526-2.json...")
            req = urllib.request.Request(API_BASE_URL + "materias2526-2.json")
            with urllib.request.urlopen(req) as f:
                data = json.load(f)
                for d in data:
                    materias.append(Materia(d["Código"], d["Nombre"], d["Secciones"]))
            
            # Descargar profesores
            print("Descargando profesores.json...")
            req = urllib.request.Request(API_BASE_URL + "profesores.json")
            with urllib.request.urlopen(req) as f:
                data = json.load(f)
                for d in data:
                    profesores.append(Profesor(
                        cedula=d["Cedula"],
                        nombre=d["Nombre"],
                        apellido=d["Apellido"],
                        email=d["Email"],
                        max_carga=d["Max Carga"],
                        materias=d["Materias"]
                    ))
            
            print("¡Descarga de datos completada!")
        except Exception as e:
            print(f"Error descargando datos: {e}")
            
        return materias, profesores

    @staticmethod
    def guardar_horario_csv(horario: List[SeccionHorario], filename: str = "horario.csv"):
        """
        Guarda asignación de horarios en formato CSV.
        Eficiencia: O(S) donde S es el número de secciones programadas.
        """
        # Según el requerimiento: permite cargar para parar a mitad.
        # Guardaremos el formato que permita reconstruir también Materias, Profesores 
        # y qué se le ha asignado, o simplificado a un CSV que almacena estado.
        # Para el propósito de visualización rápida con MS Excel: 
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Bloque", "Codigo Materia", "Nombre Materia", "Estado", "Cedula Profesor", "Nombre Profesor"])
                for s in horario:
                    prof_cedula = s.profesor.cedula if s.profesor else ""
                    prof_nombre = f"{s.profesor.nombre} {s.profesor.apellido}" if s.profesor else ""
                    writer.writerow([s.bloque_tiempo, s.materia.codigo, s.materia.nombre, s.estado, prof_cedula, prof_nombre])
                    
            print(f"Horario guardado exitosamente en {filename}")
        except Exception as e:
            print(f"Error guardando horario: {e}")

    @staticmethod
    def cargar_horario_csv(filename: str = "horario.csv") -> Tuple[List[SeccionHorario], List[Materia], List[Profesor]]:
        """
        Carga una lista de horarios desde un archivo CSV.
        También reconstruye las listas temporales para seguir la ejecución.
        Como requerimiento pide: "ser capaz de cargar archivos CSV para permitir parar a mitad de la modificación y continuar más tarde."
        En una implementación completa, se podría requerir grabar el estado entero. Aquí lo inferimos.
        Eficiencia: O(L) líneas leídas. Reconstrucción parcial para demostración.
        """
        horario = []
        materias_dict = {}
        profesores_dict = {}

        try:
            with open(filename, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cod_mat = row["Codigo Materia"]
                    nom_mat = row["Nombre Materia"]
                    # Suponemos seccion = 1 por entrada del CSV (ya que cada row es una seccion)
                    if cod_mat not in materias_dict:
                        materias_dict[cod_mat] = Materia(cod_mat, nom_mat, 0)
                    mat = materias_dict[cod_mat]
                    
                    estado = row["Estado"]
                    prof = None
                    if row["Cedula Profesor"]:
                        cedula = int(row["Cedula Profesor"])
                        if cedula not in profesores_dict:
                            partes = row["Nombre Profesor"].split()
                            nombre_p = partes[0] if partes else ""
                            apellido_p = " ".join(partes[1:]) if len(partes) > 1 else ""
                            profesores_dict[cedula] = Profesor(cedula, nombre_p, apellido_p, "", 99, [cod_mat])
                        prof = profesores_dict[cedula]
                        
                    horario.append(SeccionHorario(mat, prof, row["Bloque"], estado))
                    
            print(f"Horario cargado exitosamente desde {filename}")
        except FileNotFoundError:
            print(f"No se encontró el archivo '{filename}'.")
        except Exception as e:
            print(f"Error cargando el archivo: {e}")
            
        return horario, list(materias_dict.values()), list(profesores_dict.values())
