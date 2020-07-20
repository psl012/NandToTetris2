import os
import glob

folder_directory = "C:/Users/Paul/Documents/Open Source Society for Computer Science (OSSU)/nand2tetris/projects/11/CompileFolder"
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
        if self.jack_index < len(self.jack_array_token_elements) - 1:
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
        elif (
                element == '{' or element == '}' or element == '(' or element == ')' or element == '[' or element == ']' or
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
        self.class_name = ''
        self.vm_table = []
        self.symbol_table = SymbolTable()

        # Starts the compilation and makes sure the first token is a class
        if self.has_more_tokens():
            self.advance()
            if self.current_token == '<keyword> class </keyword>':
                self.compile_class()
            else:
                print("ERROR!!! A jack compiler must always have a class as it's first token!!!")
        self.symbol_table.print_class_tables()
        print("VM TRANSLATION------------------------------------------")
        [print(vm_code) for vm_code in self.vm_table]

    def has_more_tokens(self):
        if self.token_array[self.token_index + 1] == "</tokens>":
            return False
        else:
            return True

    def advance(self):
        self.token_index += 1
        self.current_token = self.token_array[self.token_index]
        return self

    def compile_class(self):
        sc = 2  # sc means space counter (usually for the spacing)
        self.jack_array.append('<class>')  # <class>

        # 'class'
        self.jack_array.append(' ' * sc + self.current_token)

        # className: <identifier> Main </identifier> SymbolTable Input: Class Scope
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)
        # store the className in the className table
        self.class_names.append(self.current_token)
        self.class_name = self.current_token

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
        # SymbolTable kind entry:
        sym_kind = self.current_token

        # type: Int|Char|Boolean|ClassName
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)
        # SymbolTable type entry:
        sym_type = self.current_token

        # varName SymbolTable Entry
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)
        # Store the var Name
        self.var_names.append(self.current_token)
        sym_name = self.current_token

        self.symbol_table.define(sym_name, sym_type, sym_kind)

        # Repetition of varName if applicable
        while self.check_token(1, '<symbol> , </symbol>'):
            # comma
            self.advance()
            self.jack_array.append(' ' * sc + self.current_token)

            # varName SymbolTable Entry
            self.advance()
            self.jack_array.append(' ' * sc + self.current_token)
            # Store the var Name
            self.var_names.append(self.current_token)
            sym_name = self.current_token
            self.symbol_table.define(sym_name, sym_type, sym_kind)

        # ;
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        self.jack_array.append(' ' * c_sc + '</classVarDec>')
        # End of ClassVarDec-------------------------------------------------------------

    def compile_subroutine(self, c_sc):
        # c_sc is the caller's space_counter
        self.jack_array.append(' ' * c_sc + '<subroutineDec>')  # <SubroutineDec>
        sc = c_sc + 2
        # Holds if function is void or have a return value
        function_type = 'placeholder'

        # Construction|Function|Method: <keyword> function </keyword>
        self.jack_array.append(' ' * sc + self.current_token)

        # void | Type: <keyword> void </keyword>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)
        function_type = self.current_token

        # subroutineName: <identifier> main </identifier> SymbolTable Entry No need but restart subroutine table
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)
        self.symbol_table.start_subroutine('', ('this', self.class_name, 'ARGUMENT'))

        # VM Translation
        # Remove the tags
        f_class_name = self.class_name[13:-14]
        f_class_subroutine = self.current_token[13:-14]
        self.write_function(f_class_name + '.' + f_class_subroutine, '0')

        # (: <symbol> ( </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # ParameterList: Symbol Table Entry
        self.advance()
        is_void = self.compile_parameter_list(sc)  # is_void will contain a boolean whether
        # there is a parameter or not

        # ): <symbol> ) </symbol>
        # If parameter list is Void then no self.advance is needed
        if not is_void:
            self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # SubroutineBody -adjust-space-counter----------------------------------------------------------------------
        self.jack_array.append(' ' * sc + '<subroutineBody>')  # <subroutineBody>
        i_sc = sc + 2  # inner space_counter

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

        self.jack_array.append(' ' * sc + '</subroutineBody>')  # </subroutineBody>
        # End of Subroutine Body------------------------------------------------

        self.jack_array.append(' ' * c_sc + '</subroutineDec>')  # </subroutineDec>
        # End of Subroutine Dec------------------------------------------------

    def compile_parameter_list(self, c_sc):
        self.jack_array.append(' ' * c_sc + '<parameterList>')  # <parameterList>
        is_comma = False  # Initialize for the while loop (different structure than standard)
        is_void = True  # this will be returned to say if there are any parameters or none
        sc = c_sc + 2

        # Type or None at all: Initial
        if self.check_token(0, '<keyword> int </keyword>', '<keyword> char </keyword>',
                            '<keyword> boolean </keyword>') or self.is_token_class():
            is_void = False
            # type : <keyword> int </keyword>
            self.jack_array.append(' ' * sc + self.current_token)
            # SymbolTable Type entry:
            sym_type = self.current_token

            # varName SymbolTable Entry
            self.advance()
            self.jack_array.append(' ' * sc + self.current_token)
            self.var_names.append(self.current_token)
            # SymbolTable Name entry:
            sym_name = self.current_token

            # As of now just assume every paramater in this list is an argument!!!
            sym_kind = 'ARGUMENT'
            self.symbol_table.define(sym_name, sym_type, sym_kind)

            # Repeating parameterList if applicable (will repeat if comma is found next)
            while self.check_token(1, '<symbol> , </symbol>'):
                # , : <symbol> , </symbol>'
                self.advance()
                self.jack_array.append(' ' * sc + self.current_token)

                # type : <keyword> int </keyword>
                self.advance()
                self.jack_array.append(' ' * sc + self.current_token)
                # SymbolTable type entry:
                sym_type = self.current_token

                # varName SymbolTable Entry
                self.advance()
                self.jack_array.append(' ' * sc + self.current_token)
                self.var_names.append(self.current_token)
                # SymbolTable Name Entry:
                sym_name = self.current_token

                # Just assume the kind is an ARGUMENT for now!!!
                self.symbol_table.define(sym_name, sym_type, 'ARGUMENT')

        # End of ParameterList: </parameterList>
        self.jack_array.append(' ' * c_sc + '</parameterList>')

        return is_void
        # End of ParameterList-------------------------------------------------------------

    def compile_var_dec(self, c_sc):
        self.jack_array.append(' ' * c_sc + '<varDec>')  # <varDec>
        sc = c_sc + 2

        # 'var': <keyword> var </keyword>
        self.jack_array.append(' ' * sc + self.current_token)
        # SymbolTable Input: Kind
        sym_kind = self.current_token

        # type : <identifier> SquareGame </identifier> SymbolTable Entry
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)
        # if the type is an identifier it is a className: Update className array
        self.class_names.append(self.current_token)
        # SymbolTable Input: Type
        sym_type = self.current_token

        # varName: <identifier> game </identifier> SymbolTable Entry
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)
        # Store the var_name
        self.var_names.append(self.current_token)
        # SymbolTable Input: Name
        sym_name = self.current_token

        # SymbolTable Input:
        self.symbol_table.define(sym_name, sym_type, sym_kind)

        while self.check_token(1, '<symbol> , </symbol>'):
            # comma :
            self.advance()
            self.jack_array.append(' ' * sc + self.current_token)

            # varName SymbolTable Entry
            self.advance()
            self.jack_array.append(' ' * sc + self.current_token)
            # Store the var_name
            self.var_names.append(self.current_token)
            # SymbolTable Input: Recursion Name
            sym_name = self.current_token

            # SymbolTable Input:
            self.symbol_table.define(sym_name, sym_type, sym_kind)

        # ; <symbol> ; </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        self.jack_array.append(' ' * c_sc + '</varDec>')  # </varDec>
        # end of var-dec-------------------------------------------------------------

    # this is put top because this is confusing as hell
    def compile_statements(self, c_sc, subroutine_type='void'):
        self.jack_array.append(' ' * c_sc + '<statements>')  # <Statements>
        sc = c_sc + 2

        # Initial Check statement so no self.advance is needed (parallel to other compile functions)
        self.check_statement(sc, subroutine_type)

        # Recursion: statements*
        while self.check_token(1, '<keyword> let </keyword>', '<keyword> do </keyword>',
                               '<keyword> return </keyword>', '<keyword> if </keyword>',
                               '<keyword> while </keyword>'):
            # Statement type: <____Statement>
            self.advance()
            self.check_statement(sc)

        self.jack_array.append(' ' * c_sc + '</statements>')  # </statements>
        # End of Statements------------------------------------------------

    def check_statement(self, c_sc, subroutine_type='void'):
        # Check if the statement is a let statement
        if self.current_token == '<keyword> let </keyword>':
            self.compile_let_statement(c_sc)

        # Check if the statement is a do statement
        elif self.current_token == '<keyword> do </keyword>':
            self.compile_do_statement(c_sc)

        # Check if the statement is a return statement
        elif self.current_token == '<keyword> return </keyword>':
            # VM translation: End of a function
            if subroutine_type == 'void':
                self.write_push('CONST', '0')
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

        # varName SymbolTable Output
        self.advance()

        # <identifier>----------------------------------------------------
        # varName
        if self.symbol_table.is_var_defined(self.current_token):
            self.jack_array.append(' ' * sc + self.current_token)
            # Store the varName
            self.var_names.append(self.current_token)
        # </identifier> -------------------------------------------------

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

        # VM For do statement we always need to put the pop temp 0
        self.write_pop('TEMP', '0')
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

        # VM translation
        self.write_return()

        # End of return Statement---------------------------------------

    def compile_expression(self, c_sc, master_level=True):
        self.jack_array.append(' ' * c_sc + '<expression>')  # <Expression>
        sc = c_sc + 2

        # VM translation beginning checkpoint
        if master_level:
            expression_beginning = len(self.jack_array) - 1

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

            # VM Translate------------------------------------------------------------

            # term:
            self.advance()
            self.compile_term(sc)

            is_op = self.check_token(1, '<symbol> + </symbol>', '<symbol> - </symbol>', '<symbol> * </symbol>',
                                     '<symbol> / </symbol>', '<symbol> &amp; </symbol>', '<symbol> | </symbol>',
                                     '<symbol> &lt; </symbol>', '<symbol> &gt; </symbol>', '<symbol> = </symbol>')

        self.jack_array.append(' ' * c_sc + '</expression>')  # <Expression>
        # end of Expression---------------------------------------------------------

        # Start of the VM_Translation----------------------------------------------
        # Check if the current expression is master level or it is just part of a bigger expression to prevent double
        # counting from other expression calls in the bigger picture
        if master_level:
            # Initialize the given array to make it easier to translate by removing unnecessary tags
            initialize_array = self.expression_array_vm_initialize(self.jack_array[expression_beginning:])
          #  self.token_part_viewer(self.jack_array,expression_beginning) #View the array using this for debugging
            # Starts the actual VM translation
            self.expression_vm_translator(initialize_array[1:-1])

    def expression_array_vm_initialize(self, jack_array, output=[]):
        """Initialize the expression section of the token xml file for vm translation"""
        token_holder = output

        # This is where the filtering happens wherein unnecessary tags are ignored
        for element in jack_array:
            current_expression = element.strip()
            if element.strip() == '<expression>':
                token_holder.append((current_expression, 'n/a'))

            elif element.strip() == '</expression>':
                token_holder.append((current_expression, 'n/a'))

            elif element.strip()[0:17] == '<integerConstant>':
                token_holder.append((current_expression[0:17], current_expression[18:-19]))

            elif element.strip() == '<symbol> + </symbol>':
                token_holder.append((current_expression[0:8], current_expression[9:-10]))

            elif element.strip() == '<symbol> * </symbol>':
                token_holder.append((current_expression[0:8], current_expression[9:-10]))

            elif element.strip() == '<symbol> , </symbol>':
                token_holder.append((current_expression[0:8], current_expression[9:-10]))

        return token_holder

    def expression_vm_translator(self, exp_arr, arr_ind=0, branch=False):
        """The official VM translator for Expressions"""
        # Expression is a Number
        if exp_arr[arr_ind][0] == '<integerConstant>' and len(exp_arr) == 1:
            self.write_push('CONST', exp_arr[0][1])

        # Expression is Exp1 Op Exp2
        elif len(exp_arr) >= 3:
            if (exp_arr[arr_ind][0] == '<integerConstant>' and exp_arr[arr_ind + 1][0] == '<symbol>' and
                    (exp_arr[arr_ind + 2][0] == '<integerConstant>' or exp_arr[arr_ind + 2][0] == '<expression>')):
                exp1 = [exp_arr[arr_ind]]
                exp2 = exp_arr[arr_ind+2:]
                op = exp_arr[arr_ind+1]
                self.expression_vm_translator(exp1)

                # Checks to see if exp2 is also a compounded expression
                if exp2[0][0] == '<expression>':
                    self.expression_vm_translator(exp2[1:-1])
                # Expression to is just a simple expression (like a constant integer)
                else:
                    self.expression_vm_translator(exp2)

                # Writes the operation symbol based on the VM algorithm

                # A function called Math.multiply is already given for us
                if op[1] == '*':
                    self.write_call('Math.multiply', exp1[0][1])

                # Standard Adding
                elif op[1] == '+':
                    self.write_arithmetic('ADD')

    def token_part_viewer(self, jack_array, array_index=0):
        """View the current jack array: use expression_beginning for array_index"""
        if jack_array[array_index].strip() != '</expression>':
            print(jack_array[array_index].strip())
            self.token_part_viewer(jack_array, array_index + 1)
        else:
            print(jack_array[array_index].strip())

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

        # the term is a varName[ or varName SymbolTable Output
       # elif self.is_token_var() and not self.check_token(1, '<symbol> . </symbol>'):
        elif self.symbol_table.is_var_defined(self.current_token) and not self.check_token(1, '<symbol> . </symbol>'):
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
        elif (self.symbol_table.is_var_defined(self.current_token) or self.check_token(1, '<symbol> . </symbol>')
              or (self.current_token[0:12] == '<identifier>' and self.check_token(1, '<symbol> ( </symbol>'))):
            self.og_compile_subroutine_call(sc)

        # the term is an (expression) -----------------------------------------
        elif self.current_token == '<symbol> ( </symbol>':
            # ( : <symbol> ( </symbol>
            self.jack_array.append(' ' * sc + self.current_token)

            # expression
            self.advance()
            self.compile_expression(sc, False)

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

    def og_compile_subroutine_call(self, c_sc=0, master_level=True):
        # Subroutine Name or Class Name|Var Name SymbolTable Output SPECIAL Case
        # This is a special case because usually the subroutine Calls came from the OS

        current_expression = ''
        subroutine_name = ''
        exp_count = ''

        # VM translation beginning checkpoint
        if master_level:
            subroutine_call_beginning = len(self.jack_array) - 1

        # SubroutineName
        self.jack_array.append(' ' * c_sc + self.current_token)

        subroutine_name += self.current_token[13:-14]

        if self.check_token(1, '<symbol> ( </symbol>'):
            # ( symbol
            self.advance()
            self.jack_array.append(' ' * c_sc + self.current_token)

            # expressionList ------------------------------------
            exp_count = self.call_expression_list(c_sc)
            # /expressionList-----------------------------------

            # ) symbol
            self.advance()
            self.jack_array.append(' ' * c_sc + self.current_token)

        else:
            # . : <symbol> . </symbol>
            self.advance()
            self.jack_array.append(' ' * c_sc + self.current_token)

            subroutine_name += self.current_token[9:-10]

            # subroutineName : <identifier> new </identifier> SymbolTable Output
            self.advance()
            self.jack_array.append(' ' * c_sc + self.current_token)

            subroutine_name += self.current_token[13:-14]

            # ( : <symbol> ( </symbol>
            self.advance()
            self.jack_array.append(' ' * c_sc + self.current_token)

            # expressionList ------------------------------------
            exp_count = self.call_expression_list(c_sc)
            # /expressionList-----------------------------------

            # ) : <symbol> ) </symbol>
            self.advance()
            self.jack_array.append(' ' * c_sc + self.current_token)

            # This is where we will put the Call VM translation: I hope
            self.write_call(subroutine_name, exp_count)

            # Note for July 9 Paul: Basically try to apply the logic you used here in Subroutine Call to
            # all the routines

    # End of Subroutine Call-----------------------------------

    def call_expression_list(self, c_sc):
        # Holds the exp_count coming from expression_list
        exp_count_holder = 0

        if self.check_token(1, '<symbol> ) </symbol>'):
            exp_count_holder = self.compile_expression_list(c_sc)
        else:
            self.advance()
            exp_count_holder = self.compile_expression_list(c_sc)

        return str(exp_count_holder)

    def compile_expression_list(self, c_sc=0):
        self.jack_array.append(' ' * c_sc + '<expressionList>')  # <expressionList>
        sc = c_sc + 2

        # Counter for the number of expressions
        exp_count = 0

        # The caller of this method is always choosing between entering '(' or the expression
        # token itself. When current token is ( then there is no expression

        # There is an expression
        if not self.check_token(0, '<symbol> ( </symbol>') or not self.check_token(1, '<symbol> ) </symbol>'):
            # expression Initial
            self.compile_expression(sc)
            exp_count += 1

            # expression recursion
            while self.check_token(1, '<symbol> , </symbol>'):
                # , : <symbol> , </symbol>
                self.advance()
                self.jack_array.append(' ' * sc + self.current_token)

                # expression
                self.advance()
                self.compile_expression(sc)
                exp_count += 1

        # End of expression List
        self.jack_array.append(' ' * c_sc + '</expressionList>')  # </expressionList>

        return exp_count
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

    def write_push(self, segment, index):
        if segment == 'CONST':
            self.vm_table.append('push constant ' + index)

    def write_pop(self, segment, index):
        if segment == 'TEMP':
            self.vm_table.append('pop temp ' + index)

    def write_arithmetic(self, command):
        if command == 'ADD':
            self.vm_table.append('add')

    def write_function(self, name, nLocals):
        self.vm_table.append('function ' + name + ' ' + nLocals)

    def write_call(self, name, nArgs):
        self.vm_table.append('call ' + name + ' ' + nArgs)

    def write_return(self):
        self.vm_table.append('return')

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


class SymbolTable:
    def __init__(self):
        self.class_table = []
        self.subroutine_table = []

        self.count_STATIC = 0
        self.count_FIELD = 0
        self.count_ARG = 0
        self.count_VAR = 0

    def start_subroutine(self, mode='', f_class_entry=''):
        if mode == 'print':
            print('Subroutine-Table------------------------------------------------------')
            [print(table_entry) for table_entry in self.subroutine_table]
        self.subroutine_table = []
        self.define(f_class_entry[0], f_class_entry[1], f_class_entry[2])

    def define(self, f_name, f_type, f_kind):
        if f_kind == '<keyword> static </keyword>':
            self.class_table.append((f_name, f_type, f_kind, self.count_STATIC))
            self.count_STATIC += 1
        elif f_kind == '<keyword> field </keyword>':
            self.class_table.append((f_name, f_type, f_kind, self.count_FIELD))
            self.count_FIELD += 1
        elif f_kind == 'ARGUMENT':   # Special Case: the word argument is hard-coded
            self.subroutine_table.append((f_name, f_type, f_kind, self.count_ARG))
            self.count_ARG += 1
        elif f_kind == '<keyword> var </keyword>':
            self.subroutine_table.append((f_name, f_type, f_kind, self.count_VAR))
            self.count_VAR += 1

    def var_count(self, f_kind):
        if f_kind == '<keyword> static </keyword>':
            return self.count_STATIC
        elif f_kind == '<keyword> field </keyword>':
            return self.count_FIELD
        elif f_kind == 'ARGUMENT':
            return self.count_ARG
        elif f_kind == '<keyword> var </keyword>':
            return self.count_VAR

    def kind_of(self, f_name):
        # Checks the subroutine table if the variable name is in there
        for entry in self.subroutine_table:
            if entry[0] == f_name:
                return entry[2]

        # Checks the class table if the variable name is in there
        for entry in self.class_table:
            if entry[0] == f_name:
                return entry[2]

        # the variable is not found or not in the current scope
        return 'NONE'

    def type_of(self, f_name):
        # Checks the subroutine table if the variable name is in there
        for entry in self.subroutine_table:
            if entry[0] == f_name:
                return entry[1]

        # Checks the class table if the variable name is in there
        for entry in self.class_table:
            if entry[0] == f_name:
                return entry[1]

        # the variable is not found or not in the current scope
        return 'NONE'

    def index_of(self, f_name):
        # Checks the subroutine table if the variable name is in there
        for entry in self.subroutine_table:
            if entry[0] == f_name:
                return entry[3]

        # Checks the class table if the variable name is in there
        for entry in self.class_table:
            if entry[0] == f_name:
                return entry[3]

        # the variable is not found or not in the current scope
        return 'NONE'

    def print_class_tables(self):
        print('Class-Table-----------------------------------------------------------')
        [print(table_entry) for table_entry in self.class_table]
        print('Subroutine-Table------------------------------------------------------')
        [print(table_entry) for table_entry in self.subroutine_table]

    def is_var_defined(self, f_name):
        # Checks the subroutine table if the variable name is in there
        for entry in self.subroutine_table:
            if entry[0] == f_name:
                return True

        # Checks the class table if the variable name is in there
        for entry in self.class_table:
            if entry[0] == f_name:
                return True

        return False


def symbol_table_tester():
    sym = SymbolTable()
    sym.define('nAccounts', 'int', '<keyword> static </keyword>')
    sym.define('id', 'int', '<keyword> field </keyword>')
    sym.define('name', 'String', '<keyword> field </keyword>')
    sym.define('balance', 'int', '<keyword> field </keyword>')
    sym.define('this', 'BankAccount', 'ARGUMENT')
    sym.define('due', 'Date', '<keyword> var </keyword>')
    sym.print_class_tables()
    print(sym.var_count('<keyword> field </keyword>'))
    print(sym.var_count('<keyword> var </keyword>'))
    print(sym.type_of('<keyword> static </keyword>'))
    print(sym.index_of('name'))
    print(sym.index_of('balance'))

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
    for tuple_element in jack_arrays:
        token_array = JackTokenizer(tuple_element)
        token_tuple_array.append(token_array.get_token_filename_tuple())

    jack_array = JackCompiler(token_tuple_array[0])
    jack_array.make_jack_file()

#jack_translate()
jack_tester()
