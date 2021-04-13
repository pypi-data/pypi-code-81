# Generated from src/main/antlr/RSQL.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .RSQLParser import RSQLParser
else:
    from RSQLParser import RSQLParser

# This class defines a complete generic visitor for a parse tree produced by RSQLParser.

class RSQLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by RSQLParser#statement.
    def visitStatement(self, ctx:RSQLParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RSQLParser#comparison.
    def visitComparison(self, ctx:RSQLParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RSQLParser#expression.
    def visitExpression(self, ctx:RSQLParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RSQLParser#comparator.
    def visitComparator(self, ctx:RSQLParser.ComparatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RSQLParser#value.
    def visitValue(self, ctx:RSQLParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RSQLParser#array_value.
    def visitArray_value(self, ctx:RSQLParser.Array_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RSQLParser#boolean_literal.
    def visitBoolean_literal(self, ctx:RSQLParser.Boolean_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RSQLParser#numeric_literal.
    def visitNumeric_literal(self, ctx:RSQLParser.Numeric_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RSQLParser#string_literal.
    def visitString_literal(self, ctx:RSQLParser.String_literalContext):
        return self.visitChildren(ctx)



del RSQLParser