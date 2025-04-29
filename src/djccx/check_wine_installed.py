import subprocess

def check_wine_installed():
    try:
        # Ejecutar el comando 'wine --version' para verificar si Wine está instalado
        result = subprocess.run(['wine', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Verificar si el comando se ejecutó correctamente
        if result.returncode == 0:
            # Extraer la salida y mostrar la versión de Wine
            version = result.stdout.decode('utf-8').strip()
            print(f"Wine está instalado. Versión: {version}")
            return True
        else:
            # Wine no está instalado, o el comando falló
            print("Wine no está instalado o no se pudo ejecutar correctamente.")
            return False
    
    except FileNotFoundError:
        # Este error ocurre si el comando 'wine' no está disponible en el sistema
        print("Wine no está instalado.")
        return False