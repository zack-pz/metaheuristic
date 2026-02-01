import copy
import random
from .models import Server, ResourceVector

# ==========================================
# Fase 1: Construcción Inicial (Ordenamiento + Greedy)
# ==========================================

def solve_ffd(tasks, server_capacity_template):
    """
    Implementa First Fit Decreasing (FFD) Multidimensional.
    1. Ordenamiento: Ordena por 'peso' de la tarea (usando CPU + RAM como proxy).
    2. Búsqueda Greedy: Coloca cada tarea en el primer servidor que quepa en TODAS las dimensiones.
    """
    # Heurística: Ordenar por uso intensivo de recursos (CPU prioritario, luego RAM)
    # Esto ayuda a acomodar las tareas más "difíciles" primero.
    sorted_tasks = sorted(tasks, 
                          key=lambda x: (x.resources.cpu * 0.6 + x.resources.ram * 0.4), 
                          reverse=True)
    
    servers = []
    server_id_counter = 1
    
    for task in sorted_tasks:
        placed = False
        for server in servers:
            if server.add_task(task):
                placed = True
                break
        
        if not placed:
            # Crear nuevo servidor clonando la capacidad base
            # Nota: server_capacity_template debe ser un ResourceVector
            new_server = Server(server_id_counter, capacity=copy.deepcopy(server_capacity_template))
            server_id_counter += 1
            new_server.add_task(task)
            servers.append(new_server)
            
    return servers

# ==========================================
# Fase 2: Optimización Metaheurística
# ==========================================

def optimize_servers(servers, max_iterations=50):
    """
    Intenta mejorar la solución inicial eliminando servidores subutilizados.
    Estrategia: Búsqueda Local Iterativa + Perturbación (Move & Swap) Multidimensional.
    """
    print(f"\n--- Iniciando Fase 2: Optimización Metaheurística ({max_iterations} intentos máx) ---")
    
    current_solution = servers
    
    for i in range(max_iterations):
        # 1. Identificación: Ordenar servidores por score de utilización (ascendente).
        # Queremos vaciar los que tienen score bajo.
        current_solution.sort(key=lambda s: s.utilization_score())
        
        if len(current_solution) < 2:
            break 
            
        server_eliminated = False
        candidates_checked = 0
        
        # Intentamos vaciar los servidores empezando por el más vacío.
        for candidate_idx in range(len(current_solution)):
            candidates_checked += 1
            candidate_server = current_solution[candidate_idx]
            
            # Lista de servidores destino (todos menos el candidato)
            other_servers = current_solution[:candidate_idx] + current_solution[candidate_idx+1:]
            
            # Simulamos el movimiento
            simulation_servers = copy.deepcopy(other_servers)
            
            # Best Fit Multidimensional: Ordenar destinos por capacidad restante "ajustada"
            # (Prefiriendo los que están casi llenos pero donde aún cabe algo)
            simulation_servers.sort(key=lambda s: s.utilization_score(), reverse=True)
            
            tasks_to_reallocate = candidate_server.tasks
            all_reallocated = True
            
            for task in tasks_to_reallocate:
                placed = False
                for target in simulation_servers:
                    if target.add_task(task):
                        placed = True
                        break
                if not placed:
                    all_reallocated = False
                    break
            
            if all_reallocated:
                print(f"  [Iteración {i+1}] ¡ÉXITO! Servidor {candidate_server.server_id} vaciado (Score: {candidate_server.utilization_score():.2f}).")
                current_solution = simulation_servers
                server_eliminated = True
                break 
        
        if not server_eliminated:
            # ESTRATEGIA DE PERTURBACIÓN
            perturbation_success = False
            action_type = "MOVE" if random.random() > 0.4 else "SWAP"
            
            # === ESTRATEGIA 1: MOVER (Relocation) ===
            if action_type == "MOVE":
                available_sources = [s for s in current_solution if s.tasks]
                random.shuffle(available_sources)
                
                for source in available_sources:
                    if perturbation_success: break
                    task_to_move = random.choice(source.tasks)
                    possible_targets = [s for s in current_solution if s != source]
                    random.shuffle(possible_targets)
                    
                    for target in possible_targets:
                        if target.can_fit(task_to_move):
                            source.remove_task(task_to_move)
                            target.add_task(task_to_move)
                            print(f"  [Iteración {i+1}] Perturbación (MOVE): Tarea T{task_to_move.task_id} de S{source.server_id} -> S{target.server_id}.")
                            perturbation_success = True
                            break
                            
            # === ESTRATEGIA 2: INTERCAMBIAR (Swap) ===
            if not perturbation_success:
                servers_with_tasks = [s for s in current_solution if s.tasks]
                if len(servers_with_tasks) >= 2:
                    s1, s2 = random.sample(servers_with_tasks, 2)
                    for _ in range(5): # Intentar 5 pares
                        t1 = random.choice(s1.tasks)
                        t2 = random.choice(s2.tasks)
                        
                        # Simular el swap
                        # 1. Quitar tareas actuales
                        # 2. Verificar si caben las nuevas (matemática de vectores)
                        
                        # Capacidad remanente SIN la tarea que vamos a quitar
                        rem_s1 = s1.remaining_capacity() + t1.resources 
                        rem_s2 = s2.remaining_capacity() + t2.resources
                        
                        # Verificar cruce
                        if t2.resources.fits_in(rem_s1) and t1.resources.fits_in(rem_s2):
                            s1.remove_task(t1)
                            s1.add_task(t2)
                            s2.remove_task(t2)
                            s2.add_task(t1)
                            print(f"  [Iteración {i+1}] Perturbación (SWAP): T{t1.task_id} (S{s1.server_id}) <-> T{t2.task_id} (S{s2.server_id}).")
                            perturbation_success = True
                            break
            
            if not perturbation_success:
                print(f"  [Iteración {i+1}] Sistema demasiado ajustado (Multidimensional). No se pudo perturbar.")
            
    return current_solution
