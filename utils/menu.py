from typing import Optional, List, Callable

def pedir_entero(mensaje: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    """
    Solicita un entero al usuario con validación de rango y tipo.
    Maneja excepciones para evitar que el programa se cierre por errores de Python.
    Eficiencia: O(N) intentos hasta entrada correcta.
    """
    while True:
        try:
            valor = input(mensaje)
            numero = int(valor)
            if min_val is not None and numero < min_val:
                print(f"Error: El valor debe ser mayor o igual a {min_val}.")
                continue
            if max_val is not None and numero > max_val:
                print(f"Error: El valor debe ser menor o igual a {max_val}.")
                continue
            return numero
        except ValueError:
            print("Error: Entrada no válida. Debe ingresar un número entero.")

def confirmar(mensaje: str) -> bool:
    """
    Solicita confirmación (S/N) del usuario.
    Eficiencia: O(N) intentos hasta que se introduce S o N.
    """
    while True:
        respuesta = input(f"{mensaje} (S/N): ").strip().upper()
        if respuesta == 'S':
            return True
        elif respuesta == 'N':
            return False
        else:
            print("Entrada no válida. Ingrese S para Sí o N para No.")

def crear_menu(titulo: str, opciones: List[str], funcion_volver: Optional[Callable] = None) -> Optional[int]:
    """
    Muestra un menú, solicita una opción validada y retorna el número seleccionado.
    O(N) por la longitud de opciones.
    """
    print(f"\n--- {titulo} ---")
    for i, opcion in enumerate(opciones, 1):
        print(f"{i}. {opcion}")
    
    extra_opcion = len(opciones) + 1
    if funcion_volver:
        print(f"{extra_opcion}. Volver/Atrás")
    
    max_idx = extra_opcion if funcion_volver else len(opciones)
    seleccion = pedir_entero("Seleccione una opción: ", 1, max_idx)

    if funcion_volver and seleccion == extra_opcion:
        return None
    
    return seleccion
