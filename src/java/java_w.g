// This file is part of PyANTLR. See LICENSE.txt for license
// details..........Copyright (C) Wolfgang Haefelinger, 2004.
//
// $Id$

/* Java 1.3 AST Recognizer Grammar
 *
 * Author: (see java.g preamble)
 *
 * This grammar is in the PUBLIC DOMAIN
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


module
    {
    m = Module()
    }
	:	(packageDefinition [m])?
		(importDefinition [m])*
		(typeDefinition [m])*
    {
    return m
    }
    ;



packageDefinition [module]
	:	#( PACKAGE_DEF i:identifier[module])
	;



importDefinition [module]
	:	#( IMPORT identifierStar[module] )
	;



typeDefinition [module]
    { 
    cls = module.klass()
    }
	:	#(CLASS_DEF modifiers[cls] identifier[cls] extendsClause[cls] implementsClause[cls] objBlock[cls] )
	|	#(INTERFACE_DEF modifiers[cls] identifier[cls] extendsClause[cls] interfaceBlock[cls] )
	;



typeSpec [block]
	:	#(TYPE typeSpecArray[block])
	;



typeSpecArray [block]
	:	#( ARRAY_DECLARATOR typeSpecArray[block] )
	|	type[block]
	;



type [block]
    :	identifier[block]
	|	builtInType
	;



builtInType
    :   "void"
    |   "boolean"
    |   "byte"
    |   "char"
    |   "short"
    |   "int"
    |   "float"
    |   "long"
    |   "double"
    ;



modifiers [block]
	:	#( MODIFIERS (modifier[block])* )
	;



modifier [block]
    :   "private"
    |   "public"
    |   "protected"
    |   "static"
    |   "transient"
    |   "final"
    |   "abstract"
    |   "native"
    |   "threadsafe"
    |   "synchronized"
    |   "const"
    |   "volatile"
	|	"strictfp"
    ;



extendsClause [classobj]
	:	#(EXTENDS_CLAUSE (identifier[classobj])* )
	;



implementsClause [module]
	:	#(IMPLEMENTS_CLAUSE (identifier[module])* )
	;



interfaceBlock [block]
	:	#(	OBJBLOCK
			(	methodDecl[block]
			|	variableDef[block]
			|	typeDefinition[block]
			)*
		)
	;



objBlock [block]
	:	#(	OBJBLOCK
			(	ctorDef[block]
			|	methodDef[block]
			|	variableDef[block]
			|	typeDefinition[block]
			|	#(STATIC_INIT slist[block])
			|	#(INSTANCE_INIT slist[block])
			)*
		)
	;



ctorDef [block]
{
method = block.method()
method.name = "__init__"
    }
	:	#(CTOR_DEF modifiers[method] methodHead[method] (slist[method])?)
	;



methodDecl [block]
	:	#(METHOD_DEF modifiers[block] typeSpec[block] methodHead[block])
	;



methodDef [block]
    {
    method = block.method()
    }
	:	#(METHOD_DEF modifiers[method] typeSpec[block] methodHead[method] (slist[method])?)
	;



variableDef [block]
	:	#(VARIABLE_DEF modifiers[block] t:typeSpec[block] n:variableDeclarator i:varInitializer[block])
        {
        print "#####", repr(block)
        block.addVariableDef(t, n, i)        
        }
	;



parameterDef [method]
	:	#(PARAMETER_DEF modifiers[method] typeSpec[method] i:identifier[method] )
        {
        method.addParameters(i)
        }

	;



objectinitializer [block]
	:	#(INSTANCE_INIT slist[block])
	;



variableDeclarator
	:	IDENT
	|	LBRACK variableDeclarator
	;



varInitializer [block]
	:	#(ASSIGN initializer[block])
	|
	;



initializer [block]
	:	expression[block]
	|	arrayInitializer[block]
	;



arrayInitializer [block]
	:	#(ARRAY_INIT (initializer[block])*)
	;



methodHead [method]
	:	identifier[method] #( PARAMETERS (parameterDef[method])* ) (throwsClause[method])?
	;



throwsClause [block]
	:	#( "throws" (identifier[block])* )
	;



identifier [block]
	:	i:IDENT
    {
    if block:
        block.addIdent(i)
    }
	|	#( DOT identifier[block] j:IDENT )
    {
    if block:
        block.addIdent(j)
    }
	;



identifierStar [module]
	:	IDENT
	|	#( DOT identifier[module] (STAR|IDENT) )
	;



slist [block]
	:	#( SLIST (stat[block])* )
	;

stat [block]
    :	typeDefinition[block]
	|	variableDef[block]
	|	expression[block]
	|	#(LABELED_STAT IDENT stat[block])
	|	#("if" expression[block] stat[block] (stat[block])? )
	|	#(	"for"
			#(FOR_INIT ((variableDef[block])+ | elist[block])?)
			#(FOR_CONDITION (expression[block])?)
			#(FOR_ITERATOR (elist[block])?)
			stat[block]
		)
	|	#("while" expression[block] stat[block])
	|	#("do" stat[block] expression[block])
	|	#("break" (IDENT)? )
	|	#("continue" (IDENT)? )
	|	#("return" (r:expression[block])? )
        {
        expr = block.expression()
        expr.addReturn(r)
        }
	|	#("switch" expression[block] (caseGroup[block])*)
	|	#("throw" expression[block])
	|	#("synchronized" expression[block] stat[block])
	|	tryBlock[block]
	|	slist[block] // nested SLIST
    // uncomment to make assert JDK 1.4 stuff work
    // |   #("assert" expression[block] (expression[block])?)
	|	EMPTY_STAT
	;

caseGroup [block]
	:	#(CASE_GROUP (#("case" expression[block]) | "default")+ slist[block])
	;

tryBlock [block]
	:	#( "try" slist[block] (handler[block])* (#("finally" slist[block]))? )
	;

handler [block]
	:	#( "catch" parameterDef[block] slist[block] )
	;

elist[block]
	:	#( ELIST (expression[block])* )
	;

expression [block]
	:	#(EXPR expr[block])
	;

expr [block]
    {
    e = block.expression()
    }
    :	#(QUESTION expr[block] expr[block] expr[block])	// trinary operator
	|	#(ASSIGN lh:expr[block] rh:expr[block])			// binary operators...
        {
        e.addBinary(lh, rh, "=")
        }
	|	#(PLUS_ASSIGN expr[block] expr[block])
        {
        e.addBinary(lh, rh, "+=")
        }
	|	#(MINUS_ASSIGN expr[block] expr[block])
        {
        e.addBinary(lh, rh, "-=")
        }
	|	#(STAR_ASSIGN expr[block] expr[block])
        {
        e.addBinary(lh, rh, "*=")
        }
	|	#(DIV_ASSIGN expr[block] expr[block])
	|	#(MOD_ASSIGN expr[block] expr[block])
	|	#(SR_ASSIGN expr[block] expr[block])
	|	#(BSR_ASSIGN expr[block] expr[block])
	|	#(SL_ASSIGN expr[block] expr[block])
	|	#(BAND_ASSIGN expr[block] expr[block])
	|	#(BXOR_ASSIGN expr[block] expr[block])
	|	#(BOR_ASSIGN expr[block] expr[block])
	|	#(LOR expr[block] expr[block])
	|	#(LAND expr[block] expr[block])
	|	#(BOR expr[block] expr[block])
	|	#(BXOR expr[block] expr[block])
	|	#(BAND expr[block] expr[block])
	|	#(NOT_EQUAL expr[block] expr[block])
	|	#(EQUAL expr[block] expr[block])
        {
        e.addBinary(lh, rh, "==")
        }
	|	#(LT expr[block] expr[block])
        {
        e.addBinary(lh, rh, "<")
        }
	|	#(GT expr[block] expr[block])
        {
        e.addBinary(lh, rh, ">")
        }
	|	#(LE expr[block] expr[block])
        {
        e.addBinary(lh, rh, "<=")
        }
	|	#(GE expr[block] expr[block])
        {
        e.addBinary(lh, rh, ">=")
        }
	|	#(SL expr[block] expr[block])
	|	#(SR expr[block] expr[block])
	|	#(BSR expr[block] expr[block])
	|	#(PLUS expr[block] expr[block])
        {
        e.addBinary(lh, rh, "+")
        }
	|	#(MINUS expr[block] expr[block])
        {
        e.addBinary(lh, rh, "-")
        }
	|	#(DIV expr[block] expr[block])
	|	#(MOD expr[block] expr[block])
	|	#(STAR expr[block] expr[block])
	|	#(INC expr[block])
	|	#(DEC expr[block])
	|	#(POST_INC expr[block])
	|	#(POST_DEC expr[block])
	|	#(BNOT expr[block])
	|	#(LNOT expr[block])
	|	#("instanceof" expr[block] expr[block])
	|	#(UNARY_MINUS um:expr[block])
        {
        e.addUnary(um, "-")
        }
	|	#(UNARY_PLUS expr[block])
	|	primaryExpression[block]
	;

primaryExpression [block]
    {
    e = block.expression()
    }
    :   IDENT
    |   #(	DOT
			(	expr[block]
				(	IDENT
				|	arrayIndex[block]
				|	"this"
				|	"class"
				|	#( "new" IDENT elist[e] )
				|   "super"
				)
			|	#(ARRAY_DECLARATOR typeSpecArray[block])
			|	builtInType ("class")?
			)
		)
	|	arrayIndex[block]
	|	#(METHOD_CALL primaryExpression[block] elist[block])
	|	ctorCall
	|	#(TYPECAST typeSpec[block] expr[block])
	|   newExpression[e]
	|   constant[block]
    |   "super"
    |   "true"
    |   "false"
    |   "this"
    |   "null"
	|	typeSpec[block] // type name used with instanceof
	;

ctorCall
	:	#( CTOR_CALL elist[block] )
	|	#( SUPER_CTOR_CALL
			(	elist[block]
			|	primaryExpression[block] elist[block]
			)
		 )
	;

arrayIndex [block]
	:	#(INDEX_OP expr[block] expression[block])
	;

constant [block]
    :   NUM_INT
    |   CHAR_LITERAL
    |   STRING_LITERAL
    |   NUM_FLOAT
    |   NUM_DOUBLE
    |   NUM_LONG
    ;

newExpression [block]
	:	#(	"new" t:type[block]
			(	newArrayDeclarator[block] (arrayInitializer[block])?
			|	elist[block] (objBlock[block])?
			)
		)

	;

newArrayDeclarator [block]
	:	#( ARRAY_DECLARATOR (newArrayDeclarator[block])? (expression[block])? )
	;
