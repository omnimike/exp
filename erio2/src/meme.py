from ply import lex, yacc

def debug(*args, **kwargs):
    import inspect
    str_args = '|'.join([str(a) for a in args])
    str_kwargs = '|'.join(['{}:{}'.format(k, str(v)) for k, v in kwargs.items()])
    print('Line: {}: {} {}'.format(inspect.currentframe().f_back.f_lineno,
                                   str_args, str_kwargs))

class MemeError(Exception): pass
class MemeSyntaxError(MemeError): pass
class MemeSemanticError(MemeError): pass
class MemeDuplicateDefinitionError(MemeSemanticError): pass
class MemeIncompatibleTypesError(MemeSemanticError): pass
class MemeUndefinedError(MemeSemanticError): pass
class MemeUndefinedTypeError(MemeUndefinedError): pass
class MemeUndefinedVariableError(MemeUndefinedError): pass
class MemeNotAFunctionError(MemeSemanticError): pass
class MemeInternalError(MemeError): pass

outputdir = '__temp__'

reserved = {
    'if':       'IF',
    'else':     'ELSE',
    'while':    'WHILE',
    'func':     'FUNC',
    'return':   'RETURN',
    'and':      'AND',
    'or':       'OR',
    'not':      'NOT',
}

literals = r',=+-*/%()[]{}'

tokens = [
    'STRING',
    'INTEGER',
    'EQ',
    'GT',
    'LT',
    'GE',
    'LE',
    'NE',
    'RARROW',
    'ID'
] + list(reserved.values())

def lexer():
    '''Creates a ply lexer for the meme language'''
    
    t_INTEGER   = r'[0-9]+'
    t_STRING    = r'".*?"'
    t_EQ        = r'=='
    t_GT        = r'>'
    t_LT        = r'<'
    t_GE        = r'>='
    t_LE        = r'<='
    t_NE        = r'!='
    t_RARROW    = r'->'

    t_ignore = ' \t'
    
    def t_ID(t):
        r'[A-Za-z_][A-Za-z0-9_]*'
        t.type = reserved.get(t.value, 'ID')
        return t

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    
    def t_error(t):
        MemeSyntaxError('Illegal character: "{}"'.format(t.value[0]))
        t.lexer.skip(1)
    
    return lex.lex()

def parser():
    '''Creates a ply parser for the meme language'''

    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('right', 'NOT'),
        ('nonassoc', 'EQ', 'NE', 'GT', 'LT', 'GE', 'LE'),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', 'UMINUS')
    )

    def p_block(p):
        '''block : statement
                          | statement block'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]

    def p_statement(p):
        '''statement : assign
                     | decl
                     | if
                     | while
                     | return
                     | func_def
                     | func_call'''
        p[0] = p[1]

    def p_assign(p):
        '''assign : ID '=' expr'''
        p[0] = ('assign', p[1], p[3])

    def p_decl(p):
        '''decl : type ID'''
        p[0] = ('decl', p[1], p[2])

    def p_type(p):
        '''type : ID'''
        p[0] = ('type', p[1])

    def p_if(p):
        '''if : IF expr '{' block '}' else'''
        p[0] = ('if', p[2], p[4], p[6])

    def p_else(p):
        '''else : empty
                | ELSE '{' block '}' '''
        if len(p) == 2:
            p[0] = None
        else:
            p[0] = p[3]

    def p_while(p):
        '''while : WHILE expr '{' block '}' '''
        p[0] = ('while', p[2], p[4])

    def p_func_def(p):
        '''func_def : FUNC ID '(' param_list ')' RARROW type '{' block '}' '''
        p[0] = ('func_def', p[2], p[7], p[4], p[9])

    def p_param_list(p):
        '''param_list : empty
                      | decl
                      | decl ',' param_list'''
        if p[1] is None:
            p[0] = []
        elif len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]
            

    def p_return(p):
        '''return : RETURN expr'''
        p[0] = ('return', p[2])

    def p_expr(p):
        '''expr : '(' expr ')'
                | binop_expr
                | unop_expr
                | func_call
                | var
                | literal'''
        if p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = p[1]

    def p_binop_expr(p):
        '''binop_expr : expr EQ expr
                      | expr NE expr
                      | expr GT expr
                      | expr LT expr
                      | expr GE expr
                      | expr LE expr
                      | expr AND expr
                      | expr OR expr
                      | expr '+' expr
                      | expr '-' expr
                      | expr '*' expr
                      | expr '/' expr
                      | expr '%' expr'''
        p[0] = ('binop', p[2], p[1], p[3])

    def p_unop_expr(p):
        '''unop_expr : NOT expr
                     | '-' expr %prec UMINUS'''
        p[0] = ('unop', p[1], p[2])

    def p_func_call(p):
        '''func_call : ID '(' arg_list ')' '''
        p[0] = ('func_call', p[1], p[3])

    def p_arg_list(p):
        '''arg_list : expr
                    | expr ',' arg_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_var(p):
        '''var : ID'''
        p[0] = ('var', p[1])

    def p_literal(p):
        '''literal : integer
                   | string'''
        p[0] = ('literal', p[1][0], p[1][1])

    def p_integer(p):
        '''integer : INTEGER'''
        p[0] = (('type', 'int'), int(p[1]))

    def p_string(p):
        '''string : STRING'''
        p[0] = (('type', 'str'), p[1][1:-1])

    def p_empty(p):
        '''empty : '''
        p[0] = None

    def p_error(p):
        raise MemeSyntaxError(p)

    return yacc.yacc(outputdir=outputdir)

def temp_name_generator(prefix):
    count = 0
    while True:
        yield prefix + str(count)
        count += 1

class Scope(dict):
    '''A hirachical dict which is used for symbol tables'''
    def __init__(self, parent=None):
        self.parent = parent
        
    def lookup(self, key):
        if key not in self and self.parent != None:
            return self.parent.lookup(key)
        return self[key]

    def exists(self, key):
        return key in self or \
               (self.parent is not None and self.parent.exists(key))

    def insert_with_unique_name(self, key, value):
        if key in self:
            value.randomize_name()
            key = value.name
        self[key] = value

    def merge(self, symt):
        for k, v in symt.items():
            self.insert_with_unique_name(k, v)

    def filter_type(self, typ):
        return [sym for sym in self.values() if sym.isa(typ)]

class IRObject:
    def isa(self, *typs):
        return isinstance(self, typs)

class Type(IRObject):
    def __init__(self, name, compound=None):
        self.name = name
        self.comp = compound

    def can_assign(self, other):
        return self == other

    def __str__(self):
        return self.name

class Variable(IRObject):
    temp_prefix = '%'
    temp_var_names = temp_name_generator(temp_prefix)
    
    def __init__(self, typ, name=None, offset=None):
        self.type = typ
        self.name = name if name is not None else next(self.temp_var_names)
        self.offset = offset

    def randomize_name(self):
        self.name = next(self.temp_var_names)

    def __str__(self):
        return "Variable(type= {} , name= {} )".format(self.type, self.name)

class Literal(IRObject):
    def __init__(self, typ, value):
        self.type = typ
        self.value = value

    def __str__(self):
        return "Literal(type= {} , value= {} )".format(self.type, self.value)

class Function(IRObject):
    def __init__(self, name, typ, params, symt, code):
        self.name = name
        self.type = typ
        self.params = params
        self.symt = symt
        self.code = code

class Return(IRObject):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return "Return(expr= {} )".format(self.expr)

class FuncCall(IRObject):
    def __init__(self, func, args):
        self.func = func
        self.args = args
        self.type = func.type

    def __str__(self):
        return "FuncCall(func= {} , args= {} )".format(self.func, self.args)

class If(IRObject):
    def __init__(self, cond, then, els = None):
        self.cond = cond
        self.then = then
        self.els = els

class While(IRObject):
    def __init__(self, cond, do):
        self.cond = cond
        self.do = do

class Assign(IRObject):
    def __init__(self, var, value):
        self.var = var
        self.value = value

    def __str__(self):
        return "Assign(var= {} , val= {} )".format(self.var, self.value)

class Block(IRObject):
    def __init__(self, symt=None, stmnts=None):
        self.symt = symt if symt is not None else Scope()
        self.stmnts = stmnts if stmnts is not None else []

    def extend(self, block):
        self.symt.merge(block.symt)
        self.stmnts.extend(block.stmnts)

    def __str__(self):
        return "Block(statements= {} )".format(
            '\n'.join(str(s) for s in self.stmnts))

class BinOp(IRObject):
    '''Binary Operator'''
    def __init__(self, op, ret_type, lhs_type, rhs_type):
        self.op = op
        self.ret_type = ret_type
        self.lhs_type = lhs_type
        self.rhs_type = rhs_type

class UnOp(IRObject):
    '''Unary operator'''
    def __init__(self, op, ret_type, rhs_type):
        self.op = op
        self.ret_type = ret_type
        self.rhs_type = rhs_type

class BinExpr(IRObject):
    '''Expression with binary operator'''
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs
        self.type = op.ret_type

    def __str__(self):
        return "BinExpr(op= {} , lhs= {} , rhs= {} )".format(
            self.op.op, self.lhs, self.rhs)

class UnExpr(IRObject):
    '''Expression with unary operator'''
    def __init__(self, op, rhs):
        self.op = op
        self.rhs = rhs
        self.type = op.ret_type

    def __str__(self):
        return "UnExpr(op= {} , rhs= {} )".format(self.op.op, self.rhs)

class Label(IRObject):
    temp_prefix = ''
    temp_label_names = temp_name_generator(temp_prefix)
    
    def __init__(self, name=None):
        self.name = name if name is not None else next(self.temp_label_names)

class Jump(IRObject):
    def __init__(self, label, cond=None):
        self.label = label
        self.cond = cond

def ir(ast):

    #On variable names:
    #ast:   Abstract Syntax Table
    #b:     branch (of the AST)
    #symt:  Symbol Table
    #gst:   Global Symbol Table
    
    def make_global_symbol_table():
        symt = Scope()

        int_type = Type('int')
        str_type = Type('str')
        func_type = Type('func')

        symt['int'] = int_type
        symt['str'] = str_type
        symt['func'] = func_type

        def make_int_binop(symbol):
            return BinOp(symbol, int_type, int_type, int_type)

        def make_int_unop(symbol):
            return UnOp(symbol, int_type, int_type)

        for s in ('==', '!=', '<', '>', '<=', '>=', 'and', 'or', \
                  '+', '-', '*', '/', '%'):
            symt[s] = make_int_binop(s)

        for s in ('-', 'not'):
            symt[s] = make_int_unop(s)
            
        return symt

    gst = make_global_symbol_table()    

    def typ(b, symt):
        type_name = b[1]
        if symt.exists(type_name) and symt.lookup(type_name).isa(Type):
            return symt.lookup(type_name)
        else: raise MemeUndefinedTypeError(type_name)

    def decl(b, symt):
        var_name = b[2]
        var_type = typ(b[1], symt)
        if var_name in symt:
            raise MemeDuplicateDefinitionError(var_name)
        symt[var_name] = Variable(var_type, var_name)

    def assign(b, symt):
        var_name = b[1]
        if not symt.exists(var_name):
            raise MemeUndefinedError(var_name)
        var = symt.lookup(b[1])
        val = expr(b[2], symt)
        if not var.type.can_assign(val.type):
            raise MemeIncompatibleTypesError(
                'Variable type: {}, Expression type: {}'.format(
                    var.type, val.type))
        return Assign(var, val)

    def if_(b, symt):
        cond = expr(b[1], symt)
        then = block(b[2],symt)
        els = block(b[3], symt)
        return If(cond, then, els)

    def while_(b, symt):
        cond = expr(b[1], symt)
        do = block(b[2], symt)
        return While(cond, do)

    def param_defs(b, symt, param_list):
        for p in b:
            decl(p, symt)
            param_list.append(symt[p[2]])

    def func_def(b, symt):
        name = b[1]
        ret_type = typ(b[2], symt)
        params = []
        param_symt = Scope(symt)
        param_defs(b[3], param_symt, params)
        func = Function(name, ret_type, params, None, None)
        code = block(b[4], param_symt)
        func.symt = param_symt
        func.code = code
        symt[name] = func

    def ret(b, symt):
        return Return(expr(b[1], symt))

    def func_call(b, symt):
        func = symt.lookup(b[1])
        if not func.isa(Function):
            raise MemeNotAFunctionError(b[1])
        args = [expr(a, symt) for a in b[2]]
        return FuncCall(func, args)
    
    def block(b, symt):
        statements = []
        symt = Scope(symt)
        #If b is None it means we have an empty block (like an empty 'else')
        if b is not None:
            for s in b:
                statement = stmnt(s, symt)
                if statement is not None:
                    statements.append(statement)
        return Block(symt, statements)

    def stmnt(b, symt):
        return {
            'decl':         decl,
            'if':           if_,
            'while':        while_,
            'func_def':     func_def,
            'func_call':    func_call,
            'literal':      literal,
            'assign':       assign,
            'return':       ret}[b[0]](b, symt)

    def binop(b, symt):
        op = symt.lookup(b[1])
        lhs = expr(b[2], symt)
        rhs = expr(b[3], symt)
        return BinExpr(op, lhs, rhs)

    def unop(b, symt):
        op = symt.lookup(b[1])
        rhs = expr(b[2], symt)
        return UnExpr(op, rhs)

    def variable(b, symt):
        var_name = b[1]
        if not symt.exists(var_name):
            raise MemeUndefinedVariableError(var_name)
        return symt.lookup(var_name)

    def literal(b, symt):
        lit_type = typ(b[1], symt)
        lit_val = b[2]
        return Literal(lit_type, lit_val)

    def expr(b, symt):
        return {
            'func_call':    func_call,
            'binop':        binop,
            'unop':         unop,
            'var':          variable,
            'literal':      literal}[b[0]](b, symt)

    return block(ast, gst)

def destruct(block):
    '''Destructures a block and all of the functions defined in it.'''
    def destruct_block(b):
        dblock = Block(b.symt);
        for s in b.stmnts:
            if s.isa(If):
                dblock.extend(destruct_if(s))
            elif s.isa(While):
                dblock.extend(destruct_while(s))
            else:
                dblock.stmnts.append(s)
        b.symt = dblock.symt
        b.stmnts = dblock.stmnts

    def destruct_if(stmnt):
        dblock = Block()
        dblock.symt.merge(stmnt.then.symt)
        dblock.symt.merge(stmnt.els.symt)
        lab_true = Label()
        lab_end = Label()
        dblock.stmnts = [Jump(lab_true, stmnt.cond)]
        destruct_block(stmnt.els)
        dblock.extend(stmnt.els)
        dblock.stmnts.extend([
            Jump(lab_end),
            lab_true])
        destruct_block(stmnt.then)
        dblock.extend(stmnt.then)
        dblock.stmnts.append(lab_end)
        return dblock

    def destruct_while(stmnt):
        dblock = Block()
        dblock.symt.merge(stmnt.do.symt)
        lab_cont = Label()
        lab_body = Label()
        lab_end = Label()
        dblock.stmnts = [
            lab_cont,
            Jump(lab_body, stmnt.cond),
            Jump(lab_end),
            lab_body]
        destruct_block(stmnt.do)
        dblock.extend(stmnt.do)
        dblock.stmnts.extend([
            Jump(lab_cont),
            lab_end])
        return dblock

    destruct_block(block)
    for f in block.symt.filter_type(Function):
        destruct_block(f.code)

def expand_exprs(block):

    #TODO expand 'and' and 'or' into jumps

    def expand_block(block):
        new_stmnts = []
        for s in block.stmnts:
            stmnts = []
            newtemps = []
            if s.isa(If):
                s.cond, stmnts, newtemps = expand_expr(s.cond)
                expand_block(s.then)
                expand_block(s.els)
            elif s.isa(While):
                s.cond, stmnts, newtemps = expand_expr(s.cond)
                expand_block(s.do)
            elif s.isa(Jump):
                if s.cond is not None:
                    s.cond, stmnts, newtemps = expand_expr(s.cond)
            elif s.isa(Assign):
                s.value, stmnts, newtemps = expand_expr(s.value)
            elif s.isa(FuncCall):
                s, stmnts, newtemps = expand_expr(s)
            new_stmnts.extend(stmnts)
            new_stmnts.append(s)
            block.symt.update({tmp.name: tmp for tmp in newtemps})
        block.stmnts = new_stmnts

    def expand_expr(expr):
        stmnts = []
        newtemps = []
        if expr.isa(Variable):
            return expr, stmnts, newtemps
        elif expr.isa(Literal):
            return expr, stmnts, newtemps    
        elif expr.isa(BinExpr):
            return expand_binop_expr(expr)
        elif expr.isa(UnExpr):
            return expand_unop_expr(expr)            
        elif expr.isa(FuncCall):
            return expand_func_call(expr)

    def expand_unop_expr(expr):
        stmnts = []
        newtemps =[]
        rhs, stmnts, newtemps = expand_expr(expr.rhs)
        temp = Variable(expr.type)
        newtemps.append(temp)
        val = UnExpr(expr.op, rhs)
        assign = Assign(temp, val)
        stmnts.append(assign)
        return temp, stmnts, newtemps

    def expand_binop_expr(expr):
        stmnts = []
        newtemps = []
        lhs, lhs_stmnts, lhs_temps = expand_expr(expr.lhs)
        stmnts.extend(lhs_stmnts)
        newtemps.extend(lhs_temps)
        rhs, rhs_stmnts, rhs_temps = expand_expr(expr.rhs)
        stmnts.extend(rhs_stmnts)
        newtemps.extend(rhs_temps)
        temp = Variable(expr.type)
        newtemps.append(temp)
        val = BinExpr(expr.op, lhs, rhs)
        assign = Assign(temp, val)
        stmnts.append(assign)
        return temp, stmnts, newtemps

    def expand_func_call(expr):
        stmnts = []
        newtemps = []
        args = expr.args
        lowered_args = []
        for arg in args:
            arg, arg_stmnts, arg_temps = expand_expr(arg)
            stmnts.extend(arg_stmnts)
            newtemps.extend(arg_temps)
            lowered_args.append(arg)
        temp = Variable(expr.type)
        newtemps.append(temp)
        val = FuncCall(expr.func, lowered_args)
        assign = Assign(temp, val)
        stmnts.append(assign)
        return temp, stmnts, newtemps

    for f in block.symt.filter_type(Function):
        expand_block(f.code)
    expand_block(block)

def offset_vars(block):
    #Parameters are numbered from 1 to n.
    #Locals are numbered from 0 to -n.
    c = 0
    for v in block.symt.filter_type(Variable):
        v.offset = c
        c -= 1
    for f in block.symt.filter_type(Function):
        c = 1
        for p in f.params:
            p.offset = c
            c += 1
        offset_vars(f.code)

def x86asm(block):
    word_length = 4

    class Register:
        prefix = '%'
        def __init__(self, name):
            self.name = self.prefix + name
            
        def __call__(self, offset):
            #We need to skip over the return address and the saved base pointer.
            #The first param starts at 8(%ebp).
            #The first local starts at -4(%ebp).
            offset = word_length * (offset - 1) if offset <= 0 \
                     else word_length * (offset + 1)
            return '{}({})'.format(offset, self)

        def __str__(self):
            return self.name
 
    eax = Register('eax')
    ebx = Register('ebx')
    ecx = Register('ecx')
    edx = Register('edx')
    ebp = Register('ebp')
    esp = Register('esp')
    edi = Register('edi')
    esi = Register('esi')

    al = Register('al')

    def asm_block(block):
        func_defs = []
        stmnts = []
        for f in block.symt.filter_type(Function):
            func_defs.extend(asm_func(f))
        for s in block.stmnts:
            stmnts.extend(asm_stmnt(s))
        return func_defs, stmnts

    def asm_func(func):
        #Nested functions are not tested for unique names yet.
        funcs, body = asm_block(func.code)
        code = funcs
        code.extend([func.name + ':',
                     ('enter', word_length * len(func.params), 0)])
        code.extend(body)
        code.extend(['leave', 'ret'])
        return code

    def asm_stmnt(stmnt):
        if stmnt.isa(Assign):
            return asm_assign(stmnt)
        elif stmnt.isa(FuncCall):
            return asm_func_call(stmnt)
        elif stmnt.isa(Label):
            return asm_label(stmnt)
        elif stmnt.isa(Jump):
            return asm_jump(stmnt)
        elif stmnt.isa(Return):
            return asm_ret(stmnt)
        else:
            raise MemeInternalError('Invalid statement found: {}'.format(stmnt))

    def asm_assign(stmnt):
        code = asm_expr(stmnt.value)
        code.append(('mov', eax, ebp(stmnt.var.offset)))
        return code

    def asm_func_call(stmnt):
        code = [('push', asm_atom(arg)) for arg in reversed(stmnt.args)]
        code.append(('call', stmnt.func.name))
        return code

    def asm_label(stmnt):
        return ['L{}:'.format(stmnt.name)]

    def asm_jump(stmnt):
        if stmnt.cond is not None:
            code = asm_expr(stmnt.cond)
            code.extend([('cmp', 0, eax),
                         ('jne', 'L{}'.format(stmnt.label.name))])
            return code
        else:
            return [('jmp', 'L{}'.format(stmnt.label.name))]

    def asm_ret(stmnt):
        code = asm_expr(stmnt.expr)
        code.extend(['leave', 'ret'])
        return code

    def asm_expr(expr):
        if expr.isa(Literal, Variable):
            return [('mov', asm_atom(expr), eax)]
        elif expr.isa(BinExpr):
            code = [('mov', asm_atom(expr.lhs), eax),
                    ('mov', asm_atom(expr.rhs), edx)]
            code.extend(asm_binop(expr.op))
            return code
        elif expr.isa(UnExpr):
            code = [('mov', asm_atom(expr.rhs), eax)]
            code.extend(asm_unop(expr.op))
            return code
        elif expr.isa(FuncCall):
            return asm_func_call(expr)
        else:
            raise MemeInternalError('Invalid expression found: {}'.format(expr))

    def asm_atom(expr):
        if expr.isa(Literal):
            return '${}'.format(expr.value)
        elif expr.isa(Variable):
            return ebp(expr.offset)

    def asm_binop(op):
        bool_ops = {
            '==':   ('sete', al),
            '!=':   ('setne', al),
            '<':    ('setg', al),
            '>':    ('setl', al),
            '<=':   ('setle', al),
            '>=':   ('setge', al)}
        arith_ops = {
            '+':    ('add', edx, eax),
            '-':    ('sub', edx, eax),
            '*':    ('imul', edx, eax),
            '/':    ('idiv', edx, eax),
            '%':    ('mod', edx, eax)}
        if op.op in bool_ops:
            return [('cmp', eax, edx),
                    bool_ops[op.op],
                    ('movzbl', al, eax)]
        elif op.op in arith_ops:
            return [arith_ops[op.op]]
        else:
            raise MemeInternalError('Invalid boolean operator: {}'.format(op.op))

    def asm_unop(op):
        if op.op == 'not':
            return [('cmp', 0, eax),
                    ('sete', al),
                    ('movzbl', al, eax)]
        elif op.op == '-':
            return [('neg', eax)]
        else:
            raise MemeInternalError('Invalid unary operator: {}'.format(op.op))

    def inst_to_string(inst):
        if isinstance(inst, int):
            return '$' + str(inst)
        if isinstance(inst, tuple):
            if len(inst) == 3:
                return '{} {},{}'.format(inst[0],
                    inst_to_string(inst[1]), inst_to_string(inst[2]))
        if isinstance(inst, tuple):
            if len(inst) == 2:
                return '{} {}'.format(inst[0], inst_to_string(inst[1]))
        return str(inst)
        
    template = r'''
.text
{funcs}

.globl _main
_main:
enter ${local_size},$0
call ___main
{main}
leave
ret
'''
    funcs, main = asm_block(block)
    funcs_code = ''
    for stmnt in funcs:
        funcs_code += '{}\n'.format(inst_to_string(stmnt))
    main_code = ''
    for stmnt in main:
        main_code += '{}\n'.format(inst_to_string(stmnt))
    local_size = len(block.symt.filter_type(Variable)) * word_length
    return template.format(funcs=funcs_code, main=main_code, local_size=local_size)

if __name__ == '__main__':
    c = r'''
        func add(int a, int b) -> int {
            while b != 0 {
                a = a + 1
                b = b - 1
            }
            return a
        }
        if ((3 - 2) * 20 < 6) {
            return -1
        }
        else {
            return add(3, 4)
        }
        '''
    l = lexer()
    p = parser()
    i = ir(p.parse(c, l))
    destruct(i)
    expand_exprs(i)
    offset_vars(i)
    a = x86asm(i)
    with open('meme.s', 'w') as f:
        f.write(a)
