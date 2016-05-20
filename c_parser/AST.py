class Node(object):
    def __str__(self):
        return self.printTree()


class Program(Node):
    def __init__(self, declarations, fundefs_opt, instructions_opt):
        self.declarations = declarations
        self.fundefs_opt = fundefs_opt
        self.instructions_opt = instructions_opt


class Declarations(Node):
    def __init__(self):
        self.declarations = []

    def add(self, declaration):
        self.declarations.append(declaration)


class Declaration(Node):
    def __init__(self, d_type, inits):
        self.type = d_type
        self.inits = inits


class Inits(Node):
    def __init__(self):
        self.inits = []

    def add(self, init):
        self.inits.append(init)


class Init(Node):
    def __init__(self, id, expr):
        self.id = id
        self.expression = expr


class Instructions(Node):
    def __init__(self):
        self.instructions = []

    def add(self, instruction):
        self.instructions.append(instruction)


class PrintInstruction(Node):
    def __init__(self, expression_list):
        self.expression_list = expression_list


class LabeledInstruction(Node):
    def __init__(self, id, instruction):
        self.id = id
        self.instruction = instruction


class Assignment(Node):
    def __init__(self, id, expression):
        self.id = id
        self.expression = expression


class ChoiceInstruction(Node):
    def __init__(self, condition, instruction, else_instruction):
        self.condition = condition
        self.instruction = instruction
        self.else_instruction = else_instruction


class WhileInstruction(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class RepeatInstruction(Node):
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions


class ReturnInstruction(Node):
    def __init__(self, expression):
        self.expression = expression


class ContinueExpression(Node):
    pass


class BreakExpression(Node):
    pass


class CompoundInstruction(Node):
    def __init__(self, declarations, instructions_opt):
        self.declarations = declarations
        self.instructions_opt = instructions_opt


class Const(Node):
    def __init__(self, value):
        self.value = value


class Funcall(Node):
    def __init__(self, id, expression_list):
        self.id = id
        self.expressions = expression_list


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Expressions(Node):
    def __init__(self):
        self.expressions = []

    def add(self, expression):
        self.expressions.append(expression)


class Fundef(Node):
    def __init__(self, d_type, id, arguments, compound_instructions):
        self.type = d_type
        self.id = id
        self.arguments = arguments
        self.compound_instructions = compound_instructions


class Fundefs(Node):
    def __init__(self):
        self.fundefs = []

    def add(self, fundef):
        self.fundefs.append(fundef)


class Arguments(Node):
    def __init__(self):
        self.arguments = []

    def add(self, argument):
        self.arguments.append(argument)


class Argument(Node):
    def __init__(self, type, id):
        self.type = type
        self.id = id