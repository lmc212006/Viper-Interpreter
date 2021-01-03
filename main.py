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


def parse(lineNo):
    command = cont[lineNo]
    return command


def wait(command):
    if "wait" in command:
        time = command.split("(")[1].split(")")[0].split("\n")[0]
        sleep(int(time))


def ifStatement(command, lineNo):
    global isIf
    if commands[11] in command:
        condition = "".join(command.split("(")[1].split("):"))
        if '"' not in condition:
            con1 = 0
            con2 = 1
            try:
                con1 = eval(condition.split("==")[0])
                con2 = eval(str(condition.split("==")[1].split(")")[0]))
            except SyntaxError:
                if str(condition.split(")")[0]) == "TRUE":
                    con1 = 1
                    con2 = 1
                elif (condition.split(")")[0]) == "FALSE":
                    con1 = 2
                    con2 = 1

            except NameError:
                con1 = condition.split("==")[0]
                con2 = str(condition.split("==")[1].split(")")[0])
                if con1 in vardict:
                    con1 = vardict[con1]
                    if con2 in vardict:
                        con2 = vardict[con2]
                    else:
                        print(F"ERROR IN LINE {lineNo + 1}: The second condition in the given if statement is not a "
                              F"variable, expression, number, string, or boolean. Please check if you have initialized "
                              F"the respective variable, or if you have misspelled anything")


            if con1 == con2:
                if "{" in command:
                    isIf = True
            else:
                return
        else:
            con1 = condition.split("==")[0]
            con2 = str(condition.split("==")[1].split(")")[0])
            if con1 == con2:
                if "{" in command:
                    isIf = True
            else:
                return


def newVar(command, lineNo):
    if commands[1] in command:
        if "==" in command:
            return
        varName = command.split("=")[0]
        varVal = command.split("=")[1]
        if '"' not in varVal:
            if varVal != "TRUE" or varVal != "FALSE":
                try:
                    vardict[varName] = eval(varVal.strip("\n"))
                except NameError:
                    print(F"ERROR IN LINE {lineNo + 1}: You have made a variable, but it isn't a boolean, string, "
                          F"integer, float or expression. Please check if you have put double quotes for the string, "
                          F"and make sure that there are no spaces in the variable declaration")
            else:
                vardict[varName] = varVal.strip("\n")

        else:
            vardict[varName] = varVal.strip("\n")


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
