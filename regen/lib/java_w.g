/*
Current:

    This file is part of IbPy.  Redistributed under terms of original
    license below.  Modifications Copyright (C) Troy Melhase
    <troy@gci.net>.

Original:

    This file is part of PyANTLR. See LICENSE.txt for license
    details..........Copyright (C) Wolfgang Haefelinger, 2004.
    Java 1.3 AST Recognizer Grammar
    Author: (see java.g preamble)
    This grammar is in the PUBLIC DOMAIN
*/


options { language=Python; }
{
from asttypes import Module, typeMap, otherTypeMap
noassignment = ("<noassign>", )
missing = ("%s", "<missing>", )
unknown = ("%s", "<unknown>", )
}


class walker extends TreeParser;
options { importVocab = Java; }


module [infile, outfile]
returns [source = Module(infile, outfile)]
    :   (pkg = package_def[source])?
        (imp = import_def[source])*
        (typ = type_def[source])*
    ;


package_def [block]
returns [defn]
    :   #(PACKAGE_DEF defn = identifier[block])
    ;


import_def [block]
returns [defn]
    :   #(IMPORT defn = identifier_star[block])
    ;


type_def [block]
returns [klass = block.newClass()]
    :   #(CLASS_DEF
          modifiers[klass]
          name = identifier[klass] {klass.name = name}
          ext_clause = extends_clause[klass]
          imp_clause = implements_clause[klass]
          obj_block[klass]
        )
    |   #(INTERFACE_DEF
          modifiers[klass]
          name = identifier[klass] {klass.name = name}
          ext_clause = extends_clause[klass]
          interface_block[klass]
        )
    ;


type_spec [block]
returns [spec]
    :   #(t0:TYPE type_spec_array[block])
        {
        value = t0.getFirstChild().getText()
        try:
            spec = otherTypeMap[value]
        except (KeyError, ):
            spec = value
        }
    ;


type_spec_array [block]
    :   #(ARRAY_DECLARATOR type_spec_array[block])
    |   spec = type[block]
    ;


type [block]
returns [typ]
    :   typ = identifier[block]   {block.setType(typ)}
    |   typ = builtin_type[block] {block.setType(typ)}
    ;


builtin_type [block]
returns [typ]
    :   "void"    {typ = "None"  }
    |   "boolean" {typ = "bool"  }
    |   "byte"    {typ = "str"   }
    |   "char"    {typ = "str"   }
    |   "short"   {typ = "int"   }
    |   "int"     {typ = "int"   }
    |   "float"   {typ = "float" }
    |   "long"    {typ = "long"  }
    |   "double"  {typ = "float" }
    ;


modifiers [block, mod=None]
    :   #(MODIFIERS
            (mod = modifier[block])*) {block.addModifier(mod)}
    ;


modifier [block]
returns [mod]
    :   pri0:"private"       {mod = pri0.getText()}
    |   pub0:"public"        {mod = pub0.getText()}
    |   pro0:"protected"     {mod = pro0.getText()}
    |   sta0:"static"        {mod = sta0.getText()}
    |   tra0:"transient"     {mod = tra0.getText()}
    |   fin0:"final"         {mod = fin0.getText()}
    |   abt0:"abstract"      {mod = abt0.getText()}
    |   nat0:"native"        {mod = nat0.getText()}
    |   ths0:"threadsafe"    {mod = ths0.getText()}
    |   syn0:"synchronized"  {mod = syn0.getText()}
    |   con0:"const"         {mod = con0.getText()}
    |   vol0:"volatile"      {mod = vol0.getText()}
    |   sfp0:"strictfp"      {mod = sfp0.getText()}
    ;


extends_clause [block]
returns [clause = None]
    :   #(EXTENDS_CLAUSE
            (clause = identifier[block])*) {block.addBaseClass(clause)}
    ;


implements_clause [block]
returns [clause = None]
    :   #(IMPLEMENTS_CLAUSE
            (clause = identifier[block])*) {block.addBaseClass(clause)}
    ;


interface_block [block]
    :   #(OBJBLOCK
            (method_decl[block]
                | variable_def[block]
                | typ = type_def[block]
            )*
        )
    ;


obj_block [block]
    :   #(OBJBLOCK
            (ctor_def[block]
                | method_def[block]
                | variable_def[block]
                | typ = type_def[block]
                | #(STATIC_INIT statement_list[block])
                | #(INSTANCE_INIT statement_list[block])
            )*
        )
    ;


ctor_def [block]
    :   {
        meth = block.newMethod()
        }
        #(CTOR_DEF
            modifiers[meth]
            method_head[meth, "__init__"]
            (statement_list[meth])?
        )
    ;


method_decl [block]
    :   {
        meth = block.newMethod()
        meth.addSource("raise NotImplementedError()")
        }
        #(METHOD_DEF
            modifiers[meth]
            typ = type_spec[meth]
            method_head[meth]
        ) {meth.setType(typ)}
    ;


method_head [meth, name=None]
    :   ident = identifier[meth]
        {
        meth.name = name if name else ident
        meth.parent.addVariable(name)
        }
        #(PARAMETERS (parameter_def[meth])*)
        (throws_clause[meth])?
    ;


method_def [block]
    :   {
        meth = block.newMethod()
        }
        #(METHOD_DEF
            modifiers[meth]
            typ = type_spec[block]
            method_head[meth]
            (statement_list[meth])?
        )
    ;


variable_def [block]
    :   #(VARIABLE_DEF
            modifiers[block]
            typ = type_spec[block]
            dec = var_decl[block]
            val = var_init[block]
        )
        {
        block.addVariable(dec[1])
        if val == noassignment:
            val = ("%s", typeMap.get(typ, "None"))
        block.addSource( ("%s = %s", (dec, val)) )
        }
    ;


parameter_def [meth]
    :   #(PARAMETER_DEF
            modifiers[meth]
            ptype = type_spec[meth]
            ident = identifier[meth]
        ) {meth.addParameter(ptype, ident)}
    ;


obj_init [block]
    :   #(INSTANCE_INIT statement_list[block])
    ;


var_decl [block]
returns [decl]
    :   ident = identifier[block]      {decl = ("%s", ident)}
    |   LBRACK inner = var_decl[block] {decl = ("(%s)", inner)}
    ;


var_init [block]
returns [init = noassignment]
    :   #(ASSIGN init = initializer[block])
    |   // on purpose
    ;


initializer [block]
returns [init]
    :   init = expression[block, False]
    |   init = array_initializer[block]
    ;


array_initializer [block]
returns [init]
    :  #(ARRAY_INIT (init = initializer[block])*)
    ;


throws_clause [block, ident=None]
    :   #("throws" (ident = identifier[block])*)
        {
        if ident:
            block.addModifier("throws %s" % ident)
        }
    ;


identifier [block]
returns [ident]
    :   id0:IDENT
        {
        ident = id0.getText()
        }
    |   #(DOT id1 = identifier[block] id2:IDENT)
        {
        // raise NotImplementedError("DOT identifier" + s)
        }
    ;


identifier_star [block]
returns [ident]
    :   id0:IDENT
        {
        ident = id0.getText()
        }
    |   #(DOT id1 = identifier[block] id2:(STAR|IDENT))
        {
        // raise NotImplementedError("DOT identifier_star")
        }
    ;


statement_list [block]
    :   #(SLIST (statement[block])*)
    ;


statement [block]
    :   typ = type_def[block]
    |   variable_def[block]
    |   exp = expression[block]
    |   #(LABELED_STAT IDENT statement[block])

    |   {
        ifstat = block.newStatement("if")
        elsestat = block.newStatement("else")
        }
        #("if"
            e0 = expression[ifstat, False]
            s0:statement[ifstat]
            (s1:statement[elsestat])?
        )
        {
        ifstat.setExpression(e0)
        }

    |   {
        forstat = block.newStatement("for")
        forex1 = forex2 = forex3 = ""
        }
        #("for"
            #(FOR_INIT ((variable_def[block])+ | forex1=expr_list[block])?)
            #(FOR_CONDITION (forex2=expression[block])?)
            #(FOR_ITERATOR (forex3=expr_list[block])?)
            statement[block]
        )
        {
        forstat.setExpression(("%s", forex1))
        }

    |   {
            s = block.newStatement("while")
        }
        #("while" r=expression[block] statement[block])

    |   {
            s = block.newStatement("do_while")
        }
        #("do" statement[block] r=expression[block])

    |   {
            s = block.newStatement("break")
        }
        #("break" (IDENT)? )

    |   #("continue" (IDENT)? )
        {
            s = block.newStatement("continue")
        }

    |   {
            value = None
        }
        #("return" (value = expression[block, False])? )
        {
        if value is None:
            block.addSource("return")
        else:
            block.addSource(("return %s", value))
        }

    |   #("switch" x=expression[block] (c:case_group[block])*)
        {
            s = block.newStatement("if_switch")
        }

    |   #("throw" exc = expression[block])
        {
            s = block.newStatement("raise")
            s.setExpression(exc)
        }

    |   try_block[block]
    |   statement_list[block]
    |   EMPTY_STAT
    ;


case_group [block]
    :   #(CASE_GROUP
            (#("case" e=expression[block]) | "default")+
            statement_list[block]
        )
    ;


try_block [block]
    :   #("try"
            statement_list[block]
            (handler[block])*
            (#("finally" statement_list[block]))?
        )
    ;


handler [block]
    :   #("catch"
            parameter_def[block]
            statement_list[block]
        )
    ;


expr_list [block]
returns [seq]
    :   #(ELIST
            (exp = expression[block, False]
            {
            if seq:
                seq = ("%s, %s", (("%s", seq), ("%s", exp)))
            else:
                seq = ("%s", exp)
            }
        )*
    )
    ;


expression [block, append=True]
returns [exp]
    :   #(EXPR exp = expr[block])
        {
        if append:
            block.addSource(exp)
        }
    ;


expr [block]
returns [exp = unknown]
    :   #(QUESTION a0=expr[block] b0=expr[block] c0=expr[block])
        {exp = ("(%s %s ", (("%s", b0), ("%s %s", (("if %s", a0), ("else %s)", c0)))))}

    |   #(ASSIGN left=expr[block] right=expr[block])
        {exp = ("%s = %s", (left, right))}

    |   #(PLUS_ASSIGN left=expr[block] right=expr[block])
        {exp = ("%s += %s", (left, right))}

    |   #(MINUS_ASSIGN left=expr[block] right=expr[block])
        {exp = ("%s -= %s", (left, right))}

    |   #(STAR_ASSIGN left=expr[block] right=expr[block])
        {exp = ("%s *= %s", (left, right))}

    |   #(DIV_ASSIGN left=expr[block] right=expr[block])
        {exp = ("%s /= %s", (left, right))}

    |   #(MOD_ASSIGN left=expr[block] right=expr[block])
        {exp = ("%s %= %s", (left, right))}

    |   #(SR_ASSIGN left=expr[block] right=expr[block])
        {exp = ("%s >>= %s", (left, right))}

    |   #(BSR_ASSIGN left=expr[block] right=expr[block])
        // raise an exception during parsing, not at runtime
        {raise NotImplementedError("BSR_ASSIGN")}

    |   #(SL_ASSIGN left=expr[block] right=expr[block])
        {exp = ("%s <<= %s", (left, right))}

    |   #(BAND_ASSIGN left=expr[block] right=expr[block])
        {exp = ("%s &= %s", (left, right))}

    |   #(BXOR_ASSIGN left=expr[block] right=expr[block])
        {exp = ("%s ^= %s", (left, right))}

    |   #(BOR_ASSIGN left=expr[block] right=expr[block])
        {exp = ("%s |= %s", (left, right))}

    |   #(LOR left=expr[block] right=expr[block])
        {exp = ("(%s or %s)", (left, right))}

    |   #(LAND left=expr[block] right=expr[block])
        {exp = ("(%s and %s)", (left, right))}

    |   #(BOR left=expr[block] right=expr[block])
        {exp = ("(%s | %s)", (left, right))}

    |   #(BXOR left=expr[block] right=expr[block])
        {exp = ("(%s ^ %s)", (left, right))}

    |   #(BAND left=expr[block] right=expr[block])
        {exp = ("(%s & %s)", (left, right))}

    |   #(NOT_EQUAL left=expr[block] right=expr[block])
        {exp = ("%s != %s", (left, right))}

    |   #(EQUAL left=expr[block] right=expr[block])
        {exp = ("%s == %s", (left, right))}

    |   #(LT left=expr[block] right=expr[block])
        {exp = ("%s < %s", (left, right))}

    |   #(GT left=expr[block] right=expr[block])
        {exp = ("%s > %s", (left, right))}

    |   #(LE left=expr[block] right=expr[block])
        {exp = ("%s <= %s", (left, bright))}

    |   #(GE left=expr[block] right=expr[block])
        {exp = ("%s >= %s", (left, right))}

    |   #(SL left=expr[block] right=expr[block])
        {exp = ("%s << %s", (left, right))}

    |   #(SR left=expr[block] right=expr[block])
        {exp = ("%s >> %s", (left, right))}

    |   #(BSR left=expr[block] right=expr[block])
        // raise an exception during parsing, not at runtime
        {raise NotImplementedError("BSR")}

    |   #(PLUS left=expr[block] right=expr[block])
        {exp = ("%s + %s", (left, right))}

    |   #(MINUS left=expr[block] right=expr[block])
        {exp = ("%s - %s", (left, right))}

    |   #(DIV left=expr[block] right=expr[block])
        {exp = ("%s / %s", (left, right))}

    |   #(MOD left=expr[block] right=expr[block])
        {exp = ("%s % %s", (left, right))}

    |   #(STAR left=expr[block] right=expr[block])
        {exp = ("%s * %s", (left, right))}

    |   #(INC ex=expr[block])
        {exp = ("%s += 1", ex)}

    |   #(DEC ex=expr[block])
        {exp = ("%s -= 1", ex)}

    |   #(POST_INC ex=expr[block])
        {exp = ("%s += 1", ex)}

    |   #(POST_DEC ex=expr[block])
        {exp = ("%s -= 1", ex)}

    |   #(BNOT ex=expr[block])
        {exp = ("~%s", ex)}

    |   #(LNOT ex=expr[block])
        {exp = ("not %s", ex)}

    |   #("instanceof" obj=expr[block] typ=expr[block])
        {exp = ("isinstance(%s, (%s))", (obj, typ))}

    |   #(UNARY_MINUS uex=expr[block])
        {exp = ("-%s", uex)}

    |   #(UNARY_PLUS uex=expr[block])
        {exp = ("+%s", uex)}

    |   exp = primary_expr[block]
    ;


primary_expr [e]
returns [r = missing]
    :   i0:IDENT
        {
        r = ("%s", i0.getText())
        }

    |   #(DOT
            (x=expr[e]
                (a:IDENT
                    | array_index[e]
                    | "this"
                    | "class"
                    | #("new" k:IDENT el0=expr_list[e] )
                    | "super"
                )
                | #(ARRAY_DECLARATOR type_spec_array[e])
                | t = builtin_type[e]("class")?
            )
        )
        {
        r = ("%s.%s", (x, ("%s", a.getText())))
        }

    |   array_index[e]

    |   #(METHOD_CALL pex = primary_expr[e] el44=expr_list[e])
        {
        if el44:
            r = ("%s(%s)", (pex, el44))
        else:
            r = ("%s()", pex)
        }

    |   call = ctor_call[e]
        {
        r = ("%s", call)
        }

    |   #(TYPECAST ts3=type_spec[e] ex3=expr[e])
        {
        r = ("%s", ex3)
        }

    |   ex = new_expression[e] 
        {
        r = ("%s", ex)
        }

    |   con = constant[e]
        {
        r = ("%s", con)
        }

    |   "super" {r = ("%s", "super"  )}
    |   "true"  {r = ("%s", "True"   )}
    |   "false" {r = ("%s", "False"  )}
    |   "this"  {r = ("%s", "self"   )}
    |   "null"  {r = ("%s", "None"   )}

    // type name used with instanceof
    |   typ = type_spec[e] 
        {r = ("%s", typ)}
    ;


ctor_call [block]
returns [seq=()]
    :   #(cn:CTOR_CALL seq=expr_list[block] )
        {
        print "#@#@@@", cn
        }

    |   #(SUPER_CTOR_CALL
            (el0=expr_list[block]
                | p=primary_expr[block] el2=expr_list[block]
            )
            {raise NotImplementedError("SUPER_CTOR_CALL")}
        )
    ;


array_index [block]
    :   #(INDEX_OP 
            r = expr[block] 
            e = expression[block]
        )
        {
        block.addSource("%s[%s]" % (r, e))
        }
    ;


constant [block]
returns [value]
    :   i0:NUM_INT        {value = i0.getText()}
    |   c0:CHAR_LITERAL   {value = c0.getText()}
    |   s0:STRING_LITERAL {value = s0.getText()}
    |   f0:NUM_FLOAT      {value = f0.getText()}
    |   d0:NUM_DOUBLE     {value = d0.getText()}
    |   l0:NUM_LONG       {value = l0.getText()}
    ;


new_expression [block]
returns [value = missing]
    {
    exp = ()
    }
    :   #("new"
            typ = type[block] 
            (new_array_declarator[block]
                ( arrexp = array_initializer[block])?
                | exp = expr_list[block] (obj_block[block])?
            )
        )
        {

        if exp:
            value = ("%s(%s)", (("%s", typ), ("%s", exp)))
        elif typ in typeMap:
            value = ("%s", typeMap[typ])
        else:
            value = ("%s()", typ)
        }
    ;


new_array_declarator [block]
    :   #(ARRAY_DECLARATOR
            (new_array_declarator[block])? 
            (e=expression[block])?
        )
    ;
