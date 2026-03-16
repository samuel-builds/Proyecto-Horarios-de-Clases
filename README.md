# Proyecto: Horarios de Clases

**Materia:** Algoritmos y Programación (BPTSP05)  
**Trimestre:** 2526-2  
**Lenguaje:** Python 3.x  

## Descripción

Este proyecto es un sistema interactivo en consola desarrollado bajo el paradigma de Programación Orientada a Objetos (POO). Permite a Control de Estudios gestionar y planificar horarios para el trimestre, asignando automáticamente materias a profesores sin superar su capacidad máxima y respetando la disponibilidad de salones de clase por cada bloque horario.

## Estructura del Proyecto

```text
📦 Proyecto-Horarios-de-Clases
 ┣ 📂 models/       # Clases de datos (Materia, Profesor, SeccionHorario)
 ┣ 📂 modules/      # Lógica de negocio y módulos (Generador, Estadísticas, CRUDs)
 ┣ 📂 utils/        # Validaciones de menú por consola e interacción con la API Github
 ┣ 📜 Main.py       # Archivo principal para iniciar la ejecución del sistema
 ┗ 📜 Diagrama de Clases.md # Arquitectura de POO interactiva
```

## Requisitos y Configuración

El proyecto corre de forma nativa en Python sin necesidad de librerías externas complejas, a excepción del módulo de validación visual de métricas.

1. Instalar Python 3.x en el equipo.
2. (Para los Puntos Adicionales) Se requiere instalar la librería **Matplotlib** para visualizar gráficas. En la consola ejecutar:
   ```bash
   pip install matplotlib
   ```

## Instrucciones de Uso

1. Abrir la consola de comandos en el directorio del proyecto.
2. Iniciar el programa corriendo:
   ```bash
   python Main.py
   ```
3. Seguir las instrucciones en pantalla:
   * **Recomendación Inicial:** Selecciona en el Menú Principal la Opción 2: *"Descargar los datos de la API de Github"*.
   * Luego, entra al *"Módulo de Generación de horarios"* para correr la asignación inteligente, prueba dándole un límite de `30` salones.
   * Por último, ingresa en el *"Módulo de Estadísticas"* para ver las gráficas (si se instaló Matplotlib).
4. El sistema permite **Guardar** los horarios listos en un CSV llamado `horario.csv` y también **Cargarlos** en futuras sesiones.