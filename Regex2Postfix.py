import re
#Check validated Formats
def validate_Regex(regex):
    try:
        re.compile(regex)
    except re.error:
        print(f"Invalid regular expression: {regex}")
        return False
    return True

def Shunting_Yard(regex):
    Higher_Operator_Importance = {
        "*": 5,
        "+": 4,
        "?": 3,
        ".": 2,
        "|": 1
    }
    
    postfix, stack = "", ""
    #Preprocessing 1
    square_brackets_count = regex.count('[')
    for idx in range(square_brackets_count):
        for i in range(len(regex)):
            chr_rgx = regex[i]
            if chr_rgx ==  '[':
                j = i + 1
                while regex[j] != ']':
                    if regex[j] == '(':
                        while regex[j] != ')':
                            j += 1
                    elif regex[j].isalnum() and regex[j + 1].isalnum():
                        regex = regex[:j + 1] + '|' + regex[j + 1:]
                    j += 1
    regex = regex.replace('[', '(')
    regex = regex.replace(']', ')')    
    
    #Preprocessing 2
    dashes_count = regex.count('-')
    for idx in range(dashes_count):
        for i in range(len(regex)):
            chr_rgx = regex[i]
            if chr_rgx == '-':
                first = regex[i - 1]
                final = regex[i + 1]
                in_between_list = ''
                for j in range(int(ord(final) - ord(first))): #Asci sequences [0-9A-Za-z]
                    in_between_list = in_between_list + '|'
                    char = chr(ord(first) + j + 1)
                    in_between_list = in_between_list + char
                regex = regex[0: i] + in_between_list + regex[i + 2:]
                
    #Preprocessing 3
    dot_indexes = []
    for i in range(len(regex) - 1):
        # startOps = [')', '*', '+', '*']
        # endOps = ["*", "+", ".", "|", ")"]
        opening_brackets = ['(', '[']
        operators = ['*', '+', '?', ')', ']']
        if regex[i] in operators and regex[i+1] not in operators:
            dot_indexes.append(i)
        elif regex[i].isalnum() and (regex[i+1].isalnum() or regex[i+1] in opening_brackets):
            dot_indexes.append(i)
    
    for i in range(len(dot_indexes)):
        index = dot_indexes[i] + 1 + i
        regex = regex[:index] + '.' + regex[index:]
        
    
    #Shunting_Yard Algorithms
    for i in range(len(regex)):
        chr_rgx = regex[i]
        if chr_rgx == '(' :
                stack += chr_rgx
                
        elif chr_rgx == ')':
            while stack!= '' and stack[-1]!= '(':
                postfix = postfix + stack[-1]
                stack = stack[:-1]
            stack = stack[:-1] # removes the open bracket in the stack
            
        elif chr_rgx in Higher_Operator_Importance:
            while stack!= '' and Higher_Operator_Importance.get(chr_rgx,0) <= Higher_Operator_Importance.get(stack[-1],0):
                postfix = postfix + stack[-1]
                stack = stack[:-1]
            stack += chr_rgx
            
        else:
            postfix = postfix + chr_rgx
            
    if stack!= '':
        postfix = postfix + stack[-1]
        stack = stack[:-1]
    return postfix
            