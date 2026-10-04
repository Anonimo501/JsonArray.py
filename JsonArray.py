import json

def pedir_entero(mensaje, minimo=0):
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit() and int(valor) >= minimo:
            return int(valor)
        print(f"❌ Ingresa un número entero válido (>= {minimo}).")

def main():
    print("=== Generador de JSON por lotes para Burp Suite ===\n")

    inicio = pedir_entero("Número inicial (ej. 0 para 000000): ")
    fin    = pedir_entero("Número final   (ej. 999999): ")

    if fin < inicio:
        print("❌ El número final debe ser mayor o igual al inicial.")
        return

    # Detecta automáticamente los dígitos según el número más largo
    digitos = len(str(fin))
    print(f"\n🔢 Se usarán {digitos} dígitos (ej. {str(inicio).zfill(digitos)} ... {str(fin).zfill(digitos)})")

    # Pregunta cuántos elementos por lote (línea del array)
    lote = pedir_entero("Elementos por lote (ej. 10, 50, 100): ", minimo=1)

    salida = []
    lote_actual = []

    for i in range(inicio, fin + 1):
        lote_actual.append(f'"{str(i).zfill(digitos)}"')

        if len(lote_actual) == lote:
            salida.append("  " + ", ".join(lote_actual))
            lote_actual = []

    # Último lote parcial
    if lote_actual:
        salida.append("  " + ", ".join(lote_actual))

    # Construye el JSON tipo array por lotes
    json_final = "[\n" + ",\n".join(salida) + "\n]"

    # Guarda en archivo
    with open("pins.json", "w", encoding="utf-8") as f:
        f.write(json_final)

    print(f"\n✅ Archivo generado: pins.json")
    print(f"   Total de elementos: {fin - inicio + 1}")
    print(f"   Formato: {digitos} dígitos, {lote} por lote\n")

    # Muestra una vista previa
    print("--- Vista previa (primeras líneas) ---")
    print("\n".join(json_final.splitlines()[:6]))
    print("...")

if __name__ == "__main__":
    main()
