
class Plan:
    def __init__(self):
        self.edge_order = []
        self.edges = {}
    
    def get_edge(self, index):
        name = self.get_edge_name(index)
        
        return self.get_edge_data(name)
    
    def get_edge_name(self, index):
        return self.edge_order[index]
    
    def get_edge_data(self, name):
        return self.edges[name]
    
    def get_size(self):
        return len(self.edge_order)