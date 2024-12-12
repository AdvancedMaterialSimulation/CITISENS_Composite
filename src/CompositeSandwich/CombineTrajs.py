
import numpy as np
# Función que determina si dos trayectorias están conectadas
def is_connected(traj1, traj2, threshold):
    return np.linalg.norm(traj1[-1] - traj2[0]) < threshold

def CombineTrajs(all_trajs):
    
    # Agrupación de trayectorias conectadas
    threshold = 1  # Ajusta según tus datos
    final_trajs = []

    while all_trajs:
        current_traj = all_trajs.pop(0)  # Toma la primera trayectoria
        combined = False

        for i, other_traj in enumerate(all_trajs):
            if is_connected(current_traj, other_traj, threshold):
                current_traj = np.vstack([current_traj, other_traj])  # Conecta las trayectorias
    
                all_trajs.pop(i)  # Elimina la trayectoria conectada
                
                # añade la trayectoria combinada al final de la lista
                all_trajs.append(current_traj)
                
                combined = True
                break  # Reinicia el proceso para seguir uniendo trayectorias

            if is_connected(other_traj,current_traj, threshold):
                current_traj = np.vstack([other_traj, current_traj])
                all_trajs.pop(i)

                all_trajs.append(current_traj)
                combined = True
                break

        if not combined:
            final_trajs.append(current_traj)  # Si no se conecta, es una trayectoria completa

    return final_trajs