#****************** Lexer ************************

tokenlist = []
#currtoken gives the current token referring to
currtoken = ("", "", 0)
#keywords in the code
keywords = set(["while", "endwhile", "if", "else", "endif", "printf", "read", "=", "==", "!=","<=",">=", "+", "-", "*", "/",">","<",'^'])
symboltable = dict()
output=[]
k=0

#this part of the code does lexical analysis of the first token in the tokenlist
def nextToken():
    global currtoken, symboltable
    if(len(tokenlist) > 0):
        s = tokenlist.pop(0)
        if s in keywords:
            currtoken = (s, "", 0)
        elif s.isdigit():
            currtoken = ("digit", "", int(s))
        elif s.isalnum():
            symboltable[s] = 0
            currtoken = ("label", s, 0)
        elif isinstance(s,str):
            symboltable[s] = s
            currtoken = ("string", "", s)
        else:
            print ("syntax error: " + s)
    else:
        currtoken = ("", "", 0)

def consume(expected):
    global k
    if currtoken[0] == expected:
        nextToken()
    else:
        k=1
        print ("expected " + expected + " not found")

#****************** Parser ************************

def parseFile(name):
    global tokenlist
    tokenlist=name
    nextToken()
    return doStatementList()

def doStatementList():
    global k
    stmts=[]
    newstmt=[]

    while currtoken[0] in ["while", "if", "printf", "label","read"]:
        if currtoken[0] == "while":
            # ["while", [condition], [statementlist]]
            consume("while")
            newstmt = ["while"]
            newstmt.append(doCondition())
            newstmt.append(doStatementList())
            consume("endwhile")
            if(k==1):
                k=0
                return stmts
            stmts.append(newstmt)
        elif currtoken[0] == "if":
            # ["if", [condition], [then part], [else part]]
            consume("if")
            newstmt = ["if"]
            newstmt.append(doCondition())
            newstmt.append(doStatementList())
            if currtoken[0] == "else":
                consume("else")
                newstmt.append(doStatementList())
            consume("endif")
            if(k==1):
                k=0
                return stmts
            stmts.append(newstmt)
        elif currtoken[0] == "printf":
            # ["print", [expression]]
            consume("printf")
            newstmt = ["print"]
            newstmt.append(doExpression())
            stmts.append(newstmt)
        elif currtoken[0] == "read":
            consume("read")
            newstmt = ["input"]
            newstmt.append(doExpression())
            stmts.append(newstmt)
        elif currtoken[0] == "label":
            # ["=", [expression], [expression]]
            label = [currtoken[1]]
            nextToken()
            consume("=")
            newstmt = ["="]
            if(k):
                k=0
                return stmts
            newstmt.append(label)
            newstmt.append(doExpression())
            stmts.append(newstmt)
        else:
            print ("invalid statement: " + currtoken[0])
            stmts.append(newstmt)
    return stmts


#checks weather the syntax is correct or not
def doCondition():
    exp = doExpression()
    # ["==|!=", [left side], [right side]]
    if currtoken[0] in ["==", "!=", '<=', '>=','<','>']:
        retval = [currtoken[0]]
        retval.append(exp)
        nextToken()
        retval.append(doExpression())
    else:
        print ("expected == or != not found")
    return retval

def doExpression():
    term = doTerm()
    # carry the term in case there's no +|-|/|*
    exp = term
    # ["+|-", [left side], [right side]]
    while currtoken[0] in ["+", "-","*","/",'^']:
        exp = [currtoken[0]]
        nextToken()
        exp.append(term)
        exp.append(doExpression())
    return exp

def doTerm():
    if currtoken[0] == "label":
        retval = currtoken[1]
        nextToken()
    elif currtoken[0] == "digit":
        retval = currtoken[2]
        nextToken()
    elif currtoken[0] == "string":
        retval = currtoken[2]
        nextToken()
    try:
        return [retval]
    except UnboundLocalError:
        pass



#*****************Interpreter**************
stack = []

def execStatementList(pgm):
    for stmt in pgm:
        execStatement(stmt)

def execStatement(stmt):
    if stmt[0] == "while":
        execCondition(stmt[1])
        while stack.pop():
            execStatementList(stmt[2])
            execCondition(stmt[1])
    elif stmt[0] == "if":
        execCondition(stmt[1])
        if stack.pop():
            execStatementList(stmt[2])
        elif len(stmt) == 4:
            execStatementList(stmt[3])
    elif stmt[0] == "=":
        execExpression(stmt[2])
        symboltable[stmt[1][0]] = stack.pop()
    elif stmt[0] == "input":
        print ("enter the value of "+stmt[1][0])
        p=input()
        symboltable[stmt[1][0]]=p

    elif stmt[0] == "print":
        execExpression(stmt[1])
        y=stack.pop()
        try:
            print (str(eval(y)))
            #output.append(str(eval(y)))
        except NameError:
            pass
    else:
        print ("invalid statement")

def execCondition(cond):
    execExpression(cond[1])
    execExpression(cond[2])
    x=eval(stack.pop())
    if cond[0] == "==":
        stack.append(eval(stack.pop()) == x)
    elif cond[0] == "!=":
        stack.append(eval(stack.pop()) != x)
    elif cond[0] == "<=":
        #print (type(stack.pop()))
        stack.append(eval(stack.pop()) <= x)
    elif cond[0] == ">=":
        stack.append((eval(stack.pop())) >= x)
    elif cond[0] == ">":
        stack.append(eval(stack.pop()) > x)
    elif cond[0] == "<":
        stack.append(eval(stack.pop()) < x)

def execExpression(exp):
        if len(exp) == 3:
            execExpression(exp[1])
            execExpression(exp[2])
            x=stack.pop()
            if exp[0] == "+":
                stack.append(str(stack.pop())+ '+'+str(x))
            else:
                if exp[0] == "-":
                    stack.append(str(stack.pop())+ '-'+str(x))
                else:
                    if exp[0] == "*":
                        stack.append(str(stack.pop())+ '*'+str(x))
                    else:
                        if exp[0] == "/":
                            stack.append(str(stack.pop())+ '/'+str(x))
                        else:
                            if exp[0] == "^":
                                 stack.append(str(stack.pop())+ '**'+str(x))
        else:
            if type(exp[0]) == int:
                stack.append(str(exp[0]))
            else:
                  stack.append(symboltable[exp[0]])


