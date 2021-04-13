# Generated from src/main/antlr/RSQL.g4 by ANTLR 4.8
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\23")
        buf.write("[\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\3\2\3\2\3\2\3\2\3\2\3\2\5\2\33\n")
        buf.write("\2\3\2\3\2\3\2\3\2\3\2\3\2\7\2#\n\2\f\2\16\2&\13\2\3\3")
        buf.write("\3\3\3\3\3\3\3\4\3\4\5\4.\n\4\3\5\3\5\3\5\3\5\3\5\5\5")
        buf.write("\65\n\5\3\6\3\6\3\6\3\6\5\6;\n\6\3\7\3\7\3\7\3\7\7\7A")
        buf.write("\n\7\f\7\16\7D\13\7\3\7\3\7\3\7\3\7\3\7\3\7\7\7L\n\7\f")
        buf.write("\7\16\7O\13\7\3\7\3\7\5\7S\n\7\3\b\3\b\3\t\3\t\3\n\3\n")
        buf.write("\3\n\2\3\2\13\2\4\6\b\n\f\16\20\22\2\4\3\2\t\n\3\2\20")
        buf.write("\21\2]\2\32\3\2\2\2\4\'\3\2\2\2\6-\3\2\2\2\b\64\3\2\2")
        buf.write("\2\n:\3\2\2\2\fR\3\2\2\2\16T\3\2\2\2\20V\3\2\2\2\22X\3")
        buf.write("\2\2\2\24\25\b\2\1\2\25\26\7\3\2\2\26\27\5\2\2\2\27\30")
        buf.write("\7\4\2\2\30\33\3\2\2\2\31\33\5\4\3\2\32\24\3\2\2\2\32")
        buf.write("\31\3\2\2\2\33$\3\2\2\2\34\35\f\6\2\2\35\36\7\13\2\2\36")
        buf.write("#\5\2\2\7\37 \f\5\2\2 !\7\f\2\2!#\5\2\2\6\"\34\3\2\2\2")
        buf.write("\"\37\3\2\2\2#&\3\2\2\2$\"\3\2\2\2$%\3\2\2\2%\3\3\2\2")
        buf.write("\2&$\3\2\2\2\'(\5\6\4\2()\5\b\5\2)*\5\6\4\2*\5\3\2\2\2")
        buf.write("+.\5\n\6\2,.\7\17\2\2-+\3\2\2\2-,\3\2\2\2.\7\3\2\2\2/")
        buf.write("\60\7\5\2\2\60\61\7\17\2\2\61\65\7\5\2\2\62\65\7\r\2\2")
        buf.write("\63\65\7\16\2\2\64/\3\2\2\2\64\62\3\2\2\2\64\63\3\2\2")
        buf.write("\2\65\t\3\2\2\2\66;\5\16\b\2\67;\5\22\n\28;\5\20\t\29")
        buf.write(";\5\f\7\2:\66\3\2\2\2:\67\3\2\2\2:8\3\2\2\2:9\3\2\2\2")
        buf.write(";\13\3\2\2\2<=\7\3\2\2=B\5\n\6\2>?\7\6\2\2?A\5\n\6\2@")
        buf.write(">\3\2\2\2AD\3\2\2\2B@\3\2\2\2BC\3\2\2\2CE\3\2\2\2DB\3")
        buf.write("\2\2\2EF\7\4\2\2FS\3\2\2\2GH\7\7\2\2HM\5\n\6\2IJ\7\6\2")
        buf.write("\2JL\5\n\6\2KI\3\2\2\2LO\3\2\2\2MK\3\2\2\2MN\3\2\2\2N")
        buf.write("P\3\2\2\2OM\3\2\2\2PQ\7\b\2\2QS\3\2\2\2R<\3\2\2\2RG\3")
        buf.write("\2\2\2S\r\3\2\2\2TU\t\2\2\2U\17\3\2\2\2VW\t\3\2\2W\21")
        buf.write("\3\2\2\2XY\7\22\2\2Y\23\3\2\2\2\13\32\"$-\64:BMR")
        return buf.getvalue()


class RSQLParser ( Parser ):

    grammarFileName = "RSQL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'='", "','", "'['", "']'", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'=='", "'!='" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "TRUE", "FALSE", 
                      "AND_OPERATOR", "OR_OPERATOR", "EQ", "NE", "IDENTIFIER", 
                      "INT_LITERAL", "DECIMAL_LITERAL", "STRING_LITERAL", 
                      "STRING_ESCAPE_SEQ" ]

    RULE_statement = 0
    RULE_comparison = 1
    RULE_expression = 2
    RULE_comparator = 3
    RULE_value = 4
    RULE_array_value = 5
    RULE_boolean_literal = 6
    RULE_numeric_literal = 7
    RULE_string_literal = 8

    ruleNames =  [ "statement", "comparison", "expression", "comparator", 
                   "value", "array_value", "boolean_literal", "numeric_literal", 
                   "string_literal" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    TRUE=7
    FALSE=8
    AND_OPERATOR=9
    OR_OPERATOR=10
    EQ=11
    NE=12
    IDENTIFIER=13
    INT_LITERAL=14
    DECIMAL_LITERAL=15
    STRING_LITERAL=16
    STRING_ESCAPE_SEQ=17

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class StatementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.left = None # StatementContext
            self.wrapped = None # StatementContext
            self.node = None # ComparisonContext
            self.op = None # Token
            self.right = None # StatementContext

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RSQLParser.StatementContext)
            else:
                return self.getTypedRuleContext(RSQLParser.StatementContext,i)


        def comparison(self):
            return self.getTypedRuleContext(RSQLParser.ComparisonContext,0)


        def AND_OPERATOR(self):
            return self.getToken(RSQLParser.AND_OPERATOR, 0)

        def OR_OPERATOR(self):
            return self.getToken(RSQLParser.OR_OPERATOR, 0)

        def getRuleIndex(self):
            return RSQLParser.RULE_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)



    def statement(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = RSQLParser.StatementContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 0
        self.enterRecursionRule(localctx, 0, self.RULE_statement, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                self.state = 19
                self.match(RSQLParser.T__0)
                self.state = 20
                localctx.wrapped = self.statement(0)
                self.state = 21
                self.match(RSQLParser.T__1)
                pass

            elif la_ == 2:
                self.state = 23
                localctx.node = self.comparison()
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 34
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 32
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = RSQLParser.StatementContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_statement)
                        self.state = 26
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 27
                        localctx.op = self.match(RSQLParser.AND_OPERATOR)
                        self.state = 28
                        localctx.right = self.statement(5)
                        pass

                    elif la_ == 2:
                        localctx = RSQLParser.StatementContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_statement)
                        self.state = 29
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 30
                        localctx.op = self.match(RSQLParser.OR_OPERATOR)
                        self.state = 31
                        localctx.right = self.statement(4)
                        pass

             
                self.state = 36
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ComparisonContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.left = None # ExpressionContext
            self.cmp = None # ComparatorContext
            self.right = None # ExpressionContext

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RSQLParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(RSQLParser.ExpressionContext,i)


        def comparator(self):
            return self.getTypedRuleContext(RSQLParser.ComparatorContext,0)


        def getRuleIndex(self):
            return RSQLParser.RULE_comparison

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparison" ):
                return visitor.visitComparison(self)
            else:
                return visitor.visitChildren(self)




    def comparison(self):

        localctx = RSQLParser.ComparisonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_comparison)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            localctx.left = self.expression()
            self.state = 38
            localctx.cmp = self.comparator()
            self.state = 39
            localctx.right = self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def value(self):
            return self.getTypedRuleContext(RSQLParser.ValueContext,0)


        def IDENTIFIER(self):
            return self.getToken(RSQLParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return RSQLParser.RULE_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = RSQLParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_expression)
        try:
            self.state = 43
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [RSQLParser.T__0, RSQLParser.T__4, RSQLParser.TRUE, RSQLParser.FALSE, RSQLParser.INT_LITERAL, RSQLParser.DECIMAL_LITERAL, RSQLParser.STRING_LITERAL]:
                self.enterOuterAlt(localctx, 1)
                self.state = 41
                self.value()
                pass
            elif token in [RSQLParser.IDENTIFIER]:
                self.enterOuterAlt(localctx, 2)
                self.state = 42
                self.match(RSQLParser.IDENTIFIER)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComparatorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(RSQLParser.IDENTIFIER, 0)

        def EQ(self):
            return self.getToken(RSQLParser.EQ, 0)

        def NE(self):
            return self.getToken(RSQLParser.NE, 0)

        def getRuleIndex(self):
            return RSQLParser.RULE_comparator

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparator" ):
                return visitor.visitComparator(self)
            else:
                return visitor.visitChildren(self)




    def comparator(self):

        localctx = RSQLParser.ComparatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_comparator)
        try:
            self.state = 50
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [RSQLParser.T__2]:
                self.enterOuterAlt(localctx, 1)
                self.state = 45
                self.match(RSQLParser.T__2)
                self.state = 46
                self.match(RSQLParser.IDENTIFIER)
                self.state = 47
                self.match(RSQLParser.T__2)
                pass
            elif token in [RSQLParser.EQ]:
                self.enterOuterAlt(localctx, 2)
                self.state = 48
                self.match(RSQLParser.EQ)
                pass
            elif token in [RSQLParser.NE]:
                self.enterOuterAlt(localctx, 3)
                self.state = 49
                self.match(RSQLParser.NE)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.boolean = None # Boolean_literalContext
            self.string = None # String_literalContext
            self.number = None # Numeric_literalContext
            self.array = None # Array_valueContext

        def boolean_literal(self):
            return self.getTypedRuleContext(RSQLParser.Boolean_literalContext,0)


        def string_literal(self):
            return self.getTypedRuleContext(RSQLParser.String_literalContext,0)


        def numeric_literal(self):
            return self.getTypedRuleContext(RSQLParser.Numeric_literalContext,0)


        def array_value(self):
            return self.getTypedRuleContext(RSQLParser.Array_valueContext,0)


        def getRuleIndex(self):
            return RSQLParser.RULE_value

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValue" ):
                return visitor.visitValue(self)
            else:
                return visitor.visitChildren(self)




    def value(self):

        localctx = RSQLParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_value)
        try:
            self.state = 56
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [RSQLParser.TRUE, RSQLParser.FALSE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 52
                localctx.boolean = self.boolean_literal()
                pass
            elif token in [RSQLParser.STRING_LITERAL]:
                self.enterOuterAlt(localctx, 2)
                self.state = 53
                localctx.string = self.string_literal()
                pass
            elif token in [RSQLParser.INT_LITERAL, RSQLParser.DECIMAL_LITERAL]:
                self.enterOuterAlt(localctx, 3)
                self.state = 54
                localctx.number = self.numeric_literal()
                pass
            elif token in [RSQLParser.T__0, RSQLParser.T__4]:
                self.enterOuterAlt(localctx, 4)
                self.state = 55
                localctx.array = self.array_value()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Array_valueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def value(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RSQLParser.ValueContext)
            else:
                return self.getTypedRuleContext(RSQLParser.ValueContext,i)


        def getRuleIndex(self):
            return RSQLParser.RULE_array_value

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArray_value" ):
                return visitor.visitArray_value(self)
            else:
                return visitor.visitChildren(self)




    def array_value(self):

        localctx = RSQLParser.Array_valueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_array_value)
        self._la = 0 # Token type
        try:
            self.state = 80
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [RSQLParser.T__0]:
                self.enterOuterAlt(localctx, 1)
                self.state = 58
                self.match(RSQLParser.T__0)
                self.state = 59
                self.value()
                self.state = 64
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==RSQLParser.T__3:
                    self.state = 60
                    self.match(RSQLParser.T__3)
                    self.state = 61
                    self.value()
                    self.state = 66
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 67
                self.match(RSQLParser.T__1)
                pass
            elif token in [RSQLParser.T__4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 69
                self.match(RSQLParser.T__4)
                self.state = 70
                self.value()
                self.state = 75
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==RSQLParser.T__3:
                    self.state = 71
                    self.match(RSQLParser.T__3)
                    self.state = 72
                    self.value()
                    self.state = 77
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 78
                self.match(RSQLParser.T__5)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Boolean_literalContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TRUE(self):
            return self.getToken(RSQLParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(RSQLParser.FALSE, 0)

        def getRuleIndex(self):
            return RSQLParser.RULE_boolean_literal

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBoolean_literal" ):
                return visitor.visitBoolean_literal(self)
            else:
                return visitor.visitChildren(self)




    def boolean_literal(self):

        localctx = RSQLParser.Boolean_literalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_boolean_literal)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            _la = self._input.LA(1)
            if not(_la==RSQLParser.TRUE or _la==RSQLParser.FALSE):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Numeric_literalContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT_LITERAL(self):
            return self.getToken(RSQLParser.INT_LITERAL, 0)

        def DECIMAL_LITERAL(self):
            return self.getToken(RSQLParser.DECIMAL_LITERAL, 0)

        def getRuleIndex(self):
            return RSQLParser.RULE_numeric_literal

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumeric_literal" ):
                return visitor.visitNumeric_literal(self)
            else:
                return visitor.visitChildren(self)




    def numeric_literal(self):

        localctx = RSQLParser.Numeric_literalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_numeric_literal)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 84
            _la = self._input.LA(1)
            if not(_la==RSQLParser.INT_LITERAL or _la==RSQLParser.DECIMAL_LITERAL):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class String_literalContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_LITERAL(self):
            return self.getToken(RSQLParser.STRING_LITERAL, 0)

        def getRuleIndex(self):
            return RSQLParser.RULE_string_literal

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString_literal" ):
                return visitor.visitString_literal(self)
            else:
                return visitor.visitChildren(self)




    def string_literal(self):

        localctx = RSQLParser.String_literalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_string_literal)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 86
            self.match(RSQLParser.STRING_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[0] = self.statement_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def statement_sempred(self, localctx:StatementContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 3)
         




