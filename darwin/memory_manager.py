import yaml
import os 

class MemoryManager:
    def __init__(self, filename='../memory.yaml'):
        self.filename = filename
        self.service = None
        self.encoding = 'utf8'
        self.allow_unicode = True

        if not os.path.exists(self.filename):
            with open(self.filename, 'w+', encoding=self.encoding) as file:
                self.service = yaml.safe_load(file)
                data = {
                    'име': None,
                    'локация': None,
                    'телефон': None,
                    'интереси': [],
                    'последно съобщение': None,
                    'последна локация': None,
                    'последно име': None
                }

                yaml.dump(data, file, allow_unicode=self.allow_unicode, sort_keys=False)
                print('Паметта е създадена')

    def get_property(self, name):
        with open(self.filename, 'r', encoding=self.encoding) as file:
            self.service = yaml.safe_load(file)
            if name not in self.service:
                return None
            
            return self.service[name]

        
    def set_property(self, name, value):
        with open(self.filename, 'r', encoding=self.encoding) as file:
            self.service = yaml.safe_load(file)

            if name not in self.service:
                return False
            
            if type(self.service[name]) == list:
                if value not in self.service[name]:
                    self.service[name].append(value)
            else:
                self.service[name] = value

            with open(self.filename, 'w', encoding=self.encoding) as file:
                yaml.dump(self.service, file, allow_unicode=self.allow_unicode, sort_keys=False)