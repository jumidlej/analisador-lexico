# passar pra números a partir de 256 depois
class tag:
    number = 'num'
    identifier = 'id'
    true = 'true'
    false = 'false'
    addition = '+'
    subtraction = '-'
    multiplication = '*'
    division = '/'
    logarithm = 'log'
    square = 'sqrt'
    assignment = '='
    equality = '=='
    bigger_than = '>'
    less_than = '<'
    bigger_or_equal = '>='
    less_or_equal = '<=' 
    logical_or = 'or'
    logical_and = 'and'
    logical_not = 'not'
    open_parentesis = '('
    close_parentesis = ')'

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

class lexer:
    def __init__(self):
        self.tags = tag() 
        
        # hash identifiers
        self.identifiers_hash = {}
        # hash operators
        self.operators_hash = {}
        # hash reserved words
        self.reserved_hash = {}

        # log e sqrt são operadores?
        self.reserved_hash['true'] = token(self.tags.true)
        self.reserved_hash['false'] = token(self.tags.false)
        self.reserved_hash['or'] = token(self.tags.logical_or)
        self.reserved_hash['and'] = token(self.tags.logical_and)
        self.reserved_hash['not'] = token(self.tags.logical_not)
        self.reserved_hash['log'] = token(self.tags.logarithm)
        self.reserved_hash['sqrt'] = token(self.tags.square)
        self.operators_hash['='] = token(self.tags.assignment)
        self.operators_hash['+'] = token(self.tags.addition)
        self.operators_hash['-'] = token(self.tags.subtraction)
        self.operators_hash['*'] = token(self.tags.multiplication)
        self.operators_hash['/'] = token(self.tags.division)
        self.operators_hash['=='] = token(self.tags.equality)
        self.operators_hash['>'] = token(self.tags.bigger_than)
        self.operators_hash['<'] = token(self.tags.less_than)
        self.operators_hash['>='] = token(self.tags.bigger_or_equal)
        self.operators_hash['<='] = token(self.tags.less_or_equal)
        self.operators_hash['('] = token(self.tags.open_parentesis)
        self.operators_hash[')'] = token(self.tags.close_parentesis)
        
    # função para saber se um char é uma letra [a-zA-Z]
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
        self.peek = ' '
        end = False
        while not end:
            # procura char que não seja espaço, tabulação ou quebra de linha
            while True:
                if self.peek == ' ' or self.peek == '\t':
                    if len(peeks_list) > 0:
                        self.peek = peeks_list.pop(0)
                    else:
                        return
                        break
                    continue
                elif self.peek == '\n':
                    self.output_file.write("\n")
                    self.line += 1
                    if len(peeks_list) > 0:
                        self.peek = peeks_list.pop(0)
                    else:
                        return
                        break
                    continue
                else:
                    break
            
            # number tag
            if self.peek.isdigit():
                v = 0
                decimal = False
                div = 1
                while (True):
                    if self.peek != '.':
                        v = 10*v+ord(self.peek)-48
                        if decimal:
                            div *= 10
                    else:
                        if not decimal:
                            decimal = True
                        else:
                            self.output_file.write("<"+str(self.tags.number)+","+str(v/div)+"> ")
                            break
                    if len(peeks_list) > 0:
                        self.peek = peeks_list.pop(0)
                    else:
                        end = True
                        break
                    if not (self.peek.isdigit() or self.peek == '.'):
                        break
                
                self.output_file.write("<"+str(self.tags.number)+","+str(v/div)+"> ")

            # identifier, true, false, log, and, or, not, sqrt tags
            elif self.isletter(self.peek):
                buffer = ''
                while (True):
                    buffer += self.peek
                    if len(peeks_list) > 0:
                        self.peek = peeks_list.pop(0)
                    else:
                        end = True
                        break
                    if not (self.peek.isdigit() or self.isletter(self.peek)):
                        break

                # procurar se tem na hash de palavras reservadas
                if buffer in self.reserved_hash:
                    self.output_file.write("<"+self.reserved_hash[buffer].tag+"> ")

                # procurar se tem na hash de identificadores se não tiver adicionar
                elif buffer in self.identifiers_hash:
                    self.output_file.write("<"+str(self.tags.identifier)+","+buffer+"> ")
                else:
                    self.identifiers_hash[buffer] = identifier(self.tags.identifier, buffer)
                    self.output_file.write("<"+str(self.tags.identifier)+","+buffer+"> ")

            # operadores tags
            elif self.peek in self.operators_hash:
                buffer = self.peek
                if len(peeks_list) > 0:
                    self.peek = peeks_list.pop(0)
                    if buffer in ['=', '>', '<'] and self.peek == '=':
                        buffer += self.peek
                        if len(peeks_list) > 0:
                            self.peek = peeks_list.pop(0)
                        else:
                            end = True
                else:
                    end = True
                self.output_file.write("<"+self.operators_hash[buffer].tag+"> ")

            # tratar tokens genéricos
            else:
                self.output_file.write("<"+self.peek+"> ")
                if len(peeks_list) > 0:
                    self.peek = peeks_list.pop(0)
                else:
                    end = True

input_file = 'input.txt'
output_file = 'output.txt'

l = lexer()
l.scan(input_file, output_file)
        