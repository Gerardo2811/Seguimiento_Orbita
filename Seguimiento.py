from skyfield.api import load, Topos
from geopy.geocoders import Nominatim
import time

def seguimientoSatelite():
    # Crear un objeto geocoder de Nominatim
    geolocator = Nominatim(user_agent="my_app")

    # Obtener la ubicación actual basada en la dirección IP
    location = geolocator.geocode("192.168.1.2")#Colocas la Ip de tu dispositivo, esta es una ip de ejemplo

    # Obtener la latitud, longitud y elevación de el observador, es decir, tu maquina
    latitude = location.latitude
    longitude = location.longitude
    elevation = location.altitude

    # Imprimir los resultados
    print(f"Latitud del observador: {latitude}")
    print(f"Longitud del observador: {longitude}")
    print("----------------------------------------------------------------")

    # Cargar los datos de efemérides de satélites
    satellites = load.tle_file('./Satelites.tle')# te en ceunta que debes disponer del archivo .tle con sus datos

    # Nombre del satélite que deseas rastrear
    satellite_name = 'CUBESAT XI-IV (CO-57)' # este nombre aparece en las especificaciones de tu archivo .tle

    # Buscar el satélite con el nombre 
    satellite = None
    for sat in satellites:
        if sat.name.strip() == satellite_name:
            satellite = sat
            break

    if satellite is not None:
        # Crear un objeto Topos para la ubicación del observador
        observatory = Topos(latitude, longitude, elevation_m=elevation)
        i=1
        while True:
            # Obtener el tiempo actual
            ts = load.timescale()
            t = ts.now()

            # Calcular la posición del satélite en tiempo real
            satellite_position = satellite.at(t)

            # Calcular la posición del observador en tiempo real
            observer_position = observatory.at(t)

            # Calcular la posición relativa del satélite en relación con el observador
            relative_position = satellite_position - observer_position

            # Obtener los ángulos de azimut y elevación
            azimuth, elevation, _ = relative_position.altaz()
            

            # Imprimir los resultados
            print(f"---Posicion del satelite {satellite_name} en su seguimiento #:{i}---")
            print(f"Angulo de azimut: {azimuth.degrees} grados")
            print(f"Angulo de elevacion: {elevation.degrees} grados")
            print("---------------------------------------------------------------------")
            i+=1
            # Esperar un tiempo antes de la siguiente iteración (por ejemplo, 10 segundos)
            time.sleep(10)
    else:
        print("No se encontró el satélite especificado")
