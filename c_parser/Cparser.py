#!/usr/bin/python

from scanner import Scanner
import AST


class Cparser(object):
    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("right", '='),
        ("left", 'OR'),
        ("left", 'AND'),
        ("left", '|'),
        ("left", '^'),
        ("left", '&'),
        ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
        ("left", 'SHL', 'SHR'),
        ("left", '+', '-'),
        ("left", '*', '/', '%'),
    )

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno,
                                                                                      self.scanner.find_tok_column(p),
                                                                                      p.type, p.value))
        else:
            print("Unexpected end of input")

    def p_program(self, p):
        """program : declarations fundefs_opt instructions_opt"""
        print(AST.Program(declarations=p[1], fundefs_opt=p[2], instructions_opt=p[3]))

    def p_declarations(self, p):
        """declarations : declarations declaration
                        | """
        if len(p) == 3:
            p[0] = AST.Declarations() if p[1] is None else p[1]
            p[0].add(p[2])
        else:
            p[0] = AST.Declarations()

    def p_declaration(self, p):
        """declaration : TYPE inits ';' 
                       | error ';' """
        if len(p) == 4:
            p[0] = AST.Declaration(d_type=p[1], inits=p[2])

    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
        if len(p) == 4:
            p[0] = AST.Inits() if p[1] is None else p[1]
            p[0].add(p[3])
        else:
            p[0] = AST.Inits()
            p[0].add(p[1])

    def p_init(self, p):
        """init : ID '=' expression """
        d_id = p[1]
        expr = p[3]
        p[0] = AST.Init(d_id, expr)

    def p_instructions_opt(self, p):
        """instructions_opt : instructions
                            | """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = AST.Instructions()

    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """
        if len(p) == 3:
            p[0] = AST.Instructions() if p[1] is None else p[1]
            p[0].add(p[2])
        else:
            p[0] = AST.Instructions()
            p[0].add(p[1])

    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr 
                       | repeat_instr 
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr
                       | expression ';' """
        p[0] = p[1]

    def p_print_instr(self, p):
        """print_instr : PRINT expr_list ';'
                       | PRINT error ';' """
        expression_list = p[2]
        p[0] = AST.PrintInstruction(expression_list)

    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
        p[0] = AST.LabeledInstruction(p[1], p[3])

    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        p[0] = AST.Assignment(id=p[1], expression=p[3])

    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """

        else_instruction = None if len(p) < 8 else p[7]
        p[0] = AST.ChoiceInstruction(condition=p[3], instruction=p[5], else_instruction=else_instruction)

    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """
        p[0] = AST.WhileInstruction(condition=p[3], instruction=p[5])

    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """
        p[0] = AST.RepeatInstruction(condition=p[4], instructions=p[2])

    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = AST.ReturnInstruction(p[2])

    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = AST.ContinueInstruction()

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = AST.BreakInstruction()

    def p_compound_instr(self, p):
        """compound_instr : '{' declarations instructions_opt '}' """
        p[0] = AST.CompoundInstruction(declarations=p[2], instructions_opt=p[3])

    def p_condition(self, p):
        """condition : expression"""
        p[0] = p[1]

    def p_const(self, p):
        """const : INTEGER
                 | FLOAT
                 | STRING"""
        p[0] = p[1]

    def p_expression(self, p):
        """expression : const
                      | ID
                      | expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression
                      | '(' expression ')'
                      | '(' error ')'
                      | ID '(' expr_list_or_empty ')'
                      | ID '(' error ')' """
        if len(p) == 2:
            p[0] = AST.Const(p[1])
        elif p[1] == '(':
            p[0] = p[2]
        elif p[2] == '(':
            p[0] = AST.Funcall(id=p[1], expression_list=p[3])
        else:
            p[0] = AST.BinExpr(left=p[1], op=p[2], right=p[3])

    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ExpressionList()

    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """
        if len(p) == 4:
            p[0] = AST.Expressions() if p[1] is None else p[1]
            p[0].add(p[3])
        else:
            p[0] = AST.Expressions()
            p[0].add(p[1])

    def p_fundefs_opt(self, p):
        """fundefs_opt : fundefs
                       | """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = AST.Fundefs()

    def p_fundefs(self, p):
        """fundefs : fundefs fundef
                   | fundef """
        if len(p) == 3:
            p[0] = AST.Fundefs() if p[1] is None else p[1]
            p[0].add(p[2])
        else:
            p[0] = AST.Fundefs()
            p[0].add(p[1])

    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
        p[0] = AST.Fundef(d_type=p[1], id=p[2], arguments=p[4], compound_instructions=p[6])

    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = AST.Arguments()

    def p_args_list(self, p):
        """args_list : args_list ',' arg 
                     | arg """

        if len(p) == 4:
            p[0] = AST.Arguments() if p[1] is None else p[1]
            p[0].add(p[3])
        else:
            p[0] = AST.Arguments()
            p[0].add(p[1])

    def p_arg(self, p):
        """arg : TYPE ID """
        p[0] = AST.Argument(type=p[1], id=p[2])
