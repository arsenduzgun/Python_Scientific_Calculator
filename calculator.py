from tkinter import *
from tkinter import messagebox
import math
import sympy

root = Tk()
root.title("Scientific Calculator")
root.resizable(False, False)
root.eval('tk::PlaceWindow . center')

btn_params = {
    'padx': 12,
    'pady': 1,
    'width': 3,
    'height': 3
}

top_frame = Frame(root, bg='#666666')
top_frame.pack(side=TOP)

bottom_frame = Frame(root, bd=2, bg='#666666')
bottom_frame.pack(side=BOTTOM)

output = Entry(top_frame, width=52, borderwidth=5, justify='right')
output.pack()
output.insert(0, "0")
output.config(state=DISABLED)

parenthesesDiff = 0
isDegree = True
errorInfo = ""
isAnswer = False
answer = 0

def constant(const):
    output.config(state=NORMAL)
    arg = output.get()
    output.delete(0, END)
    if arg[-1] in [' ', '(', '^', '-']: output.insert(0, arg + const)
    elif arg == '0': output.insert(0, const)
    else: output.insert(0, arg)
    output.config(state=DISABLED)

def floating():
    output.config(state=NORMAL)
    global isAnswer
    arg = output.get()
    output.delete(0, END)
    if arg[-1] in ['(', ')', ' ', 'π', 'e', '-', '^', 's', 'f', 'n'] or isAnswer: output.insert(0, arg)
    else:
        isFloating = False
        for letter in arg[::-1]:
            if letter == '.':
                isFloating = True
                break
            elif letter in [' ', '(']: break
        if isFloating: output.insert(0, arg)
        else: output.insert(0, arg + '.')
    output.config(state=DISABLED)

def number(num):
    output.config(state=NORMAL)
    global isAnswer
    arg = output.get()
    output.delete(0, END)
    if arg[-1] in ['π', 'e', ')', 's', 'f', 'n']: output.insert(0, arg)
    elif isAnswer:
        if arg == "0":
            output.insert(0, num)
            isAnswer = False
        else: output.insert(0, arg)
    else:
        if arg == "0": output.insert(0, num)
        else: output.insert(0, arg + num)
    output.config(state=DISABLED)

def deleteAll():
    output.config(state=NORMAL)
    global parenthesesDiff
    global isAnswer
    isAnswer = False
    output.delete(0, END)
    output.insert(0, "0")
    parenthesesDiff = 0
    output.config(state=DISABLED)

def delete():
    output.config(state=NORMAL)
    global parenthesesDiff
    global isAnswer
    arg = output.get()
    output.delete(0, END)
    if isAnswer:
        output.insert(0, "0")
        isAnswer = False
    elif arg[-1] == '(':
        parenthesesDiff -= 1
        if len(arg) == 1: output.insert(0, "0")
        elif arg[-2] not in [' ', '(']:
            lastOccurence = max(arg[:-1].rfind(' '), arg[:-1].rfind('('))
            if lastOccurence == -1: output.insert(0, "0")
            else: output.insert(0, arg[:lastOccurence + 1])
        else: output.insert(0, arg[:-1])
    elif arg[-1] == ')':
        parenthesesDiff += 1
        if len(arg) == 1: output.insert(0, "0")
        else: output.insert(0, arg[:-1])
    elif arg[-1] in [' ', 's']: output.insert(0, arg[:-3])
    else:
        if len(arg) == 1: output.insert(0, "0")
        else: output.insert(0, arg[:-1])
    output.config(state=DISABLED)

def switchSign():
    output.config(state=NORMAL)
    arg = output.get()
    output.delete(0, END)
    if arg == '0': output.insert(0, '-')
    elif arg == '-': output.insert(0, '0')
    elif arg[-1] in [' ', '^', '(']: output.insert(0, arg + '-')
    elif arg[-1] == '-': output.insert(0, arg[:-1])
    else: output.insert(0, arg)
    output.config(state=DISABLED)

def addSubMulDivMod(op):
    output.config(state=NORMAL)
    global isAnswer
    isAnswer = False
    arg = output.get()
    output.delete(0, END)
    if arg[-1] not in ['.', ' ', '(', '^', '-']: output.insert(0, arg + f' {op} ')
    else: output.insert(0, arg)
    output.config(state=DISABLED)

def parenthesis(prt):
    output.config(state=NORMAL)
    global parenthesesDiff
    arg = output.get()
    output.delete(0, END)
    if prt == '(':
        if arg[-1] in ['(', ' ', '^', '-']:
            output.insert(0, arg + '(')
            parenthesesDiff += 1
        elif arg == '0':
            output.insert(0, '(')
            parenthesesDiff += 1
        else: output.insert(0, arg)
    else:
        if arg[-1] not in ['.', ' ', '(', '-'] and parenthesesDiff > 0:
            output.insert(0, arg + ')')
            parenthesesDiff -= 1
        else: output.insert(0, arg)
    output.config(state=DISABLED)

def logLnFactAbsSinCosTanCotRnd(func):
    output.config(state=NORMAL)
    global parenthesesDiff
    arg = output.get()
    output.delete(0, END)
    if arg[-1] in ['(', ' ', '-', '^']:
        output.insert(0, arg + func)
        parenthesesDiff += 1
    elif arg == '0':
        output.insert(0, func)
        parenthesesDiff += 1
    else: output.insert(0, arg)
    output.config(state=DISABLED)

def exp():
    output.config(state=NORMAL)
    global isAnswer
    isAnswer = False
    arg = output.get()
    output.delete(0, END)
    if arg[-1] not in ['(', '.', '^', ' ', '-']: output.insert(0, arg + '^')
    else: output.insert(0, arg)
    output.config(state=DISABLED)

def degree():
    global isDegree
    isDegree = not isDegree
    buttonDegree.config(text='deg(on)' if isDegree else 'deg(off)')

def result():
    output.config(state=NORMAL)
    global isAnswer
    global parenthesesDiff
    global answer
    arg = output.get().replace("ans", f"({answer})")
    if parenthesesDiff != 0 or arg[-1] in ['.', ' ', '^', '-']:
        output.config(state=DISABLED)
        messagebox.showinfo("Error", "Input format is unreadable.")
        return
    try: res = solve(arg)
    except:
        output.config(state=DISABLED)
        messagebox.showinfo("Error", errorInfo)
    else:
        output.delete(0, END)
        if math.isinf(res) or math.isnan(res): output.insert(0, str(res))
        else:
            res = int(res) if int(res) == res else res
            output.insert(0, str(res))
        isAnswer = True
        answer = res
    output.config(state=DISABLED)

def solveInsidePrt(mainArg):
    global errorInfo
    while True:
        expIndex = mainArg.rfind('^')
        if expIndex == -1: break
        leftIndex = max(mainArg[:expIndex].rfind('^'), mainArg[:expIndex].rfind(' '))
        rightIndex = mainArg[expIndex:].find(' ')
        arg = mainArg[leftIndex + 1:rightIndex + expIndex] if rightIndex != -1 else mainArg[leftIndex + 1:]
        leftArg, rightArg = arg.split('^')
        leftArg = math.e if leftArg == 'e' else -math.e if leftArg == '-e' else math.pi if leftArg == 'π' else -math.pi if leftArg == '-π' else float(leftArg)
        rightArg = math.e if rightArg == 'e' else -math.e if rightArg == '-e' else math.pi if rightArg == 'π' else -math.pi if rightArg == '-π' else float(rightArg)
        if math.isinf(rightArg):
            if leftArg == 0:
                errorInfo = f"0^inf is undefined."
                raise Exception()
            elif abs(leftArg) == 1:
                errorInfo = f"1^inf is undefined."
                raise Exception()
            elif -1 < leftArg < 1: result = 0
            elif leftArg > 1: result = math.inf
            else: result = -math.inf
        else:
            if leftArg < 0: result = -float(sympy.real_root(-leftArg, 1 / rightArg if rightArg != 0 else 0))
            else:
                result = sympy.real_root(leftArg, 1 / rightArg if rightArg != 0 else 0)
                if result.is_real: result = float(result)
                elif not math.isnan(result):
                    errorInfo = f"0^{int(rightArg) if int(rightArg) == rightArg else rightArg} is undefined."
                    raise Exception()
        mainArg = str(result).join(mainArg.rsplit(arg, 1))
    while True:
        operatorIndexes = [val for val in [mainArg.find('×'), mainArg.find('÷'), mainArg.find('%')] if val != -1]
        if len(operatorIndexes) == 0: break
        smallestOpIndex = min(operatorIndexes)
        leftIndex = mainArg[:smallestOpIndex - 1].rfind(' ')
        rightIndex = mainArg[smallestOpIndex + 2:].find(' ')
        arg = mainArg[leftIndex + 1:rightIndex + smallestOpIndex + 2] if rightIndex != -1 else mainArg[leftIndex + 1:]
        leftArg, middleArg, rightArg = arg.split(' ')
        leftArg = math.e if leftArg == 'e' else -math.e if leftArg == '-e' else math.pi if leftArg == 'π' else -math.pi if leftArg == '-π' else float(leftArg)
        rightArg = math.e if rightArg == 'e' else -math.e if rightArg == '-e' else math.pi if rightArg == 'π' else -math.pi if rightArg == '-π' else float(rightArg)
        if middleArg == '×': result = leftArg * rightArg
        elif middleArg == '÷':
            if rightArg != 0: result = leftArg / rightArg
            else:
                errorInfo = f"{int(leftArg) if int(leftArg) == leftArg else leftArg} ÷ 0 is undefined."
                raise Exception()
        else:
            if rightArg != 0:
                rightArgStr = str(rightArg)
                if rightArgStr[-2:] != '.0':
                    afterPointLength = len(rightArgStr[rightArgStr.find('.') + 1:])
                    result = ((leftArg * pow(10, afterPointLength)) % (rightArg * pow(10, afterPointLength))) / pow(10, afterPointLength)
                else: result = leftArg % rightArg
            else:
                errorInfo = f"{int(leftArg) if int(leftArg) == leftArg else leftArg} % 0 is undefined."
                raise Exception()
        mainArg = str(result).join(mainArg.rsplit(arg, 1))
    mainArg = mainArg.replace('e-', 'tmp-').replace('e+', 'tmp+').replace('e', str(math.e)).replace('tmp-', 'e-').replace('tmp+', 'e+').replace('π', str(math.pi))
    mainArgSplitted = mainArg.split(' ')
    result = float(mainArgSplitted[0])
    for operatorIndex in range(1, len(mainArgSplitted), 2):
        if mainArgSplitted[operatorIndex] == '+': result += float(mainArgSplitted[operatorIndex + 1])
        else: result -= float(mainArgSplitted[operatorIndex + 1])
    return result

def solveFunc(arg, leftPrtIndex, rightPrtIndex, result):
    global errorInfo
    global isDegree
    method = arg[leftPrtIndex - 2: leftPrtIndex]
    if method == 'in':
        methodName = 'sin'
        if isDegree: newResult = round(math.sin(math.radians(result)), 10)
        else: newResult = round(math.sin(result), 10)
    elif method == 'os':
        methodName = 'cos'
        if isDegree: newResult = round(math.cos(math.radians(result)), 10)
        else: newResult = round(math.cos(result), 10)
    elif method == 'an':
        methodName = 'tan'
        if isDegree:
            if result % 180 == 0: newResult = 0
            elif result % 90 == 0:
                errorInfo = f"tan({int(result)}°) is undefined."
                raise Exception()
            else: newResult = math.tan(math.radians(result))
        else:
            if (result / (math.pi / 2)) % 2 == 1:
                coef = int(result / (math.pi / 2))
                if coef == 1: errorInfo = f"tan(π/2) is undefined."
                elif coef == -1: errorInfo = f"tan(-π/2) is undefined."
                else: errorInfo = f"tan({coef}π/2) is undefined."
                raise Exception()
            elif result % math.pi == 0: newResult = 0
            else: newResult = math.tan(result)
    elif method == 'ot':
        methodName = 'cot'
        if isDegree:
            if result % 180 == 0:
                errorInfo = f"cot({int(result)}°) is undefined."
                raise Exception()
            elif result % 90 == 0: newResult = 0
            else: newResult = 1 / math.tan(math.radians(result))
        else:
            if (result / (math.pi / 2)) % 2 == 1: newResult = 0
            elif result % math.pi == 0:
                coef = int(result / math.pi)
                if coef == 1: errorInfo = f"cot(π) is undefined."
                elif coef == 0: errorInfo = f"cot(0) is undefined."
                elif coef == -1: errorInfo = f"cot(-π) is undefined."
                else: errorInfo = f"cot({coef}π) is undefined."
                raise Exception()
            else: newResult = 1 / math.tan(result)
    elif method == 'og':
        methodName = 'log'
        if result <= 0:
            errorInfo = f"log({int(result) if int(result) == result else result}) is undefined."
            raise Exception()
        newResult = math.log(result, 10)
    elif method == 'ln':
        methodName = 'ln'
        if result <= 0:
            errorInfo = f"ln({int(result) if int(result) == result else result}) is undefined."
            raise Exception()
        newResult = math.log(result, math.e)
    elif method == 'bs':
        methodName = 'abs'
        newResult = abs(result)
    elif method == 'ct':
        methodName = 'fact'
        if int(result) == result and result >= 0: newResult = math.factorial(int(result))
        else:
            errorInfo = f"fact({int(result) if int(result) == result else result}) is undefined."
            raise Exception()
    else:
        methodName = 'rnd'
        newResult = round(result)
    return "".join(arg[:leftPrtIndex + 1].rsplit(methodName, 1)) + str(newResult) + arg[rightPrtIndex:]

def solveExp(arg, leftPrtIndex, insidePrt, result):
    global errorInfo
    if leftPrtIndex != 0 and arg[leftPrtIndex - 1] == '-':
        middleRightArg = str(result).join(arg[leftPrtIndex - 1:].split(insidePrt, 1))
        leftArg = arg[:leftPrtIndex - 1]
    else:
        middleRightArg = str(result).join(arg[leftPrtIndex:].split(insidePrt, 1))
        leftArg = arg[:leftPrtIndex]
    prtDiff = 0
    cutIndex = -1
    splitIndex = []
    for charIndex in range(0, len(middleRightArg)):
        char = middleRightArg[charIndex]
        if char == '(': prtDiff += 1
        elif char == ')':
            if prtDiff == 0:
                cutIndex = charIndex
                break
            else: prtDiff -= 1
        elif char == ' ' and prtDiff == 0:
            cutIndex = charIndex
            break
        elif char == '^' and prtDiff == 0: splitIndex.append(charIndex)
    middleArg = middleRightArg
    if cutIndex != -1:
        middleArg = middleRightArg[:cutIndex]
        rightArg = middleRightArg[cutIndex:]
    else: rightArg = ""
    splittedArg = [middleArg[i + 1:j] for i, j in zip([0] + splitIndex, splitIndex + [None])]
    splittedArg[0] = ('(' if middleArg[0] == '(' else '-') + splittedArg[0]
    while True:
        if len(splittedArg) == 1: break
        else:
            isSecondLastArgPrt = isSecondLastArgNeg = False
            if splittedArg[-2][-1] == ')':
                isSecondLastArgPrt = True
                if splittedArg[-2][0] == '-':
                    isSecondLastArgNeg = True
                    splittedArg[-2] = splittedArg[-2][2:-1]
                else: splittedArg[-2] = splittedArg[-2][1:-1]
            secondLastArgResult, lastArgResult = solve(splittedArg[-2]), solve(splittedArg[-1])
            if math.isinf(lastArgResult):
                if secondLastArgResult == 0:
                    errorInfo = f"0^inf is undefined."
                    raise Exception()
                elif abs(secondLastArgResult) == 1:
                    if secondLastArgResult == -1 and isSecondLastArgPrt: errorInfo = f"(-1)^inf is undefined."
                    else: errorInfo = f"1^inf is undefined."
                    raise Exception()
                elif -1 < secondLastArgResult < 1: result = 0
                elif secondLastArgResult > 1:
                    if isSecondLastArgNeg: result = -math.inf
                    else: result = math.inf
                else:
                    if isSecondLastArgPrt and isSecondLastArgNeg: result = math.inf
                    else: result = -math.inf
            elif isSecondLastArgPrt:
                if isSecondLastArgNeg:
                    result = sympy.real_root(secondLastArgResult, 1 / lastArgResult if lastArgResult != 0 else 0)
                    if result.is_real: result = -float(result)
                    elif not math.isnan(result):
                        secondLastArgDisplay = int(secondLastArgResult) if int(secondLastArgResult) == secondLastArgResult else secondLastArgResult
                        lastArgDisplay = int(lastArgResult) if int(lastArgResult) == lastArgResult else lastArgResult
                        if secondLastArgResult == 0: errorInfo = f"0^{lastArgDisplay} is undefined."
                        else: errorInfo = f"({secondLastArgDisplay})^{lastArgDisplay} is undefined."
                        raise Exception()
                else:
                    result = sympy.real_root(secondLastArgResult, 1 / lastArgResult if lastArgResult != 0 else 0)
                    if result.is_real: result = float(result)
                    elif not math.isnan(result):
                        secondLastArgDisplay = int(secondLastArgResult) if int(secondLastArgResult) == secondLastArgResult else secondLastArgResult
                        lastArgDisplay = int(lastArgResult) if int(lastArgResult) == lastArgResult else lastArgResult
                        if secondLastArgResult == 0: errorInfo = f"0^{lastArgDisplay} is undefined."
                        else: errorInfo = f"({secondLastArgDisplay})^{lastArgDisplay} is undefined."
                        raise Exception()
            else:
                if secondLastArgResult < 0: result = -float(sympy.real_root(-secondLastArgResult, 1 / lastArgResult if lastArgResult != 0 else 0))
                else:
                    result = sympy.real_root(secondLastArgResult, 1 / lastArgResult if lastArgResult != 0 else 0)
                    if result.is_real: result = float(result)
                    elif not math.isnan(result):
                        errorInfo = f"0^{int(lastArgResult) if int(lastArgResult) == lastArgResult else lastArgResult} is undefined."
                        raise Exception()
            splittedArg = splittedArg[:-2] + [str(result)]
    return leftArg + splittedArg[0] + rightArg

def removePrt(arg, leftPrtIndex, rightPrtIndex, result):
    if leftPrtIndex != 0 and arg[leftPrtIndex - 1] == '-' and result < 0:
        return arg[:leftPrtIndex - 1] + str(abs(result)) + arg[rightPrtIndex + 1:]
    else: return arg[:leftPrtIndex] + str(result) + arg[rightPrtIndex + 1:]

def solve(arg):
    while True:
        rightPrtIndex = arg.find(')')
        if rightPrtIndex == -1: break
        leftPrtIndex = arg[:rightPrtIndex].rfind('(')
        insidePrt = arg[leftPrtIndex + 1:rightPrtIndex]
        result = solveInsidePrt(insidePrt)
        if leftPrtIndex != 0 and arg[leftPrtIndex - 1] not in ['(', ' ', '-', '^']:
            arg = solveFunc(arg, leftPrtIndex, rightPrtIndex, result)
        elif rightPrtIndex + 1 != len(arg) and arg[rightPrtIndex + 1] == '^':
            arg = solveExp(arg, leftPrtIndex, insidePrt, result)
        else: arg = removePrt(arg, leftPrtIndex, rightPrtIndex, result)
    print(solveInsidePrt(arg))
    return solveInsidePrt(arg)

buttonLeftParenthesis = Button(bottom_frame, btn_params, text="(", command=lambda: parenthesis("("))
buttonLeftParenthesis.grid(row=0, column=0)

buttonRightParenthesis = Button(bottom_frame, btn_params, text=")", command=lambda: parenthesis(")"))
buttonRightParenthesis.grid(row=0, column=1)

buttonPi = Button(bottom_frame, btn_params, text='π', command=lambda: constant("π"))
buttonPi.grid(row=0, column=2)

buttonE = Button(bottom_frame, btn_params, text='e', command=lambda: constant("e"))
buttonE.grid(row=0, column=3)

buttonC = Button(bottom_frame, btn_params, text='C', command=lambda: deleteAll())
buttonC.grid(row=0, column=4)

buttonDel = Button(bottom_frame, btn_params, text='del', command=lambda: delete())
buttonDel.grid(row=0, column=5)

buttonDegree = Button(bottom_frame, btn_params, text='deg(on)', command=lambda: degree())
buttonDegree.grid(row=1, column=0)

buttonRnd = Button(bottom_frame, btn_params, text='rnd', command=lambda: logLnFactAbsSinCosTanCotRnd("rnd("))
buttonRnd.grid(row=1, column=1)

buttonFactorial = Button(bottom_frame, btn_params, text='x!', command=lambda: logLnFactAbsSinCosTanCotRnd("fact("))
buttonFactorial.grid(row=1, column=2)

buttonExponential = Button(bottom_frame, btn_params, text='x^y', command=lambda: exp())
buttonExponential.grid(row=1, column=3)

buttonSwitchSign = Button(bottom_frame, btn_params, text='+/-', command=lambda: switchSign())
buttonSwitchSign.grid(row=1, column=4)

buttonAns = Button(bottom_frame, btn_params, text='ans', command=lambda: constant("ans"))
buttonAns.grid(row=1, column=5)

buttonSin = Button(bottom_frame, btn_params, text='sin', command=lambda: logLnFactAbsSinCosTanCotRnd("sin("))
buttonSin.grid(row=2, column=0)

buttonLog = Button(bottom_frame, btn_params, text='log', command=lambda: logLnFactAbsSinCosTanCotRnd("log("))
buttonLog.grid(row=2, column=1)

button7 = Button(bottom_frame, btn_params, text='7', command=lambda: number("7"))
button7.grid(row=2, column=2)

button8 = Button(bottom_frame, btn_params, text='8', command=lambda: number("8"))
button8.grid(row=2, column=3)

button9 = Button(bottom_frame, btn_params, text='9', command=lambda: number("9"))
button9.grid(row=2, column=4)

buttonDivide = Button(bottom_frame, btn_params, text='÷', command=lambda: addSubMulDivMod("÷"))
buttonDivide.grid(row=2, column=5)

buttonCos = Button(bottom_frame, btn_params, text='cos', command=lambda: logLnFactAbsSinCosTanCotRnd("cos("))
buttonCos.grid(row=3, column=0)

buttonLn = Button(bottom_frame, btn_params, text='ln', command=lambda: logLnFactAbsSinCosTanCotRnd("ln("))
buttonLn.grid(row=3, column=1)

button4 = Button(bottom_frame, btn_params, text='4', command=lambda: number("4"))
button4.grid(row=3, column=2)

button5 = Button(bottom_frame, btn_params, text='5', command=lambda: number("5"))
button5.grid(row=3, column=3)

button6 = Button(bottom_frame, btn_params, text='6', command=lambda: number("6"))
button6.grid(row=3, column=4)

buttonMultiply = Button(bottom_frame, btn_params, text='×', command=lambda: addSubMulDivMod("×"))
buttonMultiply.grid(row=3, column=5)

buttonTan = Button(bottom_frame, btn_params, text='tan', command=lambda: logLnFactAbsSinCosTanCotRnd("tan("))
buttonTan.grid(row=4, column=0)

buttonMod = Button(bottom_frame, btn_params, text='%', command=lambda: addSubMulDivMod("%"))
buttonMod.grid(row=4, column=1)

button1 = Button(bottom_frame, btn_params, text='1', command=lambda: number("1"))
button1.grid(row=4, column=2)

button2 = Button(bottom_frame, btn_params, text='2', command=lambda: number("2"))
button2.grid(row=4, column=3)

button3 = Button(bottom_frame, btn_params, text='3', command=lambda: number("3"))
button3.grid(row=4, column=4)

buttonSubtract = Button(bottom_frame, btn_params, text='-', command=lambda: addSubMulDivMod('-'))
buttonSubtract.grid(row=4, column=5)

buttonCot = Button(bottom_frame, btn_params, text='cot', command=lambda: logLnFactAbsSinCosTanCotRnd("cot("))
buttonCot.grid(row=5, column=0)

buttonAbs = Button(bottom_frame, btn_params, text='|x|', command=lambda: logLnFactAbsSinCosTanCotRnd("abs("))
buttonAbs.grid(row=5, column=1)

button0 = Button(bottom_frame, btn_params, text='0', command=lambda: number("0"))
button0.grid(row=5, column=2)

buttonPoint = Button(bottom_frame, btn_params, text='.', command=lambda: floating())
buttonPoint.grid(row=5, column=3)

buttonEquals = Button(bottom_frame, btn_params, text='=', command=lambda: result())
buttonEquals.grid(row=5, column=4)

buttonAdd = Button(bottom_frame, btn_params, text='+', command=lambda: addSubMulDivMod('+'))
buttonAdd.grid(row=5, column=5)

root.mainloop()