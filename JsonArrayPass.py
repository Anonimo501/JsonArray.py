import json
import os

def pedir_entero(mensaje, minimo=0):
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit() and int(valor) >= minimo:
            return int(valor)
        print(f"❌ Ingresa un número entero válido (>= {minimo}).")

def pedir_ruta_archivo(mensaje):
    while True:
        ruta = input(mensaje).strip().strip('"').strip("'")
        if not ruta:
            print("❌ Debes ingresar una ruta válida.")
            continue
        if not os.path.isfile(ruta):
            print(f"❌ El archivo '{ruta}' no existe. Intenta de nuevo.")
            continue
        return ruta

def main():
    print("=== Generador de JSON por lotes para Burp Suite ===\n")

    # Pedir archivo de credenciales
    ruta = pedir_ruta_archivo("Ruta del archivo de credenciales (ej. passwords.txt): ")

    # Leer credenciales (una por línea, ignorando vacías)
    with open(ruta, "r", encoding="utf-8", errors="replace") as f:
        credenciales = [linea.rstrip("\n").rstrip("\r") for linea in f]
    credenciales = [c for c in credenciales if c.strip() != ""]

    if not credenciales:
        print("❌ El archivo no contiene credenciales válidas.")
        return

    print(f"\n📄 Credenciales cargadas: {len(credenciales)}")

    # Pregunta cuántos elementos por lote (línea del array)
    lote = pedir_entero("Elementos por lote (ej. 10, 50, 100): ", minimo=1)

    salida = []
    lote_actual = []

    for cred in credenciales:
        # Escapa comillas y barras invertidas para JSON válido
        cred_escapada = cred.replace("\\", "\\\\").replace('"', '\\"')
        lote_actual.append(f'"{cred_escapada}"')

        if len(lote_actual) == lote:
            salida.append("  " + ", ".join(lote_actual))
            lote_actual = []

    # Último lote parcial
    if lote_actual:
        salida.append("  " + ", ".join(lote_actual))

    # Construye el JSON tipo array por lotes
    json_final = "[\n" + ",\n".join(salida) + "\n]"

    # Guarda en archivo
    with open("passwords.json", "w", encoding="utf-8") as f:
        f.write(json_final)

    print(f"\n✅ Archivo generado: passwords.json")
    print(f"   Total de elementos: {len(credenciales)}")
    print(f"   Formato: {lote} por lote\n")

    # Muestra una vista previa
    print("--- Vista previa (primeras líneas) ---")
    print("\n".join(json_final.splitlines()[:6]))
    print("...")

if __name__ == "__main__":
    main()
