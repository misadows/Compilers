import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    def _indent(num):
        return '| ' * num

    @addToClass(AST.Node)
    def printTree(self, indentation=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Program)
    def printTree(self, indentation=0):
        return '{declarations}{fundefs_opt}{instructions_opt}'.format(
            declarations="" if self.declarations is None else self.declarations.printTree(indentation),
            fundefs_opt="" if self.fundefs_opt is None else self.fundefs_opt.printTree(indentation),
            instructions_opt=self.instructions_opt.printTree(indentation + 1)
        )

    @addToClass(AST.Declarations)
    def printTree(self, indentation=0):
        return '' if not self.declarations else '{indent}DECL\n{declarations}'.format(
            indent=TreePrinter._indent(indentation),
            declarations=''.join(map(lambda x: x.printTree(indentation + 1), self.declarations))
        )

    @addToClass(AST.Declaration)
    def printTree(self, indentation=0):
        return self.inits.printTree(indentation)

    @addToClass(AST.Inits)
    def printTree(self, indentation=0):
        return "".join(map(lambda x: x.printTree(indentation), self.inits))

    @addToClass(AST.Init)
    def printTree(self, indentation=0):
        return '{indent1}=\n{indent2}{id}\n{expr}'.format(
            indent1=TreePrinter._indent(indentation),
            indent2=TreePrinter._indent(indentation + 1),
            id=str(self.id),
            expr=self.expression.printTree(indentation + 1)
        )

    @addToClass(AST.Instructions)
    def printTree(self, indentation=0):
        return ''.join(map(lambda x: x.printTree(indentation), self.instructions))

    @addToClass(AST.PrintInstruction)
    def printTree(self, indentation=0):
        return '{indent}PRINT\n{expr}'.format(
            indent=TreePrinter._indent(indentation + 1),
            expr=self.expression_list.printTree(indentation + 1)
        )

    @addToClass(AST.LabeledInstruction)
    def printTree(self, indentation=0):
        return '{indent1}LABEL\n{indent2}{id}\n{instr}'.format(
            indent1=TreePrinter._indent(indentation),
            indent2=TreePrinter._indent(indentation + 1),
            id=str(self.id),
            instr=self.instr.printTree(indentation + 1)
        )

    @addToClass(AST.Assignment)
    def printTree(self, indentation=0):
        return '{indent1}=\n{indent2}{id}\n{expr}'.format(
            indent1=TreePrinter._indent(indentation),
            indent2=TreePrinter._indent(indentation + 1),
            id=str(self.id),
            expr=self.expression.printTree(indentation + 1)
        )

    @addToClass(AST.ChoiceInstruction)
    def printTree(self, indentation=0):
        return '{indent}IF\n{condition}{instruction}{else_instruction}'.format(
            indent=TreePrinter._indent(indentation),
            condition=self.condition.printTree(indentation + 1),
            instruction=self.instruction.printTree(indentation + 1),
            else_instruction='' if self.else_instruction is None else '{indent}ELSE\n{else_instruction}'.format(
                indent=TreePrinter._indent(indentation),
                else_instruction=self.else_instruction.printTree(indentation + 1)
            )
        )

    @addToClass(AST.WhileInstruction)
    def printTree(self, indentation=0):
        return '{indent}WHILE\n{condition}{instruction}'.format(
            indent=TreePrinter._indent(indentation),
            condition=self.condition.printTree(indentation + 1),
            instruction=self.instruction.printTree(indentation)
        )

    @addToClass(AST.RepeatInstruction)
    def printTree(self, indentation=0):
        return '{indent}REPEAT{instruction}{indent}UNTIL{condition}'.format(
            indent=TreePrinter._indent(indentation),
            condition=self.condition.printTree(indentation + 1),
            instruction=self.instruction.printTree(indentation + 1)
        )

    @addToClass(AST.ReturnInstruction)
    def printTree(self, indentation=0):
        return '{indent}RETURN\n{expr}'.format(
            indent=TreePrinter._indent(indentation),
            expr=self.expression.printTree(indentation + 1)
        )

    @addToClass(AST.BreakExpression)
    def printTree(self, indentation=0):
        return '{indent}BREAK\n'.format(
            indent=TreePrinter._indent(indentation)
        )

    @addToClass(AST.ContinueExpression)
    def printTree(self, indentation=0):
        return '{indent}CONTINUE\n'.format(
            indent=TreePrinter._indent(indentation)
        )

    @addToClass(AST.Const)
    def printTree(self, indentation=0):
        return '{indent}{value}\n'.format(
            value=str(self.value),
            indent=TreePrinter._indent(indentation)
        )

    @addToClass(AST.Fundefs)
    def printTree(self, indentation=0):
        return ''.join(map(lambda x: x.printTree(indentation), self.fundefs))

    @addToClass(AST.Fundef)
    def printTree(self, indentation=0):
        return '{indent1}FUNDEF\n{indent2}{id}\n{indent2}RET {type}\n{arguments}{instr}'.format(
            indent1=TreePrinter._indent(indentation),
            indent2=TreePrinter._indent(indentation + 1),
            id=str(self.id),
            type=self.type,
            arguments=self.arguments.printTree(indentation + 1),
            instr=self.compound_instructions.printTree(indentation+1)
        )

    @addToClass(AST.Arguments)
    def printTree(self, indentation=0):
        return ''.join(map(lambda x: x.printTree(indentation), self.arguments))

    @addToClass(AST.Argument)
    def printTree(self, indentation=0):
        return '{indent}ARG {id}\n'.format(
            indent=TreePrinter._indent(indentation),
            id=self.id
        )

    @addToClass(AST.CompoundInstruction)
    def printTree(self, indentation=0):
        return '{declarations}{instructions}'.format(
            declarations=('' if not self.declarations else self.declarations.printTree(indentation)),
            instructions=self.instructions_opt.printTree(indentation)
        )

    @addToClass(AST.BinExpr)
    def printTree(self, indentation=0):
        return '{indent}{op}\n{left}{right}'.format(
            indent=TreePrinter._indent(indentation),
            left=self.left.printTree(indentation + 1),
            right=self.right.printTree(indentation + 1),
            op=self.op
        )

    @addToClass(AST.Funcall)
    def printTree(self, indentation=0):
        return '{indent1}FUNCALL\n{indent2}{id}\n{arguments}'.format(
            indent1=TreePrinter._indent(indentation),
            indent2=TreePrinter._indent(indentation + 1),
            id=self.id,
            arguments=self.expressions.printTree(indentation + 1)
        )

    @addToClass(AST.Expressions)
    def printTree(self, indentation=0):
        return ''.join(map(lambda x: x.printTree(indentation + 1), self.expressions))
