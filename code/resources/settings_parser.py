# parser

class Parser:

    def __init__(self, direct):
        # params
        self.direct = direct
        self.file = open(direct, 'r')
        self.dic = dict([])
        self.parse()

    def parse(self):
        for string in self.file:
            param, value = string.split(':')
            self.__setattr__(param, value)
            temp_dic = {param:value}
            self.dic.update(temp_dic)

    def fill(self):
        if self.dic:
            file = open(self.direct, 'w')
            for key in self.dic.keys():
                file.write(f'{key}:{self.dic[key]}')
        else:
            raise ZeroDivisionError('The dictionary is empty.')