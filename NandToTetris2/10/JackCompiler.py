import os
import glob
import numpy

folder_directory = "C:/Users/Paul/Documents/Open Source Society for Computer Science (OSSU)/nand2tetris/projects/10/CompileFolder"
jack_file_directory = folder_directory + "/*.jack"
xml_directory = folder_directory + "/*.xml"


class JackReader:
    """A Jack Reader Class"""

    # instance attribute
    def __init__(self, jack_file):
        self.jack_files = ["placeholder"]
        self.jack_array = []
        self.jack_file_name = ['placeholder']

        jack_directories = glob.glob(jack_file)
        for i, jack_add in enumerate(jack_directories):
            if jack_add[-5:] == '.jack':
                file_name = os.path.basename(jack_add)
                if file_name == "Main.jack":
                    self.jack_files[0] = jack_add
                    self.jack_file_name[0] = (file_name[0:-5])
                else:
                    self.jack_files.append(jack_add)
                    self.jack_file_name.append(file_name[0:-5])

        for jack_address in self.jack_files:
            temp_array = []
            jack_file = open(jack_address, 'r')
            for jack_element in jack_file:
                temp_array.append(jack_element.strip())

            self.jack_array.append(temp_array)

    def get_jack_array(self):
        jack_file_name_tuple = []
        for i, element in enumerate(self.jack_array):
            jack_file_name_tuple.append((element, self.jack_file_name[i]))

        return jack_file_name_tuple


class JackTokenizer:
    """A jack Tokenizer Class"""
    def __init__(self, jack_array):
        # initializations
        self.jack_index = -1
        self.current_token = "placeholder"
        self.is_comment_mode = False
        self.is_string = False
        self.jack_array_token_elements = []
        self.jack_file_name = jack_array[1]

        # Initializes the jack_array
        self.jack_array_initializer(jack_array[0])

        # Tokenize commands
        self.token_array = ['<tokens>']
        while self.has_more_tokens():
            self.advance()
            self.token_type()
        self.token_array.append('</tokens>')

    def jack_array_initializer(self, f_jack_array):
        # Remove the line comments entries
        jack_array_no_line_comments = []
        for element in f_jack_array:
            if len(element) > 1:
                if element[0] == '/' and element[1] == '/':
                    pass
                else:
                    jack_array_no_line_comments.append(element)
            else:
                jack_array_no_line_comments.append(element)

        # Revises the jack_array_no_line_comments elements into token form
        jack_array_no_comments = []
        for line in jack_array_no_line_comments:
            # For string tokens
            if '"' in line:
                token_array = self.token_string_fixer(line)
            # For others
            else:
                token_array = line.split()

            for token in token_array:
                if not self.is_comment_mode:
                    if token == '/**':
                        self.is_comment_mode = True
                    elif token == '//':
                        break
                    else:
                        jack_array_no_comments.append(token)
                else:
                    if token == '*/':
                        self.is_comment_mode = False

        for token in jack_array_no_comments:
            self.jack_token_fixer(token)

    def token_string_fixer(self, line, current_array=['reset123']):
        if current_array == ['reset123']:
            token_array_holder = []
        else:
            token_array_holder = current_array
        if '"' in line:
            left_symbol_index = line.index('"')
            left_lines = line[0:left_symbol_index]

            remaining_lines = line[left_symbol_index + 1:]
            if '"' in remaining_lines:
                right_symbol_index = remaining_lines.index('"') + left_symbol_index + 1
                right_lines = line[right_symbol_index + 1:]
            else:
                print('ERROR!!! no right "')

            [token_array_holder.append(element) for element in left_lines.split()]
            token_array_holder.append(line[left_symbol_index])
            token_array_holder.append(line[left_symbol_index + 1:right_symbol_index])
            token_array_holder.append(line[right_symbol_index])

            # Recursion will start here
            self.token_string_fixer(right_lines, token_array_holder)
            return token_array_holder
        else:
            [token_array_holder.append(element) for element in line.split()]

    def jack_token_fixer(self, f_token):
        token = f_token
        # Check for token length
        if len(token) > 1:
            # Check for (
            if '(' in token:
                self.token_fixer_rec_function('(', token)

            # check for )
            elif ')' in token:
                self.token_fixer_rec_function(')', token)

            # Check for [
            elif '[' in token:
                self.token_fixer_rec_function('[', token)

            # check for ]
            elif ']' in token:
                self.token_fixer_rec_function(']', token)

            # Check for {
            elif '{' in token:
                self.token_fixer_rec_function('{', token)

            # check for }
            elif '}' in token:
                self.token_fixer_rec_function('}', token)

            # Check for .
            elif '.' in token:
                self.token_fixer_rec_function('.', token)

            # Check for .
            elif '~' in token:
                self.token_fixer_rec_function('~', token)

            # check for ,
            elif ',' in token:
                self.token_fixer_rec_function(',', token)

            # Check for ;
            elif ';' in token:
                self.token_fixer_rec_function(';', token)

            # Check for |
            elif '|' in token:
                self.token_fixer_rec_function('|', token)

            # Check for "
            elif '"' in token:
                self.token_fixer_rec_function('"', token)

            # check for operators
            elif '+' in token:
                self.token_fixer_rec_function('+', token)

            elif '-' in token:
                self.token_fixer_rec_function('-', token)

            elif '*' in token:
                self.token_fixer_rec_function('*', token)

            elif '/' in token:
                self.token_fixer_rec_function('/', token)
            # end of check for operators

            else:
                self.jack_array_token_elements.append(token)

        elif len(token) == 1:
            self.jack_array_token_elements.append(token)

    def token_fixer_rec_function(self, symbol, token):
        if symbol in token:
            symbol_index = token.index(symbol)

            # fix before symbol: recursion
            self.jack_token_fixer(token[0:symbol_index])

            # append the symbol
            self.jack_array_token_elements.append(token[symbol_index])

            # fix the right of the symbol: recursion
            self.jack_token_fixer(token[symbol_index + 1:])

    def has_more_tokens(self):
        if self.jack_index < len(self.jack_array_token_elements)-1:
            return True
        else:
            return False
        
    def advance(self):
        self.jack_index += 1
        self.current_token = self.jack_array_token_elements[self.jack_index]

    def token_type(self):
        element = self.current_token
        if (element == 'class' or element == 'constructor' or element == 'function' or
                element == 'method' or element == 'field' or element == 'static' or element == 'var' or
                element == 'int' or element == 'char' or element == 'boolean' or element == 'void' or element == 'true' or
                element == 'false' or element == 'null' or element == 'this' or element == 'let' or element == 'do' or
                element == 'if' or element == 'else' or element == 'while' or element == 'return'):
            self.token_array.append('<keyword> ' + element + ' </keyword>')

        # Symbol
        elif (element == '{' or element == '}' or element == '(' or element == ')' or element == '[' or element == ']' or
                element == '.' or element == ',' or element == ';' or element == '+' or element == '-' or element == '*' or
                element == '/' or element == '&' or element == '|' or element == '<' or element == '>' or
                element == '=' or element == '-' or element == '~'):
            if element == '<':
                self.token_array.append('<symbol> ' + '&lt;' + ' </symbol>')
            elif element == '>':
                self.token_array.append('<symbol> ' + '&gt;' + ' </symbol>')
            elif element == '&':
                self.token_array.append('<symbol> ' + '&amp;' + ' </symbol>')

            else:
                self.token_array.append('<symbol> ' + element + ' </symbol>')

        # string_constant Special case: will use self.advance to adjust for not using '"'
        elif element == '"':
            self.advance()
            string_element = self.current_token
            self.token_array.append('<stringConstant> ' + string_element + ' </stringConstant>')
            self.advance()

        # identifier
        elif not element[0].isdigit():
            self.token_array.append('<identifier> ' + element + ' </identifier>')

        # integer_constant
        elif element.isdigit():
            self.token_array.append('<integerConstant> ' + element + ' </integerConstant>')

    def get_token_filename_tuple(self):
        return self.token_array, self.jack_file_name

    def make_token_file(self, f_file_name=''):
        if f_file_name == '':
            file_name = self.jack_file_name + 'Tokens'
        else:
            file_name = f_file_name

        file = open(folder_directory + '/' + file_name + '.xml', 'w')
        for token_element in self.token_array:
            file.write(token_element + '\n')


class XMLReader:
    """A xml reader class"""

    # instance attribute
    def __init__(self, token_file):
        self.xml_files = ["placeholder"]
        self.token_array = []
        self.xml_file_name = ['placeholder']

        xml_directories = glob.glob(token_file)
        for i, xml_add in enumerate(xml_directories):
            if xml_add[-5:] == 'T.xml':
                file_name = os.path.basename(xml_add)
                if file_name == "MainT.xml":
                    self.xml_files[0] = xml_add
                    self.xml_file_name[0] = (file_name[0:-5])
                else:
                    self.xml_files.append(xml_add)
                    self.xml_file_name.append(file_name[0:-5])

        for token_address in self.xml_files:
            temp_array = []
            token_file = open(token_address, 'r')
            for token_element in token_file:
                temp_array.append(token_element.strip())

            self.token_array.append(temp_array)

    def get_token_array(self):
        token_file_name_tuple = []
        for i, element in enumerate(self.token_array):
            token_file_name_tuple.append((element, self.xml_file_name[i]))

        return token_file_name_tuple


class JackCompiler:
    """A jack Compiler Class"""
    def __init__(self, token_array):
        self.token_array = token_array[0]
        self.token_file_name = token_array[1]
        self.token_index = 0
        self.current_token = "placeholder"
        self.jack_array = []
        self.class_names = []
        self.subroutine_name = "placeholder"
        self.var_names = []

        # Starts the compilation and makes sure the first token is a class
        if self.has_more_tokens():
            self.advance()
            if self.current_token == '<keyword> class </keyword>':
                self.compile_class()
            else:
                print("ERROR!!! A jack compiler must always have a class as it's first token!!!")

    def has_more_tokens(self):
        if self.token_array[self.token_index+1] == "</tokens>":
            return False
        else:
            return True

    def advance(self):
        self.token_index += 1
        self.current_token = self.token_array[self.token_index]
        return self

    def compile_class(self):
        sc = 2  # sc means space counter (usually for the spacing)
        self.jack_array.append('<class>')   # <class>

        # 'class'
        self.jack_array.append(' ' * sc + self.current_token)

        # className: <identifier> Main </identifier>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)
        # store the className in the className table
        self.class_names.append(self.current_token)

        # '{'
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # classVarDec: <classVarDec> red words </classVarDec> THIS CAN REPEAT
        while self.check_token(1, '<keyword> static </keyword>', '<keyword> field </keyword>'):
            self.advance()
            self.compile_class_var_dec(sc)

        # subroutineDec: <subroutineDec> some words </subroutineDec> THIS CAN REPEAT
        while self.check_token(1, '<keyword> constructor </keyword>', '<keyword> function </keyword>',
                               '<keyword> method </keyword>'):
            self.advance()
            self.compile_subroutine(sc)

        # } <symbol> } </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        self.jack_array.append('</class>')
        # end of Class --------------------------------------------------------------------

    def compile_class_var_dec(self, c_sc):
        # c_sc is the caller's space counter
        self.jack_array.append(' ' * c_sc + '<classVarDec>')  # <class>
        sc = c_sc + 2

        # static | field
        self.jack_array.append(' ' * sc + self.current_token)

        # type: Int|Char|Boolean|ClassName
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # varName
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)
        # Store the var Name
        self.var_names.append(self.current_token)

        # Repetition of varName if applicable
        while self.check_token(1, '<symbol> , </symbol>'):
            # comma
            self.advance()
            self.jack_array.append(' ' * sc + self.current_token)

            # varName
            self.advance()
            self.jack_array.append(' ' * sc + self.current_token)
            # Store the var Name
            self.var_names.append(self.current_token)

        # ;
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        self.jack_array.append(' ' * c_sc + '</classVarDec>')
        # End of ClassVarDec-------------------------------------------------------------

    def compile_subroutine(self, c_sc):
        # c_sc is the caller's space_counter
        self.jack_array.append(' ' * c_sc + '<subroutineDec>')  # <SubroutineDec>
        sc = c_sc + 2

        # Construction|Function|Method: <keyword> function </keyword>
        self.jack_array.append(' ' * sc + self.current_token)

        # void | Type: <keyword> void </keyword>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # subroutineName: <identifier> main </identifier>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # (: <symbol> ( </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # ParameterList:
        self.advance()
        is_void = self.compile_parameter_list(sc)   # is_void will contain a boolean whether
                                                    # there is a parameter or not

        # ): <symbol> ) </symbol>
        # If parameter list is Void then no self.advance is needed
        if not is_void:
            self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

    # SubroutineBody -adjust-space-counter----------------------------------------------------------------------
        self.jack_array.append(' ' * sc + '<subroutineBody>')  # <subroutineBody>
        i_sc = sc + 2   # inner space_counter

        # {: <symbol> { </symbol>
        self.advance()
        self.jack_array.append(' ' * i_sc + self.current_token)

        # VarDec: Can REPEAT
        while self.check_token(1, '<keyword> var </keyword>'):
            self.advance()
            self.compile_var_dec(i_sc)

        # Statements---------------------------------------------------------
        self.advance()
        self.compile_statements(i_sc)

        # ; : <symbol> } </symbol>
        self.advance()
        self.jack_array.append(' ' * i_sc + self.current_token)

        self.jack_array.append(' ' * sc + '</subroutineBody>')     # </subroutineBody>
    # End of Subroutine Body------------------------------------------------

        self.jack_array.append(' ' * c_sc + '</subroutineDec>')  # </subroutineDec>
        # End of Subroutine Dec------------------------------------------------

    def compile_parameter_list(self, c_sc):
        self.jack_array.append(' ' * c_sc + '<parameterList>')  # <parameterList>
        is_comma = False    # Initialize for the while loop (different structure than standard)
        is_void = True  # this will be returned to say if there are any parameters or none
        sc = c_sc + 2

        # Type or None at all: Initial
        if self.check_token(0, '<keyword> int </keyword>', '<keyword> char </keyword>',
                               '<keyword> boolean </keyword>') or self.is_token_class():
            is_void = False
            # type : <keyword> int </keyword>
            self.jack_array.append(' ' * sc + self.current_token)

            # varName
            self.advance()
            self.jack_array.append(' ' * sc + self.current_token)
            self.var_names.append(self.current_token)

            # Repeating parameterList if applicable (will repeat if comma is found next)
            while self.check_token(1, '<symbol> , </symbol>'):
                # , : <symbol> , </symbol>'
                self.advance()
                self.jack_array.append(' ' * sc + self.current_token)

                # type : <keyword> int </keyword>
                self.advance()
                self.jack_array.append(' ' * sc + self.current_token)

                # varName
                self.advance()
                self.jack_array.append(' ' * sc + self.current_token)
                self.var_names.append(self.current_token)

        # End of ParameterList: </parameterList>
        self.jack_array.append(' ' * c_sc + '</parameterList>')

        return is_void
        # End of ParameterList-------------------------------------------------------------

    def compile_var_dec(self, c_sc):
        self.jack_array.append(' ' * c_sc + '<varDec>')  # <varDec>
        sc = c_sc + 2

        # 'var': <keyword> var </keyword>
        self.jack_array.append(' ' * sc + self.current_token)

        # type : <identifier> SquareGame </identifier>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)
        # if the type is an identifier it is a className: Update className array
        self.class_names.append(self.current_token)

        # varName: <identifier> game </identifier>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)
        # Store the var_name
        self.var_names.append(self.current_token)

        while self.check_token(1, '<symbol> , </symbol>'):
            # comma :
            self.advance()
            self.jack_array.append(' ' * sc + self.current_token)

            # varName
            self.advance()
            self.jack_array.append(' ' * sc + self.current_token)
            # Store the var_name
            self.var_names.append(self.current_token)

        # ; <symbol> ; </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        self.jack_array.append(' ' * c_sc + '</varDec>')  # </varDec>
        # end of var-dec-------------------------------------------------------------

    # this is put top because this is confusing as hell
    def compile_statements(self, c_sc):
        self.jack_array.append(' ' * c_sc + '<statements>')  # <Statements>
        sc = c_sc + 2

        # Initial Check statement so no self.advance is needed (parallel to other compile functions)
        self.check_statement(sc)

        # Recursion: statements*
        while self.check_token(1, '<keyword> let </keyword>', '<keyword> do </keyword>',
                                  '<keyword> return </keyword>', '<keyword> if </keyword>',
                               '<keyword> while </keyword>'):
            # Statement type: <____Statement>
            self.advance()
            self.check_statement(sc)

        self.jack_array.append(' ' * c_sc + '</statements>')  # </statements>
        # End of Statements------------------------------------------------

    def check_statement(self, c_sc):
        # Check if the statement is a let statement
        if self.current_token == '<keyword> let </keyword>':
            self.compile_let_statement(c_sc)

        # Check if the statement is a do statement
        elif self.current_token == '<keyword> do </keyword>':
            self.compile_do_statement(c_sc)

        # Check if the statement is a return statement
        elif self.current_token == '<keyword> return </keyword>':
            self.compile_return_statement(c_sc)

        # Check if the statement is an if statement
        elif self.current_token == '<keyword> if </keyword>':
            self.compile_if_statement(c_sc)

        # Check if the statement is a while statement
        elif self.current_token == '<keyword> while </keyword>':
            self.compile_while_statement(c_sc)

    def compile_let_statement(self, c_sc):
        self.jack_array.append(' ' * c_sc + '<letStatement>')  # <Statements: letStatement>
        sc = c_sc + 2

        # 'let': '<keyword> let </keyword>'
        self.jack_array.append(' ' * sc + self.current_token)

        # varName
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)
        # Store the varName
        self.var_names.append(self.current_token)

        # check if it has [expression]--------------------------------
        if self.check_token(1, "<symbol> [ </symbol>"):
            # [ : <symbol> [ </symbol>
            self.advance()
            self.jack_array.append(' ' * sc + self.current_token)

            # Expression
            self.advance()
            self.compile_expression(sc)

            # ] : <symbol> ] </symbol>
            self.advance()
            self.jack_array.append(' ' * sc + self.current_token)
        # -------------------------------------------------------------

        # = : <symbol> = </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # expression
        self.advance()
        self.compile_expression(sc)

        # ; : <symbol> ; </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        self.jack_array.append(' ' * c_sc + '</letStatement>')  # <Statements>
        # end of Let Statement-----------------------------------

    def compile_if_statement(self, c_sc=0):
        self.jack_array.append(' ' * c_sc + '<ifStatement>')  # <Statements: ifStatement>
        sc = c_sc + 2

        # if: <keyword> if </keyword>
        self.jack_array.append(' ' * sc + self.current_token)

        # ( : <symbol> ( </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # expression
        self.advance()
        self.compile_expression(sc)

        # ) : <symbol> ) </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # { : <symbol> { </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # statements
        self.advance()
        self.compile_statements(sc)

        # } : <symbol> } </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # Check if there is an Else Statement
        if self.check_token(1, '<keyword> else </keyword>'):
            # else: <keyword> else </keyword>
            self.advance()
            self.jack_array.append(' ' * sc + self.current_token)

            # { : <symbol> { </symbol>
            self.advance()
            self.jack_array.append(' ' * sc + self.current_token)

            # statements
            self.advance()
            self.compile_statements(sc)

            # } : <symbol> } </symbol>
            self.advance()
            self.jack_array.append(' ' * sc + self.current_token)

        self.jack_array.append(' ' * c_sc + '</ifStatement>')

        # end of ifStatement----------------------------------------------

    def compile_while_statement(self, c_sc=0):
        self.jack_array.append(' ' * c_sc + '<whileStatement>')  # <Statements: whileStatement>
        sc = c_sc + 2

        # while keyword <keyword> while </keyword>
        self.jack_array.append(' ' * sc + self.current_token)

        # ( : <symbol> ( </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # expression
        self.advance()
        self.compile_expression(sc)

        # ) : <symbol> ) </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # { : <symbol> { </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # statements
        self.advance()
        self.compile_statements(sc)

        # } <symbol> } </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        self.jack_array.append(' ' * c_sc + '</whileStatement>')  # <EndOfStatements: whileStatement>
        # End of While Statement------------------------------------------------------------------------------

    def compile_do_statement(self, c_sc=0):
        self.jack_array.append(' ' * c_sc + '<doStatement>')  # <Statements: doStatement>
        sc = c_sc + 2

        # do: '<keyword> do </keyword>'
        self.jack_array.append(' ' * sc + self.current_token)

        # Subroutine Call:
        self.advance()
        self.og_compile_subroutine_call(sc)

        # ; : <symbol> ; </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        self.jack_array.append(' ' * c_sc + '</doStatement>')  # <Statements: doStatement>
        # End of do_statement------------------------------------------------

    def compile_return_statement(self, c_sc=0):
        self.jack_array.append(' ' * c_sc + '<returnStatement>')  # <Statements: returnStatement>
        sc = c_sc + 2

        # return: <keyword> return </keyword>
        self.jack_array.append(' ' * sc + self.current_token)

        # Expression: <Expression> ____ </Expression>
        if not self.check_token(1, '<symbol> ; </symbol>'):
            self.advance()
            self.compile_expression(sc)

        # ; <symbol> ; </symbol>'
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        self.jack_array.append(' ' * c_sc + '</returnStatement>')  # </Statements: /returnStatement>
        # End of return Statement---------------------------------------

    def compile_expression(self, c_sc):
        self.jack_array.append(' ' * c_sc + '<expression>')  # <Expression>
        sc = c_sc + 2

        # term : compile term
        self.compile_term(sc)

        # (op term)* will keep repeating as long as there is a term----------
        is_op = self.check_token(1, '<symbol> + </symbol>', '<symbol> - </symbol>', '<symbol> * </symbol>',
                                    '<symbol> / </symbol>', '<symbol> &amp; </symbol>', '<symbol> | </symbol>',
                                    '<symbol> &lt; </symbol>', '<symbol> &gt; </symbol>', '<symbol> = </symbol>')

        while is_op:
            # op: <symbol> + or - or | something </symbol>
            self.advance()
            self.jack_array.append(' ' * sc + self.current_token)

            # term:
            self.advance()
            self.compile_term(sc)

            is_op = self.check_token(1, '<symbol> + </symbol>', '<symbol> - </symbol>', '<symbol> * </symbol>',
                                        '<symbol> / </symbol>', '<symbol> &amp; </symbol>', '<symbol> | </symbol>',
                                        '<symbol> &lt; </symbol>', '<symbol> &gt; </symbol>', '<symbol> = </symbol>')

        self.jack_array.append(' ' * c_sc + '</expression>')  # <Expression>
        # end of Expression---------------------------------------------------------

    def compile_term(self, c_sc=0):
        self.jack_array.append(' ' * c_sc + '<term>')  # <term>
        sc = c_sc + 2

        # term: Integer|String|Keyword Constant; varName| varName[EXPRESSION]; |SUBROUTINECALL|
        # (EXPRESSION)| unary Op term
        # Note words in caps-lock means it contains a possible recursion

        # the term is an integer constant
        if self.current_token[0:17] == '<integerConstant>':
            self.jack_array.append(' ' * sc + self.current_token)

        # the term is a string constant
        elif self.current_token[0:16] == '<stringConstant>':
            self.jack_array.append(' ' * sc + self.current_token)

        # The term is a keyword constant
        elif self.check_token(0, '<keyword> true </keyword>', '<keyword> false </keyword>',
                               '<keyword> null </keyword>', '<keyword> this </keyword>'):
            self.jack_array.append(' ' * sc + self.current_token)

        # the term is a varName[ or varName
        elif self.is_token_var() and not self.check_token(1, '<symbol> . </symbol>'):
            # varName : <identifier> ___ </identifier>
            self.jack_array.append(' ' * sc + self.current_token)

            if self.check_token(1, '<symbol> [ </symbol>'):
                # [ : <symbol> [ </symbol>
                self.advance()
                self.jack_array.append(' ' * sc + self.current_token)

                # expression
                self.advance()
                self.compile_expression(sc)

                # ] : <symbol> ] </symbol>
                self.advance()
                self.jack_array.append(' ' * sc + self.current_token)

        # the term is a SubroutineCall: Current token is varName or className under SubroutineCall
        # (className|varName).SubroutineName(expressionList) or it can be a subroutineName(ExpressionList)
        elif (self.is_token_class() or self.is_token_var() or self.check_token(1, '<symbol> . </symbol>')
                or (self.current_token[0:12] == '<identifier>' and self.check_token(1, '<symbol> ( </symbol>'))):
            self.og_compile_subroutine_call(sc)

        # the term is an (expression) -----------------------------------------
        elif self.current_token == '<symbol> ( </symbol>':
            # ( : <symbol> ( </symbol>
            self.jack_array.append(' ' * sc + self.current_token)

            # expression
            self.advance()
            self.compile_expression(sc)

            # ) : <symbol> ) </symbol>
            self.advance()
            self.jack_array.append(' ' * sc + self.current_token)
        # end of (expression)--------------------------------------------------

        # the term is an unaryOp
        elif self.current_token == '<symbol> - </symbol>' or self.current_token == '<symbol> ~ </symbol>':
            # '-' : <symbol> - or ~ </symbol>
            self.jack_array.append(' ' * sc + self.current_token)

            # term :
            self.advance()
            self.compile_term(sc)

        self.jack_array.append(' ' * c_sc + '</term>')

        # END OF TERM----------------------------------

    def og_compile_subroutine_call(self, c_sc=0):
        # Subroutine Name or Class Name|Var Name
        self.jack_array.append(' ' * c_sc + self.current_token)

        if self.check_token(1, '<symbol> ( </symbol>'):
            # ( symbol
            self.advance()
            self.jack_array.append(' ' * c_sc + self.current_token)

            # expressionList ------------------------------------
            self.call_expression_list(c_sc)
            # /expressionList-----------------------------------

            # ) symbol
            self.advance()
            self.jack_array.append(' ' * c_sc + self.current_token)

        else:
            # . : <symbol> . </symbol>
            self.advance()
            self.jack_array.append(' ' * c_sc + self.current_token)

            # subroutineName : <identifier> new </identifier>
            self.advance()
            self.jack_array.append(' ' * c_sc + self.current_token)

            # ( : <symbol> ( </symbol>
            self.advance()
            self.jack_array.append(' ' * c_sc + self.current_token)

            # expressionList ------------------------------------
            self.call_expression_list(c_sc)
            # /expressionList-----------------------------------

            # ) : <symbol> ) </symbol>
            self.advance()
            self.jack_array.append(' ' * c_sc + self.current_token)

    def call_expression_list(self, c_sc):
        if self.check_token(1, '<symbol> ) </symbol>'):
            self.compile_expression_list(c_sc)
        else:
            self.advance()
            self.compile_expression_list(c_sc)

    # End of subroutineCall ---------------------------

    def compile_expression_list(self, c_sc=0):
        self.jack_array.append(' ' * c_sc + '<expressionList>')  # <expressionList>
        sc = c_sc + 2

        # The caller of this method is always choosing between entering '(' or the expression
        # token itself. When current token is ( then there is no expression

        # There is an expression
        if not self.check_token(0, '<symbol> ( </symbol>') or not self.check_token(1, '<symbol> ) </symbol>'):
            # expression Initial
            self.compile_expression(sc)

            # expression recursion
            while self.check_token(1, '<symbol> , </symbol>'):
                # , : <symbol> , </symbol>
                self.advance()
                self.jack_array.append(' ' * sc + self.current_token)

                # expression
                self.advance()
                self.compile_expression(sc)

        # End of expression List
        self.jack_array.append(' ' * c_sc + '</expressionList>')  # </expressionList>
        # End of Expression List-----------------------------------------------------------

    def is_token_class(self):
        for class_name in self.class_names:
            if self.current_token == class_name:
                return True

        return False

    def is_token_var(self):
        for var_name in self.var_names:
            if self.current_token == var_name:
                return True

        return False

    def check_token(self, shift, *f_tokens):
        for token_element in f_tokens:
            if self.token_array[self.token_index + shift] == token_element:
                return True

        return False

    def get_jack_file(self):
        return self.jack_array

    def make_jack_file(self, f_file_name=''):
        if f_file_name == '':
            file_name = self.token_file_name + 'JackCompiled'
        else:
            file_name = f_file_name

        file = open(folder_directory + '/' + file_name + '.xml', 'w')
        for token_element in self.jack_array:
            file.write(token_element + '\n')


token_tuple_array = []

jack_files = JackReader(jack_file_directory)
jack_arrays = jack_files.get_jack_array()


def jack_translate():
    # tokenizer
    for tuple_element in jack_arrays:
        token_array = JackTokenizer(tuple_element)
        token_tuple_array.append(token_array.get_token_filename_tuple())

    # jack_compiler
    for tuple_element in token_tuple_array:
        jack_array = JackCompiler(tuple_element)
        jack_array.make_jack_file()

def jack_tester():
    token_array = JackTokenizer(jack_arrays[1])
    token_tuple_array.append(token_array.get_token_filename_tuple())
    token_array.make_token_file()


jack_translate()
