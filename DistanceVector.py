import sys

class Node:
    def __init__(self, node_id, neighbors):
        """
        Inizializza un nodo.
        
        :param node_id: ID univoco del nodo.
        :param neighbors: dizionario con i nodi vicini e i costi per raggiungerli.
        """
        self.node_id = node_id
        self.neighbors = neighbors
        self.routing_table = {node_id: 0}  # La distanza da se stesso è 0
        
        # Inizializza la tabella di routing con i costi ai nodi vicini
        for neighbor, cost in neighbors.items():
            self.routing_table[neighbor] = cost
        
    def update_routing_table(self, other_routing_table, neighbor_id):
        """
        Aggiorna la tabella di routing in base alle informazioni di un altro nodo.
        
        :param other_routing_table: la tabella di routing di un nodo vicino.
        :param neighbor_id: l'id del vicino per tenere traccia della distanza.
        :return: True se la tabella è cambiata, False altrimenti.
        """
        updated = False
        for dest, dist in other_routing_table.items():
            if dest != self.node_id:
                # Calcola la nuova distanza considerando il percorso attraverso il vicino
                new_dist = dist + self.neighbors.get(neighbor_id, sys.maxsize)
                
                # Se la nuova distanza è più breve, aggiorna la tabella
                if dest not in self.routing_table or self.routing_table[dest] > new_dist:
                    self.routing_table[dest] = new_dist
                    updated = True
        return updated

    def print_routing_table(self):
        """
        Stampa la tabella di routing del nodo.
        """
        print(f"Routing Table for Node {self.node_id}:")
        for dest, dist in self.routing_table.items():
            print(f"  Destination {dest} -> Distance {dist}")
        print()

def distance_vector_routing(nodes):
    """
    Simula il protocollo di routing Distance Vector.
    
    :param nodes: lista di nodi nella rete.
    """
    converged = False
    iteration = 0
    while not converged:
        converged = True
        print(f"\nIteration {iteration + 1}")
        
        # Ogni nodo invia la sua tabella di routing ai suoi vicini e aggiorna la propria tabella
        for node in nodes:
            for neighbor_id in node.neighbors:
                # Ogni nodo invia la sua tabella di routing al vicino
                neighbor = next(n for n in nodes if n.node_id == neighbor_id)
                if node.update_routing_table(neighbor.routing_table, neighbor_id):
                    converged = False
        
        # Stampare le tabelle di routing per ogni nodo
        for node in nodes:
            node.print_routing_table()
        
        iteration += 1

# Funzione per creare la rete
def create_network():
    """
    Crea una rete di nodi e connessioni.
    
    :return: lista di nodi.
    """
    # Ogni nodo ha un dizionario che rappresenta i suoi vicini e i costi per raggiungerli
    node_a = Node('A', {'B': 1, 'C': 4})
    node_b = Node('B', {'A': 1, 'C': 2, 'D': 5})
    node_c = Node('C', {'A': 4, 'B': 2, 'D': 1})
    node_d = Node('D', {'B': 5, 'C': 1})
    
    # Lista di nodi
    nodes = [node_a, node_b, node_c, node_d]
    
    return nodes

# Crea la rete
nodes = create_network()

# Avvia la simulazione del routing
distance_vector_routing(nodes)
