import os
import django
import csv

# --- Ajusta esto si tu settings están en otro módulo ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_postventa.settings')
django.setup()

from django.contrib.auth.models import User

def limpiar_nombre_columna(h):
    if h is None:
        return ''
    # quitar BOM, espacios, comas finales, puntos, y poner minúsculas
    h = h.replace('\ufeff', '').strip()
    h = h.rstrip(',').rstrip('.')
    return h.lower()

def detectar_delimiter_y_leer_header(path, encoding):
    with open(path, 'r', encoding=encoding, newline='') as f:
        sample = f.read(4096)
        sniffer = csv.Sniffer()
        try:
            dialect = sniffer.sniff(sample)
            delimiter = dialect.delimiter
        except csv.Error:
            delimiter = ','  # fallback
        f.seek(0)
        reader = csv.reader(f, delimiter=delimiter)
        try:
            header = next(reader)
        except StopIteration:
            header = []
        return delimiter, header

def cargar_usuarios_desde_csv(ruta_csv):
    # intentar distintos encodings
    for enc in ('utf-8', 'latin-1', 'windows-1252'):
        try:
            delimiter, header_raw = detectar_delimiter_y_leer_header(ruta_csv, enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise RuntimeError("No se pudo abrir el CSV con encodings utf-8/latin-1/windows-1252")

    # limpiar encabezados
    header_clean = [limpiar_nombre_columna(h) for h in header_raw]
    print("Encabezados detectados (limpios):", header_clean)
    print("Delimiter detectado:", repr(delimiter))

    # posibles nombres alternativos para cada campo
    posibles = {
        'username': {'username','UserName', 'user', 'rut', 'rut', 'user name', 'username,' , 'user_name'},
        'first_name': {'first_name', 'nombres', 'nombre', 'first name', 'nombre(s)'},
        'last_name': {'last_name', 'apellidos', 'apellido', 'ap. paterno ap. materno', 'apellido(s)', 'last name'},
        'email': {'email', 'correo', 'correo_electronico', 'e-mail', 'e mail'}
    }

    # construir mapa de índice por campo esperable
    index_map = {}
    for i, h in enumerate(header_clean):
        for key, variantes in posibles.items():
            if h in variantes or h.replace(' ', '') in variantes:
                index_map[key] = i

    # si no se detectaron, intentar heurísticos simples
    if 'username' not in index_map:
        # buscar 'rut' explícito
        for i, h in enumerate(header_clean):
            if 'rut' in h:
                index_map['username'] = i
    if 'first_name' not in index_map:
        for i,h in enumerate(header_clean):
            if 'nombre' in h:
                index_map['first_name'] = i
    if 'last_name' not in index_map:
        for i,h in enumerate(header_clean):
            if 'ap' in h or 'apellido' in h:
                index_map['last_name'] = i
    if 'email' not in index_map:
        for i,h in enumerate(header_clean):
            if 'mail' in h or 'correo' in h:
                index_map['email'] = i

    print("Mapa de índices detectado:", index_map)

    # si aun faltan campos mínimos, avisar y salir
    if 'username' not in index_map:
        raise KeyError("No se pudo localizar la columna que será usada como 'username' (RUT). "
                       "Encabezados detectados: " + ", ".join(header_raw))

    # ahora leer filas y procesar
    # reabrir con el delimiter correcto y encoding detectado
    with open(ruta_csv, 'r', encoding=enc, newline='') as f:
        reader = csv.reader(f, delimiter=delimiter)
        # saltar header
        next(reader, None)
        for fila in reader:
            # proteger contra filas cortas
            def valor(i):
                try:
                    return fila[i].strip()
                except Exception:
                    return ''

            username = valor(index_map['username'])
            password = username
            first_name = valor(index_map.get('first_name', -1)) if index_map.get('first_name') is not None else ''
            last_name = valor(index_map.get('last_name', -1)) if index_map.get('last_name') is not None else ''
            email = valor(index_map.get('email', -1)) if index_map.get('email') is not None else 'sin correo'
            if not username:
                print("Fila saltada (sin username/RUT):", fila)
                continue

            # crear usuario si no existe
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    email=email or 'sin correo'
                )
                print(f"✅ Usuario {username} creado.")
            else:
                print(f"⚠️ Usuario {username} ya existe.")

if __name__ == "__main__":
    ruta = r"C:\Users\nesto\OneDrive\Escritorio\postventa\gestion_postventa\Book(Hoja1).csv"
    cargar_usuarios_desde_csv(ruta)
