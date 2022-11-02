class Logger:
    def __init__(self):
        self.enabled = False
        self.log_collection = dict()
    
    def set_enabled(self, val):
        self.enabled = val

    def is_enabled(self):
        return self.enabled
    
    def reset(self):
        self.log_collection.clear()
    
    def log(self, name, amount_to_add: int):
        self.__create_new_entry_if_not_exist(name)
        
        self.log_collection[name]+= amount_to_add

    def __create_new_entry_if_not_exist(self, name):
        if name not in self.log_collection:
            self.log_collection[name] = 0
    
    def get_logs(self):
        return self.log_collection
        

        
