import requests

def enviar_archivo(inp_file_path, email=None, machine_type="auto"):
    url = "https://djccx.feacluster.com/djccx.php"

    # Parámetros del formulario
    payload = {
        "user_wants": "upload",
        "MAX_FILE_SIZE": "150000000",
        "email": email,
        "machine": machine_type,
    }

    # Archivo a cargar
    files = {"deck": open(inp_file_path, "rb")}

    # Realizar la solicitud POST
    response = requests.post(url, data=payload, files=files)

    # Verificar la respuesta
    if response.status_code == 200:
        print("Archivo enviado correctamente.")
        print("Respuesta del servidor:")
        # find         <p>You can view your running job files <a href=https://djccx.feacluster.com/gce/jobs/b4af7sgz>here</a>.
        # and take the link
        link = link = r.text.split("You can view your running job files")[1].split(">here<")[0].split("href=")[1]
        print(link)
    else:
        print(f"Error al enviar el archivo. Código de estado: {response.status_code}")
    return response,link


# Uso de la función
archivo_inp = os.path.join(output_folder,"simulation","all_to_run.inp")
r,link = enviar_archivo(archivo_inp, email="jesus.oroya@amsimulation.com", machine_type="google-4-16")

# link results.tar.gz
link_results = link + "/results.tar.gz"
# download results.tar.gz
import urllib.request
urllib.request.urlretrieve(link_results, os.path.join(output_folder,"simulation","results.tar.gz"))
# extract results.tar.gz
import tarfile
tar = tarfile.open(os.path.join(output_folder,"simulation","results.tar.gz"))
tar.extractall(path=os.path.join(output_folder,"simulation"))

class MachineOptions:
    OPTIONS = {
        "auto": "Automatically select for me",
        "google-4-16": "2 CPUs - 16 GB RAM - 30 minutes",
        "google-8-32": "4 CPUs - 32 GB RAM - 20 minutes",
        "google-16-64": "8 CPUs - 64 GB RAM - 15 minutes",
        "google-30-120": "15 CPUs - 120 GB RAM - 10 minutes",
        "google-60-240": "30 CPUs - 240 GB RAM - 7 minutes",
    }

    @classmethod
    def get_options(cls):
        return cls.OPTIONS

    @classmethod
    def get_description(cls, option):
        return cls.OPTIONS.get(option, "Invalid option")

# Uso de la clase
machine_options = MachineOptions()

# Obtener todas las opciones
all_options = machine_options.get_options()
print("Todas las opciones disponibles:")
for option, description in all_options.items():
    print(f"{option}: {description}")

# Obtener la descripción de una opción específica
selected_option = "google-8-32"
description = machine_options.get_description(selected_option)
print(f"\nDescripción de la opción '{selected_option}': {description}")