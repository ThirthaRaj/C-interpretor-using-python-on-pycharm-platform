from hk import *
import  tkinter
keywords = set(["while", "endwhile", "if", "else", "endif", "printf","read", "==", "!=","<=",">=", "+", "-", "*", "/",">","<",'^', "="])
tokens = []
kw = set(['=', '<', '>', '!'])
'''def fun(inputstring):
    str=''
    print (inputstring.split())
    for i in inputstring.split():
        if i in keywords:
            if str:
                tokens.append(str)
                str=''
            tokens.append(i)
        else:
            for j in i:
                print (len(i))
                if j in keywords:
                    if str:
                        tokens.append(str)
                        str=''
                    tokens.append(j)
                else:
                    str=str+j
            if str:
                tokens.append(str)
                str=''

    if str:
        tokens.append(str)

    print (tokens)




    while 'printf' in tokens:
        tokens[tokens.index('printf')] = 'print'''


def fun2(inputstring):
    str=''
   # print (inputstring.split())
    for i in inputstring.split():
        if i in keywords:
            if str:
                tokens.append(str)
                str=''
            tokens.append(i)
        else:
            j=len(i)
            p=0
            while (p<j):
                if i[p] in kw and i[p + 1] == '=':
                    if str:
                        tokens.append(str)
                        str=''
                    tokens.append(i[p] + i[p + 1])
                    p += 1
                else:
                    if i[p] in keywords:
                        if str:
                            tokens.append(str)
                            str = ''
                        tokens.append(i[p])
                    else:
                        str += i[p]
                p += 1
            if str:
                tokens.append(str)
                str=''


    if str:
        tokens.append(str)

    '''#print (tokens)

    #while 'printf' in tokens:
     #  tokens[tokens.index('printf')] = 'print'''


def fun1(txt):
    global output
    tokens[:]=[]
    fun2(txt)
    txt1=parseFile(tokens)
    output[:]=[]
    print (txt1)

    try:
        execStatementList(txt1)
    except TypeError:
        print ("Error:")
        pass
    #print ("data in output")
    #print (output)
    #out=tkinter.Tk()
    #out.geometry("500x500+0+0")
    #frame=tkinter.Frame(out)
    #str1="\n".join(str(x) for x in output)
    #print (str1)
    #lab=tkinter.Label(frame,text=str1,fg="BLUE")
    #lab.pack()
    #frame.pack()
    #out.title("Output :-) :-) :-)")




