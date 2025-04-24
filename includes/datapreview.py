import msvcrt
from tabulate import tabulate
import textwrap

def zeige_und_bestaetige(daten, max_width=100):
    print("\n📝 Vorschau der Daten:\n")
    tabelle = []

    for key, value in daten.items():
        if isinstance(value, list):
            if all(isinstance(v, str) for v in value):
                value = ", ".join(value)
            else:
                value = str(value)
        if isinstance(value, str):
            value = "\n".join(textwrap.wrap(value, width=max_width))
        tabelle.append((key, value))

    print(tabulate(tabelle, headers=["Feld", "Wert"], tablefmt="fancy_grid"))

    print("\nDrücke [Enter], um fortzufahren, oder [ESC], um abzubrechen.")

    while True:
        taste = msvcrt.getch()
        if taste == b'\x1b':  # ESC
            print("❌ Abgebrochen.")
            return False
        elif taste in (b'\r', b'\n'):  # Enter
            print("✅ Bestätigt.")
            return True