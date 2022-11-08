class Logger:
    def __init__(self):
        self._log_collection = dict()
    
    def reset(self):
        self._log_collection.clear()
    
    def log(self, name, amount_to_add: int):
        self.__create_new_entry_if_not_exist(name)
        
        self._log_collection[name]+= amount_to_add

    def __create_new_entry_if_not_exist(self, name):
        if name not in self._log_collection:
            self._log_collection[name] = 0
    
    def get_logs(self):
        return self._log_collection
        

        
