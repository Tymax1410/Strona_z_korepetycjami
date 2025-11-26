import os

print("-" * 30)
print(f"LOKALIZACJA: {os.getcwd()}")
print("-" * 30)

# 1. Sprawdź jakie foldery widzi system
foldery = [f for f in os.listdir('.') if os.path.isdir(f)]
print(f"FOLDERY NA DYSKU: {foldery}")

# 2. Sprawdź co jest zapisane w manage.py
print("\nZAWARTOŚĆ MANAGE.PY (linia ustawień):")
try:
    with open('manage.py', 'r') as f:
        found = False
        for line in f:
            if 'DJANGO_SETTINGS_MODULE' in line:
                print(f" >> {line.strip()}")
                found = True
        if not found:
            print(" >> BŁĄD: Nie znaleziono linii DJANGO_SETTINGS_MODULE!")
except FileNotFoundError:
    print(" >> BŁĄD: Nie widzę pliku manage.py!")

print("-" * 30)