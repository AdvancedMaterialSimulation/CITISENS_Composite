
class Card:
    def __init__(self, name, content):
        self.name = name.strip('\n')
        self.content = content
        # doesn't matter upper or lower case
        self.name_up = self.name.upper()
        self.type = "None"
        self.options = name.strip('\n').split(',')[1:]
        # optinos split '='
        self.options = [i.split('=') for i in self.options]
        # to dict
        self.options = {i[0].strip():i[1].strip() for i in self.options}
    def __str__(self):
        return f'Card ({self.type}): {self.name}'
    
    def __repr__(self):
        return f'Card ({self.type}) :{self.name}'
    
    def print(self):
        return self.name + self.content[0]
# =============================================================================
