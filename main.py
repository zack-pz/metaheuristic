import random
from modules.models import Task, ResourceVector
from modules.algorithms import solve_ffd, optimize_servers

def main():
    print("Generando simulación de FinOps Cloud Optimizer (Multidimensional)...\n")
    
    # 1. Definir Capacidad Estándar del Servidor (Template)
    # Ejemplo: Instancia tipo 'm5.2xlarge' pero con buffer de seguridad (80% rule)
    server_capacity_template = ResourceVector(
        cpu=80,      # 80% de uso seguro sobre 100%
        ram=64,      # 64 GB RAM
        iops=5000,   # IOPS
        net_bw=10,   # 10 Gbps
        gpu=0,       # Sin GPU por defecto en nodos generales
        energy=1000  # Unidades térmicas arbitrarias
    )
    
    # 2. Generar Datos (30 tareas heterogéneas)
    random.seed(42)
    tasks = []
    for i in range(30):
        # Generamos perfiles de carga variados:
        # Algunas tareas son CPU intensive, otras RAM intensive, etc.
        r_cpu = random.randint(5, 30)
        r_ram = random.randint(1, 16)
        r_iops = random.randint(100, 1000)
        r_net = random.randint(1, 3)
        r_gpu = 1 if random.random() > 0.9 else 0 # 10% probabilidad de requerir GPU
        
        # Las tareas GPU-bound suelen consumir mucha energía
        r_energy = (r_cpu * 2) + (r_gpu * 100) 
        
        tasks.append(Task(i+1, ResourceVector(r_cpu, r_ram, r_iops, r_net, r_gpu, r_energy)))
    
    print(f"Total Tareas: {len(tasks)}")
    print(f"Capacidad por Servidor: {server_capacity_template}")
    
    # Análisis simple de recursos totales
    total_cpu = sum(t.resources.cpu for t in tasks)
    total_ram = sum(t.resources.ram for t in tasks)
    print(f"Demanda Total: CPU={total_cpu}%, RAM={total_ram}GB")
    
    # 3. Ejecutar Fase 1 (FFD Multidimensional)
    initial_servers = solve_ffd(tasks, server_capacity_template)
    count_initial = len(initial_servers)
    print(f"\nResultados Fase 1 (FFD Multidimensional): {count_initial} Servidores utilizados.")
    for s in initial_servers:
        print(f"  {s}")
        
    # 4. Ejecutar Fase 2 (Metaheurística)
    final_servers = optimize_servers(initial_servers, max_iterations=50)
    count_final = len(final_servers)
    
    # 5. Reporte Final
    print("\n" + "="*50)
    print("REPORTE DE OPTIMIZACIÓN DE COSTOS (MULTIDIMENSIONAL)")
    print("="*50)
    print(f"Servidores iniciales: {count_initial}")
    print(f"Servidores finales tras optimización: {count_final}")
    print(f"Ahorro total: {count_initial - count_final} servidores")
    print("-" * 50)
    print("Estado Final de la Infraestructura:")
    final_servers.sort(key=lambda s: s.server_id)
    for s in final_servers:
        # Mostramos Score de utilización para ver qué tan bien empaquetado está
        print(f"  S{s.server_id} [Score: {s.utilization_score():.2f}] | Load: {s.current_load}")

if __name__ == "__main__":
    main()