import os
print("Le script est en cours d'exécution...")
print(f"Fichiers dans le dossier : {os.listdir()}")

from PIL import Image
import exifread

def get_gps_info(image_path):
    # Ouvrir l'image et extraire les métadonnées EXIF
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f, details=False)

    # Extraire les coordonnées GPS
    gps_latitude = tags.get('GPS GPSLatitude')
    gps_longitude = tags.get('GPS GPSLongitude')
    gps_latitude_ref = tags.get('GPS GPSLatitudeRef')
    gps_longitude_ref = tags.get('GPS GPSLongitudeRef')

    # Extraire la date et l'heure
    date_time = tags.get('EXIF DateTimeOriginal')

    # Convertir les coordonnées GPS en format décimal
    if gps_latitude and gps_longitude:
        lat = convert_to_decimal(gps_latitude.values, gps_latitude_ref.values)
        lon = convert_to_decimal(gps_longitude.values, gps_longitude_ref.values)
    else:
        lat, lon = None, None

    return lat, lon, date_time

def convert_to_decimal(coord, ref):
    # Convertir les coordonnées GPS (degrés, minutes, secondes) en décimal
    degrees = coord[0].num / coord[0].den
    minutes = coord[1].num / coord[1].den
    seconds = coord[2].num / coord[2].den
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']:
        decimal *= -1
    return decimal

# Remplace 'ta_photo.jpg' par le nom de ton fichier
image_path = 'photo0.jpg'
latitude, longitude, date_time = get_gps_info('photo0.jpg')

if latitude and longitude:
    print(f"Coordonnées GPS : Latitude = {latitude}, Longitude = {longitude}")
else:
    print("Aucune coordonnée GPS trouvée dans l'image.")

if date_time:
    print(f"Date et heure : {date_time}")
else:
    print("Aucune date/heure trouvée dans l'image.")