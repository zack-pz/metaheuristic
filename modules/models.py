class ResourceVector:
    """
    Representa un conjunto vectorial de recursos de hardware.
    Encapsula la lógica matemática para sumar, restar y comparar recursos multidimensionales.
    """
    def __init__(self, cpu=0, ram=0, iops=0, net_bw=0):
        self.cpu = cpu          # Cores / %
        self.ram = ram          # GB
        self.iops = iops        # Operations/sec
        self.net_bw = net_bw    # Mbps/Gbps

    def __add__(self, other):
        return ResourceVector(
            self.cpu + other.cpu,
            self.ram + other.ram,
            self.iops + other.iops,
            self.net_bw + other.net_bw
        )

    def __sub__(self, other):
        return ResourceVector(
            self.cpu - other.cpu,
            self.ram - other.ram,
            self.iops - other.iops,
            self.net_bw - other.net_bw
        )

    def fits_in(self, other):
        """Devuelve True si TODOS los recursos de self son menores o iguales a other."""
        return (self.cpu <= other.cpu and
                self.ram <= other.ram and
                self.iops <= other.iops and
                self.net_bw <= other.net_bw)

    def __repr__(self):
        return (f"(CPU:{self.cpu}, RAM:{self.ram}, IO:{self.iops}, "
                f"Net:{self.net_bw})")

class Task:
    """
    Representa una carga de trabajo con requerimientos multidimensionales.
    """
    def __init__(self, task_id, resources: ResourceVector):
        self.task_id = task_id
        self.resources = resources

    def __repr__(self):
        return f"[T{self.task_id} {self.resources}]"

class Server:
    """
    Representa un servidor con capacidades multidimensionales fijas.
    """
    def __init__(self, server_id, capacity: ResourceVector, cost_tier=1.0):
        self.server_id = server_id
        self.capacity = capacity
        self.cost_tier = cost_tier  # Multiplicador de costo para FinOps
        
        # Estado actual (inicialmente vacío)
        self.current_load = ResourceVector() 
        self.tasks = []

    def can_fit(self, task):
        """Verifica si la tarea cabe respetando TODAS las dimensiones."""
        projected_load = self.current_load + task.resources
        return projected_load.fits_in(self.capacity)

    def add_task(self, task):
        """Asigna una tarea si cabe."""
        if self.can_fit(task):
            self.tasks.append(task)
            self.current_load = self.current_load + task.resources
            return True
        return False
        
    def remove_task(self, task):
        """Elimina una tarea y libera recursos."""
        if task in self.tasks:
            self.tasks.remove(task)
            self.current_load = self.current_load - task.resources
            return True
        return False

    def remaining_capacity(self):
        """Calcula el vector de espacio libre."""
        return self.capacity - self.current_load

    def utilization_score(self):
        """
        Calcula un puntaje de uso (0.0 a 1.0) para heurísticas.
        Promedio simple de uso de CPU y RAM (las dimensiones más críticas).
        """
        cpu_usage = self.current_load.cpu / self.capacity.cpu if self.capacity.cpu > 0 else 0
        ram_usage = self.current_load.ram / self.capacity.ram if self.capacity.ram > 0 else 0
        return (cpu_usage + ram_usage) / 2

    def __repr__(self):
        return f"S{self.server_id} [Tier:{self.cost_tier}] | Load: {self.current_load} | Tasks: {len(self.tasks)}"
