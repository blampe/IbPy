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
class walker extends TreeParser;
options { importVocab = Java; }


walk [source]
    :   (pkg = package_def[source] )?
        (imp = import_def[source]  )*
        (typ = type_def[source]    )*
    ;


package_def [block]
returns [defn]
    :   #(PACKAGE_DEF defn = identifier[block])
        {block.addSource(("### package %s", defn))}
    ;


import_def [block]
returns [defn]
    :   #(IMPORT defn = identifier_star[block])
        {block.addSource(("### import %s", defn))}
    ;


type_def [block]
returns [klass = block.newClass()]
    :   #(CLASS_DEF
          modifiers[klass]
          name = identifier[klass] {klass.setName(name)}
          ext_clause = extends_clause[klass]
          imp_clause = implements_clause[klass]
          obj_block[klass]
        )
    |   #(INTERFACE_DEF
          modifiers[klass]
          name = identifier[klass] {klass.setName(name)}
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
            spec = block.typeTypeMap[value]
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
    :   typ = identifier[block]   {block.type = typ}
    |   typ = builtin_type[block] {block.type = typ}
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
        ) {meth.type = typ}
    ;


method_head [meth, name=None]
    :   ident = identifier[meth]
        {
        meth.setName(name if name else ident)
        meth.parent.addVariable(meth.name)
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
        if val == block.emptyAssign:
            val = ("%s", block.typeValueMap.get(typ, "%s()" % typ))
        block.addSource( ("%s = %s", (dec, val)) )
        }
    ;


parameter_def [meth, add=True]
    :   #(PARAMETER_DEF
            modifiers[meth]
            ptype = type_spec[meth]
            ident = identifier[meth]
        )
        {
        if add:
            meth.addParameter(ptype, ident)
        else:
            meth.setExpression(("(%s, ), %s", (("%s", ptype), ("%s", ident))))
        }
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
returns [init = block.emptyAssign]
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
    :   id0:IDENT {ident = id0.getText()}
    |   {
        exp = ()
        }
        #(DOT exp = identifier[block] id1:IDENT)
        {
        if exp:
            ident = ("%s.%s", (("%s", exp), ("%s", id1.getText())))
        else:
            ident = id1.getText()
        }
    ;


identifier_star [block]
returns [ident]
    :   id0:IDENT {ident = id0.getText()}
    |   {
        exp = ()
        }
        #(DOT exp = identifier[block] id1:(STAR|IDENT))
        {
        if exp and id1:
            ident = ("%s.%s", (("%s", exp), ("%s", id1.getText())))
        elif exp:
            ident = ("%s.%s", (("%s", exp), ("%s", "*")))
        else:
            ident = id1
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
        if_stat = block.newStatement("if")
        else_stat = block.newStatement("else")
        }
        #("if"
            if_expr = expression[if_stat, False]
            statement[if_stat]
            (statement[else_stat])?
        )
        {
        if_stat.setExpression(if_expr)
        }


    |   {
        block.addSource("")
        block.addComment("for-while")
        for_init, for_stat = block.newFor()
        }
        #("for"
            #(FOR_INIT
                ((variable_def[for_init])+ | for_exp = expr_list[for_init])?)
            #(FOR_CONDITION (for_cond = expression[for_stat, False])?)
            #(FOR_ITERATOR  (for_iter = expr_list[for_stat, False])?)
            statement[for_stat]
        )
        {
        for_stat.setExpression(("%s", for_cond))
        for_stat.addSource(("%s", for_iter))
        }


    |   {
        while_stat = block.newStatement("while")
        }
        #("while" while_expr = expression[block, False] 
                  statement[while_stat])
        {
        while_stat.setExpression(while_expr)
        }


    |   #("do" statement[block] do_exp = expression[block])
        {raise NotImplementedError("do statement")}


    |   {
        break_stat = block.newStatement("break")
        break_label = block.missingValue
        }
        #("break" (break_label:IDENT)? )
        {
        if break_label is not block.missingValue:
            raise NotImplementedError("break with label")
        }



    |   {
        continue_stat = block.newStatement("continue")
        continue_label = block.missingValue
        }
        #("continue" (continue_label:IDENT)? )
        {
        if continue_label is not block.missingValue:
            raise NotImplementedError("continue with label")
        }


    |   {
        return_value = None
        }
        #("return" (return_value = expression[block, False])? )
        {
        if return_value in (None, ("%s", "None")):
            block.addSource("return")
        else:
            block.addSource(("return %s", return_value))
        }


    |   {
        switch_block = block.newSwitch()
        }
        #("switch" switch_expr = expression[block, False]
                   (c:case_group[block, switch_expr])*
        )


    |   {
        raise_stat = block.newStatement("raise")
        }
        #("throw" raise_exp = expression[block])
        {
        raise_stat.setExpression(raise_exp)
        }

    |   try_block[block]
    |   statement_list[block]
    |   EMPTY_STAT
    ;


case_group [block, switch_expr]
    :   {
        other = block.newStatement("elif")
        right = block.missingValue
        }
        #(CASE_GROUP
            (#("case" 
               right = expression[other, False]) | "default")+
               statement_list[other]
        )
        {
        if right is block.missingValue:
            other.setName("else")
            other.setExpression(None)
        else:
            other.setExpression(("%s == %s", (switch_expr, ("%s", right))))
        }
    ;


try_block [block]
    {
    try_stat = block.newStatement("try")
    except_stat = block.newStatement("except")
    finally_stat = block.newStatement("finally")
    }

    :   #("try"
            statement_list[try_stat]
            (handler[except_stat])*
            (#("finally" statement_list[finally_stat]))?
        )
    ;


handler [block]
    :   #("catch"
            parameter_def[block, False]
            statement_list[block]
        )
    ;


expr_list [block, append=False]
returns [seq]
    :   #(ELIST
            (exp = expression[block, append]
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
returns [exp = block.unknownExpression]
    :   #(QUESTION a0=expr[block] b0=expr[block] c0=expr[block])
        {exp = ("%s %s ", (("%s", b0), ("%s %s", (("if %s", a0), ("else %s", c0)))))}

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
        {exp = ("%s or %s", (left, right))}

    |   #(LAND left=expr[block] right=expr[block])
        {exp = ("%s and %s", (left, right))}

    |   #(BOR left=expr[block] right=expr[block])
        {exp = ("%s | %s", (left, right))}

    |   #(BXOR left=expr[block] right=expr[block])
        {exp = ("%s ^ %s", (left, right))}

    |   #(BAND left=expr[block] right=expr[block])
        {exp = ("%s & %s", (left, right))}

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


primary_expr [block]
returns [exp = block.missingValue]
    :   i0:IDENT {exp = ("%s", i0.getText())}

    |   {x = ""}
        #(DOT
            (x=expr[block]
                (a:IDENT
                    | index = array_index[block]
                    | "this"
                    | a0:"class"
                    | #("new" k:IDENT el0=expr_list[block] )
                    | "super"
                )
                | #(ARRAY_DECLARATOR type_spec_array[block])
                | t = builtin_type[block]("class")?
            )
        )
        {
        if a:
            exp = ("%s.%s", (x, ("%s", a.getText())))
        }

    |   index = array_index[block] {exp = index}

    |   #(METHOD_CALL pex = primary_expr[block] el44=expr_list[block])
        {
        if el44:
            exp = ("%s(%s)", (pex, el44))
        else:
            exp = ("%s()", pex)
       }

    |   call = ctor_call[block] {exp = ("%s", call)}

    |   #(TYPECAST type_cast = type_spec[block] cast_exp = expr[block])
        {exp = ("%s", cast_exp)}

    |   other_exp = new_expression[block] {exp = ("%s", other_exp)}
    |   con = constant[block] {exp = ("%s", con)}
    |   "super" {exp = ("%s", "super"  )}
    |   "true"  {exp = ("%s", "True"   )}
    |   "false" {exp = ("%s", "False"  )}
    |   "this"  {exp = ("%s", "self"   )}
    |   "null"  {exp = ("%s", "None"   )}
    // type name used with instanceof
    |   typ = type_spec[block] {exp = ("%s", typ)}
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
returns [index]
    :   #(INDEX_OP 
            array_exp = expr[block] 
            index_exp = expression[block, False]
        )
        {
        index = ("%s[%s]", (array_exp, index_exp))
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
returns [value = block.missingValue]
    {
    exp = ()
    arrexp = None
    arrdecl = None
    }
    :   #("new"
            typ = type[block] 
            (arrdecl = new_array_declarator[block]
                ( arrexp = array_initializer[block])?
                | exp = expr_list[block] (obj_block[block])?
            )
        )
        {
        if arrdecl:
            value = ("[%s() for __idx0 in range(%s)]", (("%s", typ), ("%s", arrdecl)))
        elif exp:
            value = ("%s(%s)", (("%s", typ), ("%s", exp)))
        elif typ in block.typeValueMap:
            value = ("%s", block.typeValueMap[typ])
        else:
            value = ("%s()", typ)
        }
    ;


new_array_declarator [block]
returns [exp = None]
    :   #(ad0:ARRAY_DECLARATOR
            (exp = new_array_declarator[block])? 
            (exp = expression[block, False])?
        )
    ;
