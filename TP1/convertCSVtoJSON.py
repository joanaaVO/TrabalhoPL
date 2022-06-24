from curses.ascii import isdigit
import re
import sys

headers = []
operations = []
intervals = []
defined_op = ["sum", "media", "min", "max"]

def head_reader(header):
    hs = re.findall(r'([^,\n]+{\d,*\d*}:*:*\w*)|([^,\n]+)',header)
    for h in hs:
        if (h[0]) == '': h = h[1]
        else: h = h[0]
        if re.search(r'{\d,*\d*}:*:*\w*',h):
            interval = re.findall(r'\d',h)
            
            #Error Handling dos intervalos
            if  (len(interval) == 1 and isdigit(interval[0])) or ( len(interval) == 2 and isdigit(interval[0]) and isdigit(interval[1]) and int(interval[0]) < int(interval[1]) ):
                intervals.append(interval)
            else:
                raise NameError("Intervalo invalido!\n")
            
            #Error Handling das virgulas
            interval = [int(num) for num in interval]
            maxInt = max(interval)
            new_s = h.replace("{","\{")
            new_s = new_s.replace("}","\}")
            er = r'(' + new_s + r',{' + str(maxInt-1) + r'}$)|(' + new_s + r',{' + str(maxInt) + r'}\w)'
            
            if not re.search(er, header):
                raise NameError("Cabecalho invalido!\n")

            if re.search(r'::\w+',h):    
                op = re.findall(r':\w+',h)[0][1:]
                
                #Error Handling das operacoes 
                if (str(op).lower() in defined_op):
                    operations.append(op)
                else: 
                    raise NameError("Operacao inexistente!\n") 
                
                two_headers = re.findall(r'[^{,}:\d]+',h)
                headers.append(two_headers[0] + "_" + two_headers[1])
                
            else:
                name = re.findall(r'\w+',h)[0]
                headers.append(name)
                operations.append("list")

        else:
            headers.append(h)
            operations.append("none")
            intervals.append(0)    

def read_line(line):
    i = 0
    l = re.split(',',line)
    res = []
    for j in range(0,len(headers)):
        elements = []
        if operations[j] != "none":
            if len(intervals[j]) == 1: #Listas com tamanho definido
                it = int(intervals[j][0])
                while it > 0:
                    
                    #Error handling das virgulas
                    if i >= len(l) or not re.search(r'\w', l[i]):
                        raise NameError("Numero de elementos invalido!\n")   
                    
                    elements.append(l[i])
                    i = i+1
                    it = it-1
            
                #Error handling das virgulas
                if i == len(l)-1 and not re.search(r'\n', l[i]):
                    raise NameError("Numero de elementos invalido!\n")

            else: #Listas com um intervalo de tamanhos
                it = int(intervals[j][1]) 

                while it > 0:
                    
                    #Error handling das virgulas
                    if i >= len(l):
                        raise NameError("Numero de elementos invalido!\n")      
                    
                    if re.search(r'\w', l[i]):
                        elements.append(l[i])

                    i = i+1
                    it = it-1

                #Error handling das virgulas
                if i == len(l)-1 and not re.search(r'\n', l[i]):
                    raise NameError("Numero de elementos invalido!\n")             
                
            if operations[j] != "list":  #Funcoes de agregacao
                
                #Error handling Funcoes de Agregacao
                for elem in elements:
                    for digit in elem:
                        if not isdigit(digit):
                            raise NameError("Impossivel aplicar funcao de agregacao!\n")

                elements = [int(num) for num in elements]
                if operations[j] == "sum": op_res = sum(elements)
                elif operations[j] == "media": op_res = sum(elements)/len(elements)
                elif operations[j] == "min": op_res = min(elements)
                elif operations[j] == "max": op_res = max(elements)
                res.append(str(op_res))

            else:   
                # List correction 
                if (len(elements) > 0):
                    is_number = False
                    is_word = False
                    
                    #Error handling da coerencia das listas
                    for elem in elements:
                        for digit in elem:
                            if not isdigit(digit):
                                is_word = True
                            else:
                                is_number = True

                    if is_number and is_word:
                      raise NameError("Incoerencia nos parametros da lista\n")   
                    if is_number:
                        elements = "[" + ','.join(map(str, elements)) + "]" 
                        res.append(elements)
                    else:
                        elements = "[" + "\"" + '\",\"'.join(elements) + "\"" + "]"
                        res.append(elements)
                else:
                    res.append("[]")
        else:
            res.append("\"" + l[i] + "\"")
            i = i+1
    return res 

def converter(lines):
    result = "[\n"
    i = 0
    for line in lines:
        result += "\t{\n"
        j = 0
        l = read_line(line)
        for h in headers:
            if (j == len(headers)-1):
                result += "\t\t"
                result += "\"" + h + "\": " + l[j] + "\n"
            else:
                result += "\t\t"
                result += "\"" + h + "\": " + l[j] + ",\n"
            j = j + 1
        if (i == len(lines)-1):
            result += "\t}\n"
        else:
            result += "\t},\n"
        i = i + 1
    result += "]\n"
    return result  

def main():
    if len(sys.argv) == 1: file = "teste.csv"
    elif len(sys.argv) > 2: 
        raise NameError("Argumentos a mais na funcao principal\n")
    else: file = sys.argv[1]

    f = open(file)
    lines = f.read().splitlines()
    f.close()
    head_reader(lines[0])
    result = converter(lines[1:])
    f = open(file[:-4] + ".json","w+")
    f.write(result)
    f.close()

main()