import os
import glob

folder_directory = "C:/Users/Paul/Documents/Open Source Society for Computer Science (OSSU)/nand2tetris/projects/11/CompileFolder/ComplexArrays"
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
            print(line)
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
            string_element = ""
            while not self.current_token == '"':
                string_element += self.current_token
                self.advance()
            self.token_array.append('<stringConstant> ' + string_element + ' </stringConstant>')

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
        self.subroutine_type = 'placeholder'
        self.subroutine_output = 'placeholder'
        self.var_names = []
        self.class_name = ''
        self.vm_table = []
        self.symbol_table = SymbolTable()

        self.field_count = 0
        self.while_count = -1
        self.while_count_start = -1
        self.while_count_end = -1
        self.if_count = -1
        self.if_count_true = -1
        self.if_count_false = -1
        self.expression_array_stage = 0

        # Starts the compilation and makes sure the first token is a class
        if self.has_more_tokens():
            self.advance()
            if self.current_token == '<keyword> class </keyword>':
                self.compile_class()
            else:
                print("ERROR!!! A jack compiler must always have a class as it's first token!!!")
        self.symbol_table.print_class_tables()

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
            if self.current_token == '<keyword> field </keyword>':
                self.compile_class_var_dec(sc, True)
            else:
                self.compile_class_var_dec(sc, False)

        # subroutineDec: <subroutineDec> some words </subroutineDec> THIS CAN REPEAT
        while self.check_token(1, '<keyword> constructor </keyword>', '<keyword> function </keyword>',
                               '<keyword> method </keyword>'):
            self.advance()
            if self.current_token == '<keyword> constructor </keyword>':
                self.compile_subroutine(sc, self.field_count)
            elif self.current_token == '<keyword> method </keyword>':
                self.compile_subroutine(sc, 0, True)
            else:
                self.compile_subroutine(sc)


        # } <symbol> } </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        self.jack_array.append('</class>')
        # end of Class --------------------------------------------------------------------

    def compile_class_var_dec(self, c_sc, is_Field=False):
        # VM table field_count

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

        # Field Count increase
        if is_Field:
            self.field_count += 1

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

            # Field Count increase
            self.field_count += 1
            self.symbol_table.define(sym_name, sym_type, sym_kind)

        # ;
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        self.jack_array.append(' ' * c_sc + '</classVarDec>')

        # End of ClassVarDec-------------------------------------------------------------

    def compile_subroutine(self, c_sc, field_count=0, is_method=False):
        # VM Code Counts
        self.while_count_start = -1
        self.while_count_end = -1
        self.if_count = -1
        self.if_count_true = -1
        self.if_count_false = -1

        # c_sc is the caller's space_counter
        self.jack_array.append(' ' * c_sc + '<subroutineDec>')  # <SubroutineDec>
        sc = c_sc + 2
        # Holds if function is void or have a return value
        function_type = 'placeholder'
        # Holds the number of local variable count
        local_variable_count = 0

        # Construction|Function|Method: <keyword> function </keyword>
        self.jack_array.append(' ' * sc + self.current_token)
        self.subroutine_type = self.current_token
        # If it the subroutine is a method therefore an argument 0 called "this" must be automatically put
        if self.current_token == '<keyword> method </keyword>':
            self.symbol_table.start_subroutine('', ('<keyword> this </keyword>', self.class_name, 'ARGUMENT'), True)
        else:
            self.symbol_table.start_subroutine('', ('<keyword> this </keyword>', self.class_name, 'ARGUMENT'), False)

        # void | Type: <keyword> void </keyword>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)
        self.subroutine_output = self.current_token

        # subroutineName: <identifier> main </identifier> SymbolTable Entry No need but restart subroutine table
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # VM Translation
        # Set the variable for the VM translator function after counting the number of local argument at the var dec
        f_class_name = self.class_name[13:-14]
        f_class_subroutine = self.current_token[13:-14]

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
            local_variable_count += self.compile_var_dec(i_sc)

        self.write_function(f_class_name + '.' + f_class_subroutine, str(local_variable_count))

        # If there are fields this translates it properly to the symbol table
        if field_count > 0:
            self.write_push('CONST', str(field_count))
            self.write_call('Memory.alloc', '1')
            self.write_pop('POINTER', '0')

        if is_method:
            self.write_push('ARGUMENT', '0')
            self.write_pop('POINTER', '0')

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
        local_variable_count = 0

        # 'var': <keyword> var </keyword>
        self.jack_array.append(' ' * sc + self.current_token)
        # SymbolTable Input: Kind
        sym_kind = 'LOCAL'
        #print(sym_kind)

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
        local_variable_count += 1

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
            local_variable_count += 1

        # ; <symbol> ; </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        self.jack_array.append(' ' * c_sc + '</varDec>')  # </varDec>
        return local_variable_count
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
            if self.subroutine_output == '<keyword> void </keyword>':
                self.write_push('CONST', '0')
            self.compile_return_statement(c_sc)

        # Check if the statement is an if statement
        elif self.current_token == '<keyword> if </keyword>':
            self.compile_if_statement(c_sc)

        # Check if the statement is a while statement
        elif self.current_token == '<keyword> while </keyword>':
            self.compile_while_statement(c_sc)

    def compile_let_statement(self, c_sc):
        # Initialize truth value for array (default is false)
        is_array = False

        self.jack_array.append(' ' * c_sc + '<letStatement>')  # <Statements: letStatement>
        sc = c_sc + 2
        symbol_index = 'PLACEHOLDER'

        # 'let': '<keyword> let </keyword>'
        self.jack_array.append(' ' * sc + self.current_token)

        # varName SymbolTable Output
        self.advance()

        # <identifier>----------------------------------------------------
        # varName REPLACE THIS WITH SEARCHING THE VM TABLE
        if self.symbol_table.is_var_defined(self.current_token):
            self.jack_array.append(' ' * sc + self.current_token)

            # Get the varName VM TRANSLATION
            if not self.symbol_table.index_of(self.current_token) == 'NONE':
                symbol_type = self.symbol_table.kind_of(self.current_token)
                symbol_index = str(self.symbol_table.index_of(self.current_token))

        # </identifier> -------------------------------------------------

        # check if it has [expression]-----------------------------------
        if self.check_token(1, "<symbol> [ </symbol>"):
            # Initialize variable for array VM table
            var_token = self.current_token
            var_index = str(self.symbol_table.index_of(var_token))
            var_kind = self.symbol_table.kind_of(var_token)
            is_array = True

            # [ : <symbol> [ </symbol>
            self.advance()
            self.jack_array.append(' ' * sc + self.current_token)

            # Expression
            self.advance()
            self.compile_expression(sc)

            # ] : <symbol> ] </symbol>
            self.advance()
            self.jack_array.append(' ' * sc + self.current_token)

            # Push the array variable
            # Special case for THIS
            if self.current_token == '<keyword> this </keyword>':
                #  token_holder.append(('<POINTER>', '0'))
                self.write_call('POINTER ERROR CHECK THE EXPRESSION FOR LET STATEMENT THE SPECIAL CASE FOR THIS')
            else:
                self.write_push(var_kind, var_index)
            self.write_arithmetic('ADD')
        # -------------------------------------------------------------

        # = : <symbol> = </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # expression
        self.advance()
        self.compile_expression(sc)
        # If it is an array follow simon's advice
        if is_array:
            self.write_pop('TEMP', '0')
            self.write_pop('POINTER', '1')
            self.write_push('TEMP', '0')
            self.write_pop('THAT', '0')

        # ; : <symbol> ; </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        self.jack_array.append(' ' * c_sc + '</letStatement>')  # <Statements>

        # Start of VM translation if it is an array the local push is already handled by the Expression part(?) yeah it kindda confusing
        if not symbol_index == 'PLACEHOLDER' and not is_array:
            self.write_pop(symbol_type, symbol_index)
        # end of Let Statement-----------------------------------

    # Wait lagpas ka na pala doon :/

    def compile_if_statement(self, c_sc=0):
        # If counter IT REPEATS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.if_count += 1
        if_count = self.if_count

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

        # if statement is True
        # Command on where to go if statement is true
        self.write_if('IF_TRUE' + str(if_count))
        # Command on where to go if statement is false
        self.if_count_false += 1
        self.write_goto('IF_FALSE' + str(if_count))

        # True Statement
        self.write_label('IF_TRUE' + str(if_count))

        # statements
        self.advance()
        self.compile_statements(sc)

        # } : <symbol> } </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # Check if there is an Else Statement
        if self.check_token(1, '<keyword> else </keyword>'):

            self.write_goto('IF_END' + str(if_count))
            # end of the True statement

            # False Statement
            self.write_label('IF_FALSE' + str(if_count))

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

            self.write_label('IF_END' + str(if_count))
            # End of Else Statement
        else:
            self.write_label('IF_FALSE' + str(if_count))

        self.jack_array.append(' ' * c_sc + '</ifStatement>')
        # end of ifStatement----------------------------------------------

    def compile_while_statement(self, c_sc=0):
        self.jack_array.append(' ' * c_sc + '<whileStatement>')  # <Statements: whileStatement>
        sc = c_sc + 2
        # While counter
        self.while_count_start += 1
        self.while_count_end += 1

        while_var_start = self.while_count_start
        while_var_end = self.while_count_end

        # Start of VM Translation
        # Label
        while_start_label = 'WHILE_EXP' + str(self.while_count_start)
        self.write_label(while_start_label)

        # while keyword <keyword> while </keyword>
        self.jack_array.append(' ' * sc + self.current_token)

        # ( : <symbol> ( </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # expression THe boolean statement to determine if to loop or not
        self.advance()
        self.compile_expression(sc)

        # VM Translation: As per instruction the condition must always be negated
        self.write_arithmetic('NOT')

        # ) : <symbol> ) </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # { : <symbol> { </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # Checks the boolean obtained before Then if it is false loop if true end loop (yeah it's kindda reverse)
        while_end_label = 'WHILE_END' + str(self.while_count_start)
        self.write_if(while_end_label)

        # statements
        self.advance()
        self.compile_statements(sc)

        # } <symbol> } </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        # The end of while statement will always go back the start of the while statement for checking for the loop again
        self.write_goto('WHILE_EXP' + str(while_var_start))
        self.write_label('WHILE_END' + str(while_var_start))

        self.jack_array.append(' ' * c_sc + '</whileStatement>')  # <EndOfStatements: whileStatement>
        # End of While Statement------------------------------------------------------------------------------

    def compile_do_statement(self, c_sc=0):
        self.jack_array.append(' ' * c_sc + '<doStatement>')  # <Statements: doStatement>
        sc = c_sc + 2

        # do: '<keyword> do </keyword>'
        self.jack_array.append(' ' * sc + self.current_token)

        # Subroutine Call:
        self.advance()
        sub_tuple = self.og_compile_subroutine_call(sc)

        # ; : <symbol> ; </symbol>
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        self.jack_array.append(' ' * c_sc + '</doStatement>')  # <Statements: doStatement>

        # VM STATEMENT the call function for do can just be declared here: no need for expression to handle it
        # This finishes the VM translation of og_compile subroutine
        if not sub_tuple is None:
            if sub_tuple[2][0:12] == '<identifier>':
                adj_index = str(int(sub_tuple[1]) + 1)
                self.write_call(sub_tuple[0], adj_index)
            else:
                self.write_call(sub_tuple[0], sub_tuple[1])

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
            # If it is a constructor it must always push pointer zero as a return value
            if self.current_token == '<keyword> this </keyword>':
                self.write_push('POINTER', '0')
            self.compile_expression(sc)

        # ; <symbol> ; </symbol>'
        self.advance()
        self.jack_array.append(' ' * sc + self.current_token)

        self.jack_array.append(' ' * c_sc + '</returnStatement>')  # </Statements: /returnStatement>

        # VM translation
        self.write_return()

        # End of return Statement---------------------------------------

    def call_expression_list(self, c_sc, subroutine_name='', master_level=True):
        # Holds the exp_count coming from expression_list
        exp_count_holder = 0

        if self.check_token(1, '<symbol> ) </symbol>'):
            exp_count_holder = self.compile_expression_list(c_sc, subroutine_name, master_level)
        else:
            self.advance()
            exp_count_holder = self.compile_expression_list(c_sc, subroutine_name, master_level)

        return str(exp_count_holder)

    def compile_expression_list(self, c_sc=0, subroutine_name='', master_level=True):
        self.jack_array.append(' ' * c_sc + '<expressionList>')  # <expressionList>
        sc = c_sc + 2

        # Counter for the number of expressions
        exp_count = 0

        # The caller of this method is always choosing between entering '(' or the expression
        # token itself. When current token is ( then there is no expression


        # There is an expression
        # NOte this expression list stands for f(exp1, exp2, exp3, etc)
        if not self.check_token(0, '<symbol> ( </symbol>') or not self.check_token(1, '<symbol> ) </symbol>'):
            # expression Initial
            self.compile_expression(sc, master_level)
            exp_count += 1

            # expression recursion
            while self.check_token(1, '<symbol> , </symbol>'):
                # , : <symbol> , </symbol>
                self.advance()
                self.jack_array.append(' ' * sc + self.current_token)

                # expression
                self.advance()
                self.compile_expression(sc, master_level)
                exp_count += 1

        # End of expression List
        self.jack_array.append(' ' * c_sc + '</expressionList>')  # </expressionList>

        return exp_count
        # End of Expression List-----------------------------------------------------------

    # Master level means it is not coming from term but it is an expression of itself
    def compile_expression(self, c_sc, master_level=True):
        self.jack_array.append(' ' * c_sc + '<expression>')  # <Expression>
        sc = c_sc + 2

        expression_beginning = len(self.jack_array) - 1

        # term : compile term: Note term calling expression will have master_level set to false
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
        # If the current expression is master level then vm translation can be used
        if master_level:
            initialize_array = self.expression_array_vm_initialize(self.jack_array[expression_beginning:])
            print('--------------------------------------------------------')
            print(initialize_array)
            self.expression_vm_translator(initialize_array)
        # counting from other expression calls in the bigger picture

    def expression_array_vm_initialize(self, jack_array):
        """Initialize the expression section of the token xml file for vm translation"""
        token_holder = []
        array_variable = False
     #   print(jack_array)
        # This is where the filtering happens wherein unnecessary tags are ignored
        for i, element in enumerate(jack_array):
            current_expression = element.strip()
            if element.strip() == '<expression>':
                token_holder.append((current_expression, 'n/a'))

            elif element.strip() == '</expression>':
                token_holder.append((current_expression, 'n/a'))

            elif element.strip() == '<expressionList>':
                token_holder.append((current_expression, 'n/a'))

            elif element.strip() == '</expressionList>':
                token_holder.append((current_expression, 'n/a'))

            elif element.strip()[0:17] == '<integerConstant>':
                token_holder.append((current_expression[0:17], current_expression[18:-19]))

            elif element.strip() == '<symbol> + </symbol>':
                token_holder.append((current_expression[0:8], current_expression[9:-10]))

            elif element.strip() == '<symbol> - </symbol>':
                token_holder.append((current_expression[0:8], current_expression[9:-10]))

            elif element.strip() == '<symbol> * </symbol>':
                token_holder.append((current_expression[0:8], current_expression[9:-10]))

            elif element.strip() == '<symbol> / </symbol>':
                token_holder.append((current_expression[0:8], current_expression[9:-10]))

            elif element.strip() == '<symbol> ~ </symbol>':
                token_holder.append((current_expression[0:8], current_expression[9:-10]))

            elif element.strip() == '<symbol> , </symbol>':
                token_holder.append((current_expression[0:8], current_expression[9:-10]))

            elif element.strip() == '<symbol> | </symbol>':
                token_holder.append((current_expression[0:8], current_expression[9:-10]))

            elif element.strip() == '<symbol> &gt; </symbol>':
                token_holder.append((current_expression[0:8], current_expression[9:-10]))

            elif element.strip() == '<symbol> &lt; </symbol>':
                token_holder.append((current_expression[0:8], current_expression[9:-10]))

            elif element.strip() == '<symbol> = </symbol>':
                token_holder.append((current_expression[0:8], current_expression[9:-10]))

            elif element.strip() == '<symbol> &amp; </symbol>':
                token_holder.append((current_expression[0:8], current_expression[9:-10]))

            elif element.strip() == '<keyword> null </keyword>':
                # null pretty much means constant 0
                token_holder.append(('<integerConstant>', '0'))

            elif element.strip() == '<keyword> true </keyword>':
                # If true the VM translator will add a not command after pushing constant 0
                token_holder.append(('<boolean>', 'true'))

            elif element.strip() == '<keyword> false </keyword>':
                # If false the VM translator will never add a not command after pushing constant 0
                token_holder.append(('<boolean>', 'false'))

            elif element.strip()[0:16] == '<stringConstant>':
                token_holder.append(('<stringConstant>', element.strip()[17:-18]))

            # Subroutine Call Memory.peek(
            elif element.strip()[0:12] == '<identifier>' and jack_array[i+1].strip() == '<symbol> . </symbol>' and jack_array[i+2].strip()[0:12] == '<identifier>' :
                if self.symbol_table.is_var_defined(element.strip()):
                    subroutine_name = self.symbol_table.type_of(element.strip())[13:-14] + '.' + jack_array[i + 2].strip()[13:-14]
                    token_holder.append(('<fieldFunction>', subroutine_name))
                else:
                    subroutine_name = element.strip()[13:-14] + '.' + jack_array[i+2].strip()[13:-14]
                    token_holder.append(('<function>', subroutine_name))

            # Expression is a variable to TUESDAY PAUL: VERIFY IF THE LOGIC HERE IS CORRECT VIA TEST CASES AND LECTURE
            elif self.symbol_table.is_var_defined(element.strip()):
                var_index = str(self.symbol_table.index_of(element.strip()))
                var_kind = self.symbol_table.kind_of(element.strip())
                # Special case for THIS
                if element.strip() == '<keyword> this </keyword>':
                    token_holder.append(('<POINTER>', '0'))
                else:
                    token_holder.append((var_kind, var_index))
                    if jack_array[i+1].strip() == '<symbol> [ </symbol>':
                        array_variable = True
                        self.expression_array_stage += 1

            # array variable handling
            if array_variable:
                if element.strip() == '<symbol> [ </symbol>':
                    token_holder.append(('ARRAY', 'BEGIN'))
                elif element.strip() == '<symbol> ] </symbol>':
                    token_holder.append(('ARRAY', 'END'))
                    self.expression_array_stage -= 1
                    if self.expression_array_stage <= 0:
                        array_variable = False

        return token_holder

    def expression_vm_translator(self, exp_arr, arr_ind=0):
        """The official VM translator for Expressions"""

        def is_symbol_operator(exp_tpl):
            if (exp_tpl == ('<symbol>', '=') or exp_tpl == ('<symbol>', '+') or exp_tpl == ('<symbol>', '-') or
                exp_tpl == ('<symbol>', '*') or exp_tpl == ('<symbol>', '/') or exp_tpl == ('<symbol>', '~') or
                exp_tpl == ('<symbol>', '|') or exp_tpl == ('<symbol>', '&gt;') or exp_tpl == ('<symbol>', '&lt;') or exp_tpl == ('<symbol>', '&amp;')):
                return True
            else:
                return False

        def evaluate_operator(op, neg=False):
            if op == '+':
                self.write_arithmetic('ADD')
            elif op == '-' and neg:
                self.write_arithmetic('NEG')
            elif op == '-' and not neg:
                self.write_arithmetic('SUB')
            elif op == '~':
                self.write_arithmetic('NOT')
            elif op == '&gt;':
                 self.write_arithmetic('GT')
            elif op == '&lt;':
                 self.write_arithmetic('LT')
            elif op == '|':
                self.write_arithmetic('OR')
            elif op == '&amp;':
                self.write_arithmetic('AND')
            elif op == '=':
                self.write_arithmetic('EQ')
            elif op == '*':
                self.write_call('Math.multiply', '2')
            elif op == '/':
                self.write_call('Math.divide', '2')

        if len(exp_arr) <= 3:
            # Expression is a Number
            if exp_arr[arr_ind][0] == '<expression>' and exp_arr[arr_ind+1][0] == '<integerConstant>' and exp_arr[arr_ind+2][0] == '</expression>':
                self.write_push('CONST', exp_arr[1][1])

                # Evaluate the expression if a symbol is attached to it
                op1 = exp_arr[0][1]
                evaluate_operator(op1)
                # !!! DOUBLE CHECK THIS

            # Expression is a POINTER
            elif exp_arr[arr_ind][0] == '<expression>' and exp_arr[arr_ind+1][0] == '<POINTER>' and exp_arr[arr_ind+2][0] == '</expression>':
                self.write_push('POINTER', exp_arr[1][1])

            # Expression is a FIELD
            elif exp_arr[arr_ind][0] == '<expression>' and exp_arr[arr_ind+1][0] == '<keyword> field </keyword>' and exp_arr[arr_ind+2][0] == '</expression>':
                # This should be '<keyword< field... DON'T CHANGE THIS SO THAT IT WILL BE CONSISTENT WITH THE SYMBOL TABLE
                self.write_push('<keyword> field </keyword>', exp_arr[1][1])

            # Expression is Local variable
            elif exp_arr[arr_ind][0] == '<expression>' and exp_arr[arr_ind+1][0] == 'LOCAL' and exp_arr[arr_ind+2][0] == '</expression>':
                self.write_push('LOCAL', exp_arr[arr_ind + 1][1])

                # Evaluate the expression if a symbol is attached to it
                op1 = exp_arr[0][1]
                evaluate_operator(op1)
                # !!! DOUBLE CHECK THIS

            # Expression is Argument variable
            elif exp_arr[arr_ind][0] == '<expression>' and exp_arr[arr_ind+1][0] == 'ARGUMENT' and exp_arr[arr_ind+2][0] == '</expression>':
                self.write_push('ARGUMENT', exp_arr[arr_ind + 1][1])

            # Expression is a Static Variable: Yeah the <keyword> is required
            elif exp_arr[arr_ind][0] == '<expression>' and exp_arr[arr_ind+1][0] == '<keyword> static </keyword>' and exp_arr[arr_ind+2][0] == '</expression>':
                self.write_push('<keyword> static </keyword>', exp_arr[1][1])

            # Expression is a Boolean
            elif exp_arr[arr_ind][0] == '<expression>' and exp_arr[arr_ind+1][0] == '<boolean>' and exp_arr[arr_ind+2][0] == '</expression>':
                if exp_arr[arr_ind+1][1] == 'true':
                    self.write_push('CONST', '0')
                    self.write_arithmetic('NOT')
                else:
                    self.write_push('CONST', '0')

            # Expression is a string
            elif exp_arr[arr_ind][0] == '<expression>' and exp_arr[arr_ind+1][0] == '<stringConstant>' and exp_arr[arr_ind+2][0] == '</expression>':
                string_exp = exp_arr[arr_ind+1][1]
                string_length = str(len(string_exp))
                self.write_push('CONST', string_length)
                self.write_call('String.new', '1')
                # Convert the characters to ASCII
                for str_char in string_exp:
                    self.write_push('CONST', str(ord(str_char)))
                    self.write_call('String.appendChar', '2')

            # Expression is just an operator
            elif exp_arr[arr_ind][0] == '<expression>' and (not exp_arr[arr_ind][1] == 'n/a') and exp_arr[arr_ind+1] == ('</expression>', 'n/a'):
                evaluate_operator(exp_arr[arr_ind][1])

        # Expression is Exp1 Op Exp2
        elif len(exp_arr) > 3:

            # Expression is compounded like: (~(position > 16)): Exp1 Exp2
            if exp_arr[arr_ind][0] == '<expression>' and exp_arr[arr_ind+1][0] == '<expression>':
                print('full exp----------------------------')
                print(exp_arr)

                temp = exp_arr[1:-1]
                end_of_inner_exp = len(temp)
                exp_counter = 0
                for i, e in enumerate(temp):
                    if e[0] == '<expression>':
                        exp_counter += 1
                    elif e[0] == '</expression>':
                        exp_counter -= 1
                        if exp_counter <= 0:
                            end_of_inner_exp = i
                            break

                inner_exp = [exp_arr[0]] + temp[arr_ind+1:end_of_inner_exp+1]
                print('inner exp--------------------------')
                print(inner_exp)
                self.expression_vm_translator(inner_exp)

                outer_exp = [exp_arr[0]] + temp[end_of_inner_exp+1:] + [exp_arr[len(exp_arr)-1]]
                print('outer exp--------------------------')
                print(outer_exp)

                # A case wherein the first token is a symbol operator
                if len(outer_exp) > 1:
                    if is_symbol_operator(outer_exp[1]):
                        print('inner_exp2-------------------------')
                        inner_exp2 = [('<expression>', outer_exp[1][1])] + outer_exp[2:]
                        print(inner_exp2)
                        self.expression_vm_translator(inner_exp2)

                    else:
                        self.expression_vm_translator(outer_exp)

                    # [('<expression>', 'n/a'), ('<integerConstant>', '254'), ('</expression>', 'n/a'), LESS THAN MUST COME BEFORE &AMP end_of_inner_exp = exp_arr.index(('</expression>', 'n/a'))

            # Exp is an array
            elif exp_arr[arr_ind+1][0] == 'LOCAL' and exp_arr[arr_ind+2] == ('ARRAY', 'BEGIN'):
                array_end = len(exp_arr)
                array_counter = 0
                for i, e in enumerate(exp_arr):
                    if e == ('ARRAY', 'BEGIN'):
                        array_counter += 1
                    elif e == ('ARRAY', 'END'):
                        array_counter -= 1
                        if array_counter <= 0:
                            array_end = i
                            break

                inner_exp = exp_arr[arr_ind+3:array_end]
                print('inner_exp------------')
                print(inner_exp)
                self.expression_vm_translator(inner_exp)
                # PUSH LOCAL 1 the array variable
                self.write_push(exp_arr[arr_ind+1][0], exp_arr[arr_ind+1][1])

                evaluate_operator('+')

                # Simon's Says tips
                self.write_pop('POINTER', '1')
                self.write_push('THAT', '0')

                if array_end + 2 < len(exp_arr):
                    exp_epilogue = exp_arr[array_end+1]
                    if exp_epilogue[0] == '<symbol>':
                        outer_exp = [('<expression>', exp_epilogue[1])] + exp_arr[array_end+2:]
                        print('outer_exp-------------------------------------------')
                        print(outer_exp)

                        self.expression_vm_translator(outer_exp)

                else:
                    evaluate_operator(exp_arr[0][1])

                # Check this on Tuesday and EXTEND

            # Exp1 Op Compound_Exp2: For cases like: 2 + (1 - 43)
            # exp_arr[arr_ind + 1] is usually the integerConstant
            elif (exp_arr[arr_ind][0] == '<expression>' and exp_arr[arr_ind+2][0] == '<symbol>' and
                  (exp_arr[arr_ind+3][0] == '<expression>' or exp_arr[arr_ind+3] == ('<symbol>', '-') or
                   (exp_arr[arr_ind+3][0] == 'LOCAL' and exp_arr[arr_ind+4] == ('ARRAY', 'BEGIN')))):

                # Expression 1
                exp1 = exp_arr[arr_ind:2]  # :2 is the symbol
                exp1.append(('</expression>', 'n/a'))
                self.expression_vm_translator(exp1)

                # Expression 2 is an expression
                if exp_arr[arr_ind+3][0] == '<expression>':
                    compound_exp2 = exp_arr[arr_ind+3:-1]
                    print(compound_exp2)
                    self.expression_vm_translator(compound_exp2)

                elif exp_arr[arr_ind+3] == ('<symbol>', '-'):
                    compound_exp2 = [('<expression>', 'n/a')] + exp_arr[arr_ind+3:-1] + [('</expression>', 'n/a')]
                    print(compound_exp2)
                    self.expression_vm_translator(compound_exp2)

                # or an array
                elif exp_arr[arr_ind+3][0] == 'LOCAL' and exp_arr[arr_ind+4] == ('ARRAY', 'BEGIN'):
                    compound_exp2 = [('<expression>', 'n/a')] + exp_arr[arr_ind+3:-1] + [('</expression>', 'n/a')]
                    print(compound_exp2)
                    self.expression_vm_translator(compound_exp2)

                # output "op"
                op = exp_arr[arr_ind + 2][1]
                evaluate_operator(op)

            # Compound_Exp1 Op Compound_Exp2:
            # exp_arr[arr_ind + 1] is usually the integerConstant
            elif (exp_arr[arr_ind][0] == '<expression>' and exp_arr[arr_ind + 2][0] == '</expression>' and
                    exp_arr[arr_ind + 3] == ('<symbol>', '&amp;')):
                print('byeeeee')
                # Expression 1
                exp1 = exp_arr[arr_ind:2]  # :2 is the symbol
                exp1.append(('</expression>', exp_arr[0][1]))
                self.expression_vm_translator(exp1)

                # Expression 2 is an expression
                if exp_arr[arr_ind + 4][0] == '<expression>':
                    compound_exp2 = exp_arr[arr_ind + 4:-1]
                    self.expression_vm_translator(compound_exp2)

                elif exp_arr[arr_ind + 4] == ('<symbol>', '-'):
                    compound_exp2 = [('<expression>', 'n/a')] + exp_arr[arr_ind + 4:-1] + [('</expression>', 'n/a')]
                    self.expression_vm_translator(compound_exp2)

                # output "op"
                op = exp_arr[arr_ind + 3][1]
                evaluate_operator(op)

        # Exp1 Op Exp2
            # Mathematical Operation: exp_arr[arr_ind + 1] is usually the integerConstant and arr_ind+3 also:
            elif exp_arr[arr_ind][0] == '<expression>' and is_symbol_operator(exp_arr[arr_ind+2]) and exp_arr[arr_ind+4][0] == '</expression>':
                # Expression 1
                exp1 = [('<expression>', 'n/a')] + exp_arr[arr_ind+1:2] + [('</expression>', 'n/a')]
                print(exp1)
                self.expression_vm_translator(exp1)

                # Expression 2
                exp2 = [('<expression>', 'n/a')] + exp_arr[arr_ind + 3:]
                self.expression_vm_translator(exp2)

                # output 'op'
                op = exp_arr[arr_ind + 2][1]
                evaluate_operator(op)

            # Logical Operator
            elif exp_arr[arr_ind][0] == '<expression>' and exp_arr[arr_ind+2] == ('<symbol>', '&amp;'):
                # Expression 1
                exp1 = exp_arr[arr_ind:2] + [('</expression>', 'n/a')]
                self.expression_vm_translator(exp1)

                # Expression 2
                exp2 = [('<expression>', 'n/a')] + exp_arr[arr_ind + 3:]
                self.expression_vm_translator(exp2)

                # output 'op'
                op = exp_arr[arr_ind + 2][1]
                evaluate_operator(op)

            # Expression is Compound: Op (~) Exp or Op (-) Exp
            elif (exp_arr[arr_ind + 1] == ('<symbol>', '~') or exp_arr[arr_ind + 1] == ('<symbol>', '-')) and exp_arr[arr_ind + 2][0] == '<expression>':
                # Expression
                exp = exp_arr[arr_ind + 2:-1]
                self.expression_vm_translator(exp)

                # output 'op'
                op = exp_arr[arr_ind+1][1]

                evaluate_operator(op, True)

            # Expression is Op IntegerExpression/LocalVariable/FieldVariable
            elif is_symbol_operator(exp_arr[arr_ind + 1]) and \
                    (exp_arr[arr_ind + 2][0] == '<integerConstant>' or exp_arr[arr_ind + 2][0] == 'LOCAL' or '<keyword> field </keyword>'): #and exp_arr[arr_ind + 3][0] == '</expression>':
                # Expression
                exp1 = [('<expression>', 'n/a')] + [exp_arr[arr_ind + 2]] + [('</expression>', 'n/a')]
                self.expression_vm_translator(exp1)

                # output 'op'
                op = exp_arr[arr_ind+1][1]
                evaluate_operator(op, True)

                # If the right side is an integer expression
                if exp_arr[arr_ind+3][0] == '<symbol>' and exp_arr[arr_ind+4][0] == '<integerConstant>':
                    exp2 = [('<expression>', 'n/a')] + exp_arr[arr_ind + 4:]
                    self.expression_vm_translator(exp2)

                # output 'op'
                op = exp_arr[arr_ind+3][1]
                evaluate_operator(op)

            # Expression is an and function or a FieldFunction logical operator to something
            elif exp_arr[arr_ind][0] == '<expression>' and (exp_arr[arr_ind + 1][0] == '<function>' or exp_arr[arr_ind + 1][0] == '<fieldFunction>'):
                if exp_arr[arr_ind + 2][0] == '<expressionList>':
                    end_of_exp = exp_arr[arr_ind+2:].index(('</expressionList>', 'n/a')) + 2
                    exp = exp_arr[arr_ind+2:end_of_exp+1]

                    self.expression_vm_translator(exp)

                    # Count the number of list and see if "this" needs to be included
                    if exp_arr[arr_ind + 1][0] == '<fieldFunction>':
                        exp_count = exp.count(('<expression>', 'n/a')) + 1
                    else:
                        exp_count = exp.count(('<expression>', 'n/a'))

                    self.write_call(exp_arr[1][1], str(exp_count))

                    # Evaluate the expression if a symbol is attached to it
                    op1 = exp_arr[0][1]
                    evaluate_operator(op1)
                    # !!! DOUBLE CHECK THIS

            # Expression is Exp, Exp, Exp,....
            elif exp_arr[arr_ind][0] == '<expressionList>' and exp_arr[-1][0] == '</expressionList>':
                exp = exp_arr[1:-1]
                if ('<symbol>', ',') in exp:
                    comma_index = exp.index(('<symbol>', ','))
                    exp1 = exp[0:comma_index]
                    exp2 = exp[comma_index + 1:]
                    multi_exp = True
                else:
                    exp1 = exp
                    multi_exp = False

                self.expression_vm_translator(exp1)

                if multi_exp:
                    if ('<symbol>', ',') in exp2:
                        exp2 = [('<expressionList>', 'n/a')] + exp2 + [('</expressionList>', 'n/a')]
                        self.expression_vm_translator(exp2)
                    else:
                        self.expression_vm_translator(exp2)
                        multi_exp = False


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
                self.compile_expression(sc, False)

                # ] : <symbol> ] </symbol>
                self.advance()
                self.jack_array.append(' ' * sc + self.current_token)

        # the term is a SubroutineCall: Current token is varName or className under SubroutineCall
        # (className|varName).SubroutineName(expressionList) or it can be a subroutineName(ExpressionList)
        elif (self.symbol_table.is_var_defined(self.current_token) or self.check_token(1, '<symbol> . </symbol>')
              or (self.current_token[0:12] == '<identifier>' and self.check_token(1, '<symbol> ( </symbol>'))):
            self.og_compile_subroutine_call(sc, False)

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
        subroutine_type = ''

        # VM translation beginning checkpoint
        if master_level:
            subroutine_call_beginning = len(self.jack_array) - 1

        # SubroutineName
        self.jack_array.append(' ' * c_sc + self.current_token)

        # Temporary solution: The VM translator checks if the subroutine name is a variable in the symbol table
        # The vm transltor will push the variable from the symbol table and call
        s_table_kind = self.symbol_table.kind_of(self.current_token)
        s_table_index = str(self.symbol_table.index_of(self.current_token))
        s_table_type = self.symbol_table.type_of(self.current_token)
        subroutine_type = s_table_type
        if not s_table_kind == 'NONE':
            self.write_push(s_table_kind, s_table_index)
            subroutine_name = s_table_type[13:-14]
        else:
            subroutine_name += self.current_token[13:-14]

        if self.check_token(1, '<symbol> ( </symbol>'):
            # ( symbol
            self.advance()
            self.jack_array.append(' ' * c_sc + self.current_token)

            self.write_push('POINTER', '0')

            # expressionList ------------------------------------
            exp_count = int(self.call_expression_list(c_sc, subroutine_name, master_level))
            # /expressionList-----------------------------------

            # ) symbol
            self.advance()
            self.jack_array.append(' ' * c_sc + self.current_token)

            # VM Translation
            subroutine_name = self.class_name[13:-14] + '.' + subroutine_name
            exp_count += 1
            exp_count = str(exp_count)

           # self.write_push('POINTER', '0')

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
            exp_count = self.call_expression_list(c_sc, subroutine_name, master_level)
            # /expressionList-----------------------------------

            # ) : <symbol> ) </symbol>
            self.advance()
            self.jack_array.append(' ' * c_sc + self.current_token)

        return (subroutine_name, exp_count, subroutine_type)
    # End of Subroutine Call-----------------------------------

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
        elif segment == 'LOCAL':
            self.vm_table.append('push local ' + index)
        elif segment == 'ARGUMENT':
            self.vm_table.append('push argument ' + index)
        elif segment == 'POINTER':
            self.vm_table.append('push pointer ' + index)
        elif segment == '<keyword> field </keyword>':
            self.vm_table.append('push this ' + index)
        elif segment == '<keyword> static </keyword>':
            self.vm_table.append('push static ' + index)
        elif segment == 'THAT':
            self.vm_table.append('push that ' + index)
        elif segment == 'TEMP':
            self.vm_table.append('push temp ' + index)
        else:
            self.vm_table.append('UNDEFINED PUSH!!!' + segment + index)

    def write_pop(self, segment, index):
        if segment == 'TEMP':
            self.vm_table.append('pop temp ' + index)
        elif segment == 'LOCAL':
            self.vm_table.append('pop local ' + index)
        elif segment == 'ARGUMENT':
            self.vm_table.append('pop argument ' + index)
        elif segment == 'POINTER':
            self.vm_table.append('pop pointer ' + index)
        elif segment == '<keyword> field </keyword>':
            self.vm_table.append('pop this ' + index)
        elif segment == '<keyword> static </keyword>':
            self.vm_table.append('pop static ' + index)
        elif segment == 'THAT':
            self.vm_table.append('pop that ' + index)
        else:
            self.vm_table.append('UNDEFINED POP!!!' + segment+ index)

    def write_arithmetic(self, command):
        if command == 'ADD':
            self.vm_table.append('add')
        elif command == 'NEG':
            self.vm_table.append('neg')
        elif command == 'SUB':
            self.vm_table.append('sub')
        elif command == 'NOT':
            self.vm_table.append('not')
        elif command == 'GT':
            self.vm_table.append('gt')
        elif command == 'LT':
            self.vm_table.append('lt')
        elif command == 'AND':
            self.vm_table.append('and')
        elif command == 'OR':
            self.vm_table.append('or')
        elif command == 'EQ':
            self.vm_table.append('eq')
        else:
            self.vm_table.append('NO COMMAND FOUND')

    def write_function(self, name, nLocals):
        self.vm_table.append('function ' + name + ' ' + nLocals)

    def write_call(self, name, nArgs):
        self.vm_table.append('call ' + name + ' ' + nArgs)

    def write_return(self):
        self.vm_table.append('return')

    def write_label(self, label):
        self.vm_table.append('label ' + label)

    def write_if(self, label):
        self.vm_table.append('if-goto ' + label)

    def write_goto(self, label):
        self.vm_table.append('goto ' + label)

    def get_jack_file(self):
        return self.jack_array

    def get_vm_file(self):
        return self.vm_table

    def make_jack_file(self, f_file_name=''):
        if f_file_name == '':
            file_name = self.token_file_name + 'JackCompiled'
        else:
            file_name = f_file_name

        file = open(folder_directory + '/' + file_name + '.xml', 'w')
        for token_element in self.jack_array:
            file.write(token_element + '\n')

    def make_vm_file(self, f_file_name=''):
        if f_file_name == '':
            file_name = self.token_file_name + 'VMCompiled'
        else:
            file_name = f_file_name

        file = open(folder_directory + '/' + file_name + '.xml', 'w')
        for vm_element in self.vm_table:
            file.write(vm_element + '\n')


class SymbolTable:
    def __init__(self):
        self.class_table = []
        self.subroutine_table = []

        self.count_STATIC = 0
        self.count_FIELD = 0
        self.count_ARG = 0
        self.count_VAR = 0

    def start_subroutine(self, mode='', f_class_entry='', is_method=False):
        if mode == 'print':
            print('Subroutine-Table------------------------------------------------------')
            [print(table_entry) for table_entry in self.subroutine_table]
        self.count_ARG = 0
        self.count_VAR = 0
        self.subroutine_table = []

        if is_method:
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
        elif f_kind == 'LOCAL':
            self.subroutine_table.append((f_name, f_type, f_kind, self.count_VAR))
            self.count_VAR += 1
        else:
            print('Undefined KIND!!!')

    def var_count(self, f_kind):
        if f_kind == '<keyword> static </keyword>':
            return self.count_STATIC
        elif f_kind == '<keyword> field </keyword>':
            return self.count_FIELD
        elif f_kind == 'ARGUMENT':
            return self.count_ARG
        elif f_kind == 'LOCAL':
            return self.count_VAR
        else:
            print('UNDEFINED KIND!!!')

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
        # Checks the subroutine table what is the index of the token
        for entry in self.subroutine_table:
            if entry[0] == f_name:
                return entry[3]

        # Checks the subroutine table what is the index of the token
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
        jack_array.make_vm_file()


def jack_tester():
    for tuple_element in jack_arrays:
        token_array = JackTokenizer(tuple_element)
        token_tuple_array.append(token_array.get_token_filename_tuple())
        token_array.make_token_file('tester')

    jack_array = JackCompiler(token_tuple_array[3])
    jack_array.make_jack_file()
    jack_array.make_vm_file()

    print("VM TRANSLATION------------------------------------------")
    [print(vm_code) for vm_code in jack_array.get_vm_file()]




jack_translate()
#jack_tester()
