# folder file path 
import os 
import pandas as pd
folder = os.path.dirname(os.path.abspath(__file__))

def experimental():

    # file path
    file_path = os.path.join(folder, 'experimental.csv')

    # read data
    data = pd.read_csv(file_path)

    # return data
    return data


def resina():

    resistencia = 650  # kg/cm2

    resistencia_MPa = resistencia * 9.80665 * 1e4 * 1e-6
    # to newton/m2
    alagamiento = 0.025
    young_modulus = resistencia_MPa / alagamiento

    # https://1library.co/article/resina-ep%C3%B3xica-matrices-polim%C3%A9ricas-optimizaci%C3%B3n-propiedades-mec%C3%A1nicas-compositos.rnzw87ze
    # 0.2-0.33 nu
    nu = 0.5*(0.2+0.33)


    return {
        "resistencia [kg/cm2]": resistencia,
        "alargamiento rotura[%]": alagamiento,
        "resistencia [MPa]": resistencia_MPa,
        "young modulus [MPa]": young_modulus,
        "poisson ratio": nu
    }


def carbonfiber():

    # https://en.wikipedia.org/wiki/Composite_material

    # Coeficiente de Poisson (ν):

    # Longitudinal (0°): Aproximadamente 0,30.
    # Transversal (90°): Aproximadamente 0,50.
    # file path
    file_path = os.path.join(folder, 'carbon.csv')

    # read data
    data = pd.read_csv(file_path)

    # return data
    return {
        "carbon": data,
        "poisson ratio": 0.3
    }

def nucleo():

    return {
        "young modulus [MPa]": 800,
        "poisson ratio": 0.3
    }

def full_experiment():

    file_path = os.path.join(folder, 'full_data.csv')

    df = pd.read_csv(file_path)
    df["Modulo (GPa)"] = df["Modulo (MPa)"] * 1e-3
    df["Modulo flexion (GPa)"] = df["Modulo flexion (MPa)"] * 1e-3
    # 
    # pop
    df = df.drop(columns=["Modulo (MPa)", "Modulo flexion (MPa)"])
    df.head()
    return df


def manual_data():

    t_nucleo_exp_inches = 0.11
    t_nucleo_exp = t_nucleo_exp_inches * 25.4

    Tau_jorge_inches = 0.191
    Tau_jorge = Tau_jorge_inches * 25.4

    return {
        "t_nucleo [mm]": t_nucleo_exp,
        "t total [mm]": Tau_jorge
    }