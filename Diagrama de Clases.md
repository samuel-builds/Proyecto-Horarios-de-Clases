# Diagrama de Clases del Sistema

```mermaid
classDiagram
    class Materia {
        +String codigo
        +String nombre
        +int secciones
        +__init__(codigo, nombre, secciones)
        +__str__() String
    }

    class Profesor {
        +int cedula
        +String nombre
        +String apellido
        +String email
        +int max_carga
        +List~String~ materias
        +__init__(cedula, nombre, apellido, email, max_carga, materias)
        +puede_impartir(codigo_materia) bool
        +agregar_materia(codigo_materia)
        +eliminar_materia(codigo_materia)
        +__str__() String
    }

    class SeccionHorario {
        +Materia materia
        +Profesor profesor
        +String bloque_tiempo
        +String estado
        +__init__(materia, profesor, bloque_tiempo, estado)
        +__str__() String
    }

    class DataManager {
        <<static>>
        +descargar_datos() Tuple~List~Materia~, List~Profesor~~
        +guardar_horario_csv(horario, filename)
        +cargar_horario_csv(filename) Tuple~List~SeccionHorario~, List~Materia~, List~Profesor~~
    }

    class ProfesoresModule {
        +List~Profesor~ profesores
        +List~String~ materias_codigos
        +menu_principal()
        +ver_lista()
        +ver_especifico()
        +agregar()
        +eliminar()
        +modificar_materias()
    }

    class MateriasModule {
        +List~Materia~ materias
        +List~Profesor~ profesores
        +menu_principal()
        +ver_lista()
        +ver_especifico()
        +ver_profesores()
        +agregar()
        +eliminar()
        +modificar_secciones()
    }

    class GeneracionModule {
        +List~Materia~ materias
        +List~Profesor~ profesores
        +List~SeccionHorario~ horario
        +int salones_disponibles
        +generar() List~SeccionHorario~
        -obtener_profesor_disponible()
        -intentar_reasignacion()
        +reportar_resultados()
        +menu_post_generacion()
    }

    class ModificacionModule {
        +List~SeccionHorario~ horario
        +List~Profesor~ profesores
        +int salones_totales
        +modificar() List~SeccionHorario~
        -_cambiar_profesor()
        -_cambiar_horario()
    }

    class EstadisticasModule {
        +List~SeccionHorario~ horario
        +List~Profesor~ profesores
        +List~Materia~ materias
        +graficar_salones_ocupados()
        +graficar_carga_profesores()
        +graficar_secciones_cerradas()
    }

    class Aplicacion {
        +List~Materia~ materias
        +List~Profesor~ profesores
        +List~SeccionHorario~ horario
        +ejecutar()
        -_menu_modulos()
    }

    SeccionHorario --> Materia : "referencia a"
    SeccionHorario --> Profesor : "referencia a (opcional)"
    ProfesoresModule --> Profesor : "gestiona"
    MateriasModule --> Materia : "gestiona"
    GeneracionModule --> SeccionHorario : "crea"
    ModificacionModule --> SeccionHorario : "modifica"
    EstadisticasModule --> SeccionHorario : "lee"
    Aplicacion --> DataManager : "utiliza"
    Aplicacion --> ProfesoresModule : "instancia"
    Aplicacion --> MateriasModule : "instancia"
    Aplicacion --> GeneracionModule : "instancia"
    Aplicacion --> EstadisticasModule : "instancia"
```
