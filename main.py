from time import sleep

commands = ['out', '=', '+=', "-=", "+", "-", "*", "/", "END", "TRUE", "FALSE", "if", "endIF", "wait"]
directory = input('Enter the path of the viper(vpr) file:')
f = open("test.vpr")
cont = f.readlines()
isStdio = False
currentwrd = []
vardict = {}
isIf = False
ifCommands = []
isInp = False


def func(command, lineNo):
    if commands[11] in command:
        params = command.split("(")[1].split(")")[0].split(",")



def parse(lineNo):
    command = cont[lineNo]
    return command


def wait(command):
    if "wait" in command:
        time = command.split("(")[1].split(")")[0].split("\n")[0]
        sleep(int(time))


def inpt(command, lineNo):
    if "in" in command:
        if '"' in command:
            prompt = command.split("(")[1].split(")")[0].split("\n")[0]
            print(prompt)
        if not isInp:
            return
        input()


def ifStatement(command, lineNo):
    global isIf
    ifState = ""
    if commands[11] in command:
        condition = "".join(command.split("(")[1].split("):"))
        if '"' not in condition:
            con1 = 0
            con2 = 1
            try:
                if "==" in condition:
                    con1 = eval(condition.split("==")[0])
                    con2 = eval(str(condition.split("==")[1].split(")")[0]))
                    ifState = "equal"
                elif "!=" in condition:
                    con1 = eval(condition.split("!=")[0])
                    con2 = eval(str(condition.split("!=")[1].split(")")[0]))
                    ifState = "!equal"
                elif ">>" in condition:
                    con1 = eval(condition.split(">>")[0])
                    con2 = eval(str(condition.split(">>")[1].split(")")[0]))
                    ifState = "morethan"
                elif "<<" in condition:
                    con1 = eval(condition.split("<<")[0])
                    con2 = eval(str(condition.split("<<")[1].split(")")[0]))
                    ifState = "lessthan"
                else:
                    print("SYNTAX ERROR: Invalid Syntax")
                    return
            except SyntaxError:
                if str(condition.split(")")[0]) == "TRUE":
                    con1 = 1
                    con2 = 1
                elif (condition.split(")")[0]) == "FALSE":
                    con1 = 2
                    con2 = 1

            except NameError:
                if "==" in condition:
                    con1 = condition.split("==")[0]
                    con2 = str(condition.split("==")[1].split(")")[0])
                    ifState = "equal"
                if "!=" in condition:
                    con1 = condition.split("!=")[0]
                    con2 = str(condition.split("!=")[1].split(")")[0])
                    ifState = "!equal"
                if ">>" in condition:
                    con1 = condition.split(">>")[0]
                    con2 = str(condition.split(">>")[1].split(")")[0])
                    ifState = "morethan"
                if "<<" in condition:
                    con1 = condition.split("<<")[0]
                    con2 = str(condition.split("<<")[1].split(")")[0])
                    ifState = "lessthan"

                if con1 in vardict:
                    con1 = vardict[con1]
                    if con2 in vardict:
                        con2 = vardict[con2]
                    elif eval(con2):
                        con2 = eval(con2)
                    else:
                        print(F"ERROR IN LINE {lineNo + 1}: The second condition in the given if statement is not a "
                              F"variable, expression, number, string, or boolean. Please check if you have initialized "
                              F"the respective variable, or if you have misspelled anything")
            if con1 == con2 and ifState == "equal":
                if "{" in command:
                    isIf = True
            elif con1 != con2 and ifState == "!equal":
                if "{" in command:
                    isIf = True
            elif con1 > con2 and ifState == "morethan":
                if "{" in command:
                    isIf = True
            elif con1 < con2 and ifState == "lessthan":
                if "{" in command:
                    isIf = True
            else:
                return
        else:
            con1 = condition.split("==")[0]
            if len(con1.split('"')) <= 1:
                if con1 in vardict:
                    con1 = vardict[con1]
            con2 = str(condition.split("==")[1].split(")")[0])
            if len(con2.split('"')) <= 1:
                if con2 in vardict:
                    con2 = vardict[con2.split('"')[1]]
            if con1 == con2:
                if "{" in command:
                    isIf = True
            else:
                return
    else:
        isIf = False


def newVar(command, lineNo):
    if commands[1] in command:
        if "==" in command or "!=" in command or ">=" in command or "<=" in command:
            return
        varName = command.split("=")[0]
        varVal = command.split("=")[1]
        if '"' not in varVal:
            if varVal != "TRUE" or varVal != "FALSE":
                try:
                    if "in(" not in varVal:
                        vardict[varName.strip(" ")] = eval(varVal.strip("\n"))
                    else:
                        varVal += input()
                        varVal = varVal.split(")")[1]
                        isInt = False
                        if '"' not in varVal:
                            try:
                                varVal = eval(varVal)
                                isInt = True
                            except NameError:
                                print(f"ERROR IN LINE {lineNo + 1}: You seem to have given an invalid input. Check if "
                                      f"you have given a double quote at the start and end, or check if you have "
                                      f"written the equation correctly")
                        if not isInt:
                            vardict[varName.strip(" ")] = varVal.strip("\n")
                        else:
                            vardict[varName.strip(" ")] = int(varVal)
                        IsInp = True
                except NameError:
                    print(F"ERROR IN LINE {lineNo + 1}: You have made a variable, but it isn't a boolean, string, "
                          F"integer, float or expression. Please check if you have put double quotes for the string, "
                          F"and make sure that there are no spaces in the variable declaration")
            else:
                vardict[varName.strip(" ")] = varVal.strip("\n")

        else:
            if "in(" not in varVal:
                vardict[varName.strip(" ")] = varVal.strip("\n")
            else:
                pass


def out(command, lineNo):
    iswordprint = False
    if commands[0] in command:
        stringtoprint = ""

        for j in range(len(command)):
            if iswordprint:
                if command[j] == ")":
                    continue
                stringtoprint += command[j]
            if command[j] == "(":
                iswordprint = True
            elif command[j] == ")":
                iswordprint = False
        if '"' in stringtoprint:
            if "+" not in stringtoprint:
                print(stringtoprint)
            else:
                print("test")
                components = stringtoprint.split("+")
                print(components)
                for component in range(len(components)):
                    print(vardict)
                    print(components[component])
                    print(components[component] in vardict)
                    if '"' not in components[component]:
                        components[component] = components[component].split(" ")[-1]
                        print("name:", components[component])
                    if components[component] in vardict:
                        components[component] = vardict[components[component]]
                        print(components[component])
                stringtoprint = "".join(components)
                stringtoprint = stringtoprint.strip('" ').strip("+ ").strip(" +")
                stringtoprint = "".join(stringtoprint.split('"'))
                stringtoprint = '"' + stringtoprint + '"'
                print(stringtoprint)
        else:
            try:
                print(eval(stringtoprint))
            except NameError:
                if stringtoprint.strip("\n") in vardict:
                    print(vardict[stringtoprint.strip("\n")])
                else:
                    print(f"ERROR IN LINE {lineNo + 1}: Check if you have written a string, an integer, a float or an "
                          f"expression to print")


counter = 0
isSkip = False

for i in range(len(cont)):
    cmd = parse(i)
    ifStatement(cmd, i)
    if isIf:
        if "}" in cmd:
            isIf = False
            continue
        ifCommands.append(cmd.split("\n")[0])
        ifcmd = ifCommands[counter]
        counter += 1
        newVar(ifcmd, i)
        out(ifcmd, i)
        wait(ifcmd)
        continue
    else:
        if "{" in cmd:
            isSkip = True
        if "}" in cmd:
            isSkip = False

    if isSkip:
        continue

    newVar(cmd, i)
    out(cmd, i)
    wait(cmd)
    inpt(cmd, i)
