/*
This file is part of PyANTLR. See LICENSE.txt for license
details..........Copyright (C) Wolfgang Haefelinger, 2004.

Java 1.3 AST Recognizer Grammar
Author: (see java.g preamble)
This grammar is in the PUBLIC DOMAIN
*/


options {
    language=Python;
}

{
    from asttypes import Module
}


class walker extends TreeParser;

options {
    importVocab = Java;
}


module [infile, outfile]
    {
        m = Module(infile, outfile)
    }
    : (packageDefinition [m])?
      (importDefinition [m])*
      (typeDefinition [m])*
    {
        return m
    }
    ;


packageDefinition [b]
    : #(PACKAGE_DEF identifier[b])
    ;


importDefinition [b]
    : #(IMPORT identifierStar[b] )
    ;


typeDefinition [b]
    { 
        c = b.newClass()
    }
    : #(CLASS_DEF modifiers[c]
                  identifier[c] 
                  extendsClause[c]
                  implementsClause[c]
                  objBlock[c])
    | #(INTERFACE_DEF modifiers[c]
                      identifier[c]
                      extendsClause[c]
                      interfaceBlock[c])
    ;


typeSpec [b]
    : #(TYPE typeSpecArray[b])
    ;


typeSpecArray [b]
    : #(ARRAY_DECLARATOR typeSpecArray[b])
    | type[b]
    ;


type [b]
    : id0:identifier[b]
    {
        try:
            b.setType(id0)
        except (AttributeError, ):
            pass
    }
    | builtInType[b]
    ;


builtInType [b]
    : "void"
    | "boolean"
    | "byte"
    | "char"
    | "short"
    | "int"
    | "float"
    | "long"
    | "double"
    ;


modifiers [b]
    : #(MODIFIERS (modifier[b])*)
    ;


modifier [b]
    : "private"
    | "public"
    | "protected"
    | "static"
    | "transient"
    | "final"
    | "abstract"
    | "native"
    | "threadsafe"
    | "synchronized"
    | "const"
    | "volatile"
    | "strictfp"
    ;


extendsClause [b]
    : #(EXTENDS_CLAUSE (identifier[b])* )
    ;


implementsClause [b]
    : #(IMPLEMENTS_CLAUSE (identifier[b])* )
    ;


interfaceBlock [b]
    : #(OBJBLOCK
           (methodDecl[b]
            |variableDef[b]
            |typeDefinition[b]
        )*
    )
    ;


objBlock [b]
    : #(OBJBLOCK
           (ctorDef[b]
            |methodDef[b]
            |variableDef[b]
            |typeDefinition[b]
            |#(STATIC_INIT slist[b])
            |#(INSTANCE_INIT slist[b])
        )*
    )
    ;


ctorDef [b]
    {
        m = b.newMethod()
        m.name = "__init__"
    }
    : #(CTOR_DEF modifiers[m]
                 methodHead[m]
                 (slist[m])?)
    ;


methodDecl [b]
    : #(METHOD_DEF modifiers[b]
                   typeSpec[b]
                   methodHead[b])
    ;


methodDef [b]
    {
        m = b.newMethod()
    }
    : #(METHOD_DEF modifiers[m]
                   typeSpec[b]
                   methodHead[m]
                   (slist[m])?)
    ;


variableDef [b]
    {
        e = b.newExpression()
    }
    : #(VARIABLE_DEF modifiers[e]
                     t:typeSpec[e]
                     d:varDecl[e]
                     i:varInit[e])
        {
            e.setType(t.getFirstChild())
        }
    ;


parameterDef [method]
    : #(PARAMETER_DEF modifiers[method]
                      typeSpec[method]
                      i0:identifier[method])
    {
        method.addParameter(i0)
    }
    ;


objectInit [b]
    : #(INSTANCE_INIT slist[b])
    ;


varDecl [e]
    : i0:identifier[e]
    {
        e.setLeft(i0)
    }
    | LBRACK varDecl[e]
    ;


varInit [b]
    : #(ASSIGN id0:initializer[b])
    {
        b.setOp("=")
    }
    | // purpose
    {
        b.setOp("=")
    }
    ;


initializer [b]
    : expression[b]
    | arrayInitializer[b]
    ;


arrayInitializer [b]
    : #(ARRAY_INIT (initializer[b])*)
    ;


methodHead [m]
    : identifier[m]
      #(PARAMETERS (parameterDef[m])* ) (throwsClause[m])?
    ;


throwsClause [b]
    : #("throws" (identifier[b])*)
    ;


identifier [b]
    : i0:IDENT
    {
        b.setName(i0)
    }

    | #(DOT identifier[b] i1:IDENT)
    {
        b.setName(i1)
    }
    ;


identifierStar [b]
    : IDENT
    | #(DOT identifier[b] (STAR|IDENT) )
    ;


slist [b]
    : #(SLIST (stat[b])*)
    ;

stat [b]
    {
        e = b.newExpression()
    }
    : typeDefinition[b]
    | variableDef[b]
    | expression[b]
    | #(LABELED_STAT IDENT stat[b])
    | #("if" e0:expression[b] s0:stat[b] (s1:stat[b])? )
        {
            i = b.newIf()
            i.setClause(e0, s0, s1)
        }

    | #("for"
          #(FOR_INIT ((variableDef[b])+ | elist[b])?)
          #(FOR_CONDITION (expression[b])?)
          #(FOR_ITERATOR (elist[b])?)
          stat[b]
        )
    | #("while" expression[b] stat[b])
    | #("do" stat[b] expression[b])
    | #("break" (IDENT)? )
    | #("continue" (IDENT)? )
    | #("return" (r:expression[b])? )
    {
        e.setExpression("return", r, "")
    }

    |
    {
        // e.addSwitch()
        // e.op = "=="
    }
        #("switch" x:expression[b] (c:caseGroup[b])*)
    {
        // e.addSwitchExpr(x)
    }

    | #("throw" expression[b])
    | #("synchronized" expression[b] stat[b])
    | tryBlock[b]
    | slist[b]
    | EMPTY_STAT
    ;


caseGroup [b]
    : #(CASE_GROUP (#("case" e:expression[b]) | "default")+ s:slist[b])
    {
        // b.addCase(e, s)
    }
    ;


tryBlock [b]
    : #("try" slist[b] (handler[b])* (#("finally" slist[b]))?)
    ;


handler [b]
    : #("catch" parameterDef[b] slist[b])
    ;


elist [b]
    : #(ELIST (expression[b])*)
    ;


expression [b]
    {
    if not b.isExpression():
        b = b.newExpression()
    }
    : #(EXPR expr[b])
    ;


expr [b]
    // trinary operator
    : #(QUESTION expr[b] expr[b] expr[b])

    // binary operators
    | #(ASSIGN lh0:expr[b] rh0:expr[b])
    {
        b.setExpression(lh0, "=", rh0)
    }

    | #(PLUS_ASSIGN lh1:expr[b] rh1:expr[b])
    {
        b.setExpression(lh1, "+=", rh1)
    }

    | #(MINUS_ASSIGN lh2:expr[b] rh2:expr[b])
    {
        b.setExpression(lh2, "-=", rh2)
    }

    | #(STAR_ASSIGN lh3:expr[b] rh3:expr[b])
    {
        b.setExpression(lh3, "*=", rh3)
    }

    | #(DIV_ASSIGN expr[b] expr[b])
    | #(MOD_ASSIGN expr[b] expr[b])
    | #(SR_ASSIGN expr[b] expr[b])
    | #(BSR_ASSIGN expr[b] expr[b])
    | #(SL_ASSIGN expr[b] expr[b])
    | #(BAND_ASSIGN expr[b] expr[b])
    | #(BXOR_ASSIGN expr[b] expr[b])
    | #(BOR_ASSIGN expr[b] expr[b])
    | #(LOR expr[b] expr[b])
    | #(LAND expr[b] expr[b])
    | #(BOR expr[b] expr[b])
    | #(BXOR expr[b] expr[b])
    | #(BAND expr[b] expr[b])
    | #(NOT_EQUAL expr[b] expr[b])

    | #(EQUAL lh18:expr[b] rh18:expr[b])
    {
        b.setExpression(lh18, "==", rh18)
    }

    | #(LT lh19:expr[b] rh19:expr[b])
    {
        b.setExpression(lh19, "<", rh19)
    }

    | #(GT lh20:expr[b] rh20:expr[b])
    {
        b.setExpression(lh20, ">", rh20)
    }

    | #(LE lh21:expr[b] rh21:expr[b])
    {
        b.setExpression(lh21, "<=", rh21)
    }

    | #(GE lh22:expr[b] rh22:expr[b])
    {
        b.setExpression(lh22, ">=", rh22)
    }

    // shift left, shift right
    | #(SL lh23:expr[b] rh23:expr[b])
    | #(SR lh24:expr[b] rh24:expr[b])
    | #(BSR lh25:expr[b] rh25:expr[b])

    | #(PLUS lh26:expr[b] rh26:expr[b])
    {
        b.setExpression(lh26, "+", rh26)
    }

    | #(MINUS expr[b] expr[b])
    {
        // b.addBinary(lh, rh, "-")
    }

    | #(DIV expr[b] expr[b])
    | #(MOD expr[b] expr[b])
    | #(STAR expr[b] expr[b])
    | #(INC expr[b])
    | #(DEC expr[b])
    | #(POST_INC expr[b])
    | #(POST_DEC expr[b])
    | #(BNOT expr[b])
    | #(LNOT expr[b])
    | #("instanceof" expr[b] expr[b])

    | #(UNARY_MINUS um:expr[b])
    {
        // b.addUnary(um, "-")
    }

    | #(UNARY_PLUS expr[b])
    | primaryExpression[b]
    ;


primaryExpression [e]
    : i0:IDENT
        {
            e.setLeft(i0)
        }

    | #(DOT
           (expr[e]
               (IDENT
                | arrayIndex[e]
                | "this"
                | "class"
                | #("new" IDENT elist[e] )
                | "super"
                )
            | #(ARRAY_DECLARATOR typeSpecArray[e])
            | builtInType[e]("class")?
            )
        )

    | arrayIndex[e]
    | #(METHOD_CALL primaryExpression[e] elist[e])
    | ctorCall[e]
    | #(TYPECAST typeSpec[e] ex0:expr[e])
        {
        }

    | n0:newExpression[e]

    | c0:constant[e]
        {
            e.setRight(c0)
        }
    | "super"
    | "true"
    | "false"
    | "this"
    | "null"
    // type name used with instanceof
    | typeSpec[e]
    ;


ctorCall [b]
    : #(CTOR_CALL elist[b] )
    | #(SUPER_CTOR_CALL
           (elist[b]
            | primaryExpression[b] elist[b]
            )
       )
    ;


arrayIndex [b]
    : #(INDEX_OP expr[b] expression[b])
    ;


constant [b]
    : NUM_INT
    | CHAR_LITERAL
    | STRING_LITERAL
    | NUM_FLOAT
    | NUM_DOUBLE
    | NUM_LONG
    ;


newExpression [b]
    : #("new" type[b]
           (newArrayDeclarator[b] (arrayInitializer[b])?
            | elist[b] (objBlock[b])?
            )
       )
    ;


newArrayDeclarator [b]
    : #(ARRAY_DECLARATOR (newArrayDeclarator[b])? 
                         (expression[b])?
       )
    ;
