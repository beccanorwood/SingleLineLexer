from tkinter import *


class LexerGUI:
    __position__ = 1.0  # Position that keeps track of beginning of each string user enters
    __lineNum__ = 0  # Current Line Number for entry box
    __lineCounter__ = 1  # Line numbers for input text box
    __inputList__ = []  # List to hold each line separately
    __lexer_dict__ = {}  # dictionary that reads each line of input and corresponds to a line number

    def __init__(self, root):
        self.master = root
        self.master.title("Lexical Analyzer for TinyPie")

        """Label for Input Text Widget"""
        self.inputLabel = Label(self.master, text="Source Code Input", font="Helvetica 12 bold")
        self.inputLabel.grid(row=0, column=0, pady=5)

        """Input Text Widget Attributes"""
        self.inputBox = Text(self.master, bd=5, relief=SUNKEN)
        """Bind method that adds a line number after the user has entered it """
        """self.inputBox.bind("<Return>", lambda e: self.line_number(self.__lineCounter__))"""
        self.inputBox.grid(row=1, column=0, padx=15)
        self.inputBox.configure(width=40, height=15)

        """Line Number Label"""
        self.currprocessingline = Label(self.master, text="Current Processing Line:", font="Helvetica 10 bold")
        self.currprocessingline.grid(row=2, column=0, sticky=W, pady=5, padx=25)

        """Line number entry widget corresponding to number of line is being transferred to output widget"""
        self.lineNumber = Entry(self.master, bd=2, relief=SOLID)
        self.lineNumber.insert(2, self.__lineNum__)
        self.lineNumber.grid(row=2, column=0, sticky=E, pady=5, padx=32)
        self.lineNumber.configure(width=5)

        """Button that user will press when they want to analyze next line"""
        self.nextLine = Button(self.master, text="Next Line", bg="lightblue", command=self.readLine)
        self.nextLine.grid(row=3, column=0, sticky=E, pady=10, padx=29)
        self.nextLine.configure(height=1, width=15)

        """Label for Output Text Widget"""
        self.outputLabel = Label(self.master, text="Lexical Analyzed Result", font="Helvetica 12 bold")
        self.outputLabel.grid(row=0, column=1, pady=5)

        """Output Text Widget Attributes"""
        self.outputBox = Text(self.master, bd=5, relief=SUNKEN)
        self.outputBox.grid(row=1, column=1, padx=15)
        self.outputBox.configure(width=40, height=15)

        """Quit Button that will close GUI"""
        self.quit = Button(self.master, text="Quit", bg="lightblue", command=self.master.destroy)
        self.quit.grid(row=3, column=1, sticky=E, pady=10, padx=30)
        self.quit.configure(height=1, width=15)

    """Method that will create line numbers at beginning of new line"""
    """def line_number(self, lineNum):
        self.inputBox.insert(float(lineNum), str(lineNum) + ") ")
        self.__lineCounter__ += 1"""

    """Method that will read all input from user, parse to a list and correlate line numbers via a dictionary"""

    def readLine(self):
        """TEXT HIGHLIGHTING & BOLDING CONFIGURATION"""
        self.inputBox.tag_remove("here", 1.0, float(self.__lineNum__ + 1))
        self.inputBox.tag_configure("here", font=("Georgia", 10, "bold"), background="yellow")

        self.__lineNum__ += 1  # Increment line counter every time next line button is pressed
        self.lineNumber.delete(0, END)  # Clear current number and enter updated count
        self.lineNumber.insert(2, self.__lineNum__)

        """Local Variables"""
        linesCounted = 0
        numList = []  # List of line numbers
        input_Str = []  # List of strings corresponding to line numbers

        text_input = self.inputBox.get("1.0", 'end').rstrip()
        self.__inputList__ = text_input.split('\n')

        """Loop through list, highlight current line that is being processed, update line #, display to output box"""
        for line in self.__inputList__:
            linesCounted += 1
            numList.append(linesCounted)
            input_Str.append(line)

        """Loop through both lists"""
        self.__lexer_dict__ = dict(zip(numList, input_Str))

        """Loop through dictionary and compare current line number to string that needs to be displayed"""
        for key in self.__lexer_dict__.keys():
            if key == self.__lineNum__:
                self.inputBox.tag_add("here", float(key), float(key + 1))
                line = self.__lexer_dict__.get(key)
                analyzedresult = self.analyzeLine(line)
                """Before inserting string, send to separate method to extract lexical values
                self.outputBox.insert(self.__position__, self.__lexer_dict__[key] + '\n')"""
                self.outputBox.delete('1.0', END)  # clear any previous analyzed results
                self.outputBox.insert(self.__position__, analyzedresult, '\n')
                self.outputBox.tag_add("here", self.__position__, END)

    def analyzeLine(self, currLine):

        import re

        output = []  # Output list containing tokens with corresponding type

        # Created a dictionary to hold specific regex expressions with corresponding values (except string)
        tokenList = {r'\b(if|else|int|float)(?=\s|\t)': 'keyword',
                     r'[A-Za-z]+\d+|[A-Za-z]+': 'identifier',
                     r'[=+>*]': 'operator',
                     r'^\d+(?![\d+\.])': 'literal',  # int literal
                     r'\d+\.\d+': 'literal',  # float literal
                     r'[():\";]': 'separator',
                     r'[\t]+|[ ]+': 'space'}

        tempString = currLine

        while len(tempString) != 0:
            if tempString[0] == '\n':  # Catch for any new line characters
                continue
            for x in tokenList:
                token = re.match(x, tempString)
                if token:
                    if tokenList[x] == 'space':  # Remove spacing/tabs without appending to list
                        print(tempString)
                        pos = token.end()
                        tempString = tempString[pos:]
                    elif tokenList[x] == 'sep' and tempString[0] == '\"':  # String condition to check for edge cases
                        output.append('<' + tokenList[x] + ',' + token.group() + '>')
                        pos = token.end()
                        tempString = tempString[pos:]
                        strRgx = re.match(r'^(.)+?(?=\")', tempString)  # string literal regex match
                        if strRgx:
                            output.append('<' + 'lit' + ',' + strRgx.group() + '>')
                            pos = strRgx.end()
                        output.append('<' + tokenList[x] + ',' + token.group() + '>')
                        pos += 1
                        tempString = tempString[pos:]
                    else:
                        output.append('<' + tokenList[x] + ',' + token.group() + '>')
                        pos = token.end()
                        tempString = tempString[pos:]

        print('Output <type,token> list: ', output)
        output = '\n'.join(output)  # Add new line characters to returned list
        return output


if __name__ == '__main__':
    myGUI = Tk()
    displayGUI = LexerGUI(myGUI)
    myGUI.resizable(width=0, height=0)
    myGUI.mainloop()
