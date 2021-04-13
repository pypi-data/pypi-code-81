from antlr4 import InputStream, CommonTokenStream
import ast
import operator
from typing import Any
from storage.query.rsql.gen.RSQLVisitor import RSQLVisitor
from storage.query.rsql.gen.RSQLLexer import RSQLLexer
from storage.query.rsql.gen.RSQLParser import RSQLParser
from storage.api import Predicate
from storage.var import Vars


def parse(rsql: str) -> Predicate[Any]:
    lexer = RSQLLexer(InputStream(rsql))
    parser = RSQLParser(CommonTokenStream(lexer))
    tree = parser.statement()
    return tree.accept(StorageQueryVisitor())


class StorageQueryVisitor(RSQLVisitor):
    supported_comparisons = {
        'eq': operator.eq,
        'ne': operator.ne,
        'gt': operator.gt,
        'ge': operator.ge,
        'lt': operator.lt,
        'le': operator.le,
        'in': lambda a, b: b.__contains__(a),
        'contains': lambda a, b: a.__contains__(b),
    }

    def visitStatement(self, ctx: RSQLParser.StatementContext):
        if ctx.wrapped:
            return self.visit(ctx.wrapped)
        if ctx.node:
            return self.visit(ctx.node)
        if ctx.left or ctx.right:
            if ctx.op.type == RSQLParser.AND_OPERATOR:
                return self.visit(ctx.left) & self.visit(ctx.right)
            elif ctx.op.type == RSQLParser.OR_OPERATOR:
                return self.visit(ctx.left) | self.visit(ctx.right)
        return self.visit(ctx.node)

    def visitComparison(self, ctx: RSQLParser.ComparisonContext):
        comparator = self.visit(ctx.cmp)
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        return comparator(left, right)

    def visitExpression(self, ctx: RSQLParser.ExpressionContext):
        if ctx.IDENTIFIER():
            return Vars.key(ctx.getText())
        return self.visit(ctx.value())

    def visitComparator(self, ctx: RSQLParser.ComparatorContext):
        if ctx.EQ():
            return operator.eq
        if ctx.NE():
            return operator.ne
        if ctx.IDENTIFIER():
            textual = ctx.IDENTIFIER().getText()
            if textual not in self.supported_comparisons:
                raise NotImplementedError(ctx)
            return self.supported_comparisons[textual]
        return self.visitChildren(ctx)

    def visitValue(self, ctx: RSQLParser.ValueContext):
        if ctx.boolean:
            return self.visit(ctx.boolean)
        elif ctx.number:
            return self.visit(ctx.number)
        elif ctx.string:
            return self.visit(ctx.string)
        elif ctx.array:
            return self.visit(ctx.array)
        else:
            raise NotImplementedError(ctx)

    def visitArray_value(self, ctx: RSQLParser.Array_valueContext):
        return Vars.const(tuple([self.visit(value) for value in ctx.value()]))

    def visitString_literal(self, ctx: RSQLParser.String_literalContext):
        if ctx.STRING_LITERAL():
            return Vars.const(ast.literal_eval(ctx.getText()))
        else:
            raise NotImplementedError(ctx)

    def visitBoolean_literal(self, ctx: RSQLParser.Boolean_literalContext):
        if ctx.TRUE():
            return Vars.const(True)
        elif ctx.FALSE():
            return Vars.const(False)
        else:
            raise NotImplementedError(ctx)

    def visitNumeric_literal(self, ctx: RSQLParser.Numeric_literalContext):
        textual = ctx.getText()
        if ctx.DECIMAL_LITERAL():
            return Vars.const(float(textual))
        elif ctx.INT_LITERAL():
            return Vars.const(int(textual))
        else:
            raise NotImplementedError(ctx)
