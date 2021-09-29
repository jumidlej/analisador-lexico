class tag:
    number = 'num'
    identifier = 'id'
    operator = 'op'
    true = 'true'
    false = 'false'

class token:
    def __init__(self, tag):
        self.tag = tag

# number extends token
class number(token):
    def __init__(self, tag, value):
        super().__init__(tag)
        self.value = value

# identifier extends token
class identifier(token):
    def __init__(self, tag, name):
        super().__init__(tag)
        self.name = name

class operator(token):
    def __init__(self, tag, symbol):
        super().__init__(tag)
        self.symbol = symbol

class lexer:
    def __init__(self):
        self.tags = tag() 
        
        # por que não podem ser listas?
        # hash identifiers
        self.identifiers_hash = {}
        # hash operators
        self.operators_hash = {}
        # hash reserved words
        self.reserved_hash = {}

        self.reserved_hash['True'] = identifier(self.tags.true, 'True')
        self.reserved_hash['False'] = identifier(self.tags.true, 'False')
        self.operators_hash['0'] = operator(self.tags.operator, '+')
        self.operators_hash['1'] = operator(self.tags.operator, '-')
        self.operators_hash['2'] = operator(self.tags.operator, '*')
        self.operators_hash['3'] = operator(self.tags.operator, '/')
        
    def isletter(self, character):
        if ord(character) >= 65 and ord(character) <= 90:
            return True
        if ord(character) >= 97 and ord(character) <= 122:
            return True
        return False
    
    def scan(self, input_file_name, output_file_name):
        self.line = 0
        self.input_file = open(input_file_name, 'r')
        self.output_file = open(output_file_name, 'w')
        peeks_list = list(self.input_file.readlines())
        peeks_list = ''.join(peeks_list)
        peeks_list = list(peeks_list)

        # print(peeks_list)
        while (len(peeks_list) > 0):
            while (True):
                if len(peeks_list) > 0:
                    self.peek = peeks_list.pop(0)
                else:
                    break
                if self.peek == ' ' or self.peek == '\t':
                    continue
                elif self.peek == '\n':
                    self.output_file.write("\n")
                    self.line += 1
                    continue
                else:
                    break
            
            if (self.peek.isdigit()):
                v = 0
                while (True):
                    v = 10*v+ord(self.peek)-48
                    if len(peeks_list) > 0:
                        self.peek = peeks_list.pop(0)
                    else:
                        break
                    if not self.peek.isdigit():
                        self.output_file.write("<"+str(self.tags.number)+","+str(v)+"> ")
                        break
                    # em vez de retornar escrever no arquivo

            elif (self.isletter(self.peek)):
                buffer = []
                while (True):
                    buffer.append(self.peek)
                    if len(peeks_list) > 0:
                        self.peek = peeks_list.pop(0)
                    else:
                        break
                    if not (self.peek.isdigit() or self.isletter(self.peek)):
                        break

                # list to string
                buffer = ''.join(buffer)

                # procurar se tem na hash de identificadores se não tiver adicionar
                # ACHAR UM JEITO MELHOR DE FAZER ISSO
                is_new = True
                for obj in self.identifiers_hash.values():
                    if buffer == obj.name:
                        is_new = False
                        break

                if is_new:
                    # print(buffer)
                    self.identifiers_hash[buffer] = identifier(self.tags.identifier, buffer)
                    
                # escrever no arquivo
                self.output_file.write("<"+str(self.tags.identifier)+","+buffer+"> ")

            else:
                for obj in self.operators_hash.values():
                    if self.peek == obj.symbol:
                        # escrever no arquivo
                        self.output_file.write("<"+str(self.tags.operator)+","+self.peek+"> ")
                        break

            

            if self.peek == '\n':
                self.output_file.write("\n")
                self.line += 1

            # se não achou um op, nem id, nem digito, não devia retornar erro?

            # resolver os tokens genéricos (???)

input_file = 'input.txt'
output_file = 'output.txt'

l = lexer()
l.scan(input_file, output_file)
        






