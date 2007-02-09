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


options {
    language=Python;
}


/* our module statements  */ {
from asttypes import Module, typeMap
noassignment = "<noassign>"
missing = "<missing>"
unknown = "<unknown>"

}


class walker extends TreeParser;


options {
    importVocab = Java;
}


/* our method for starting a walk */
module [infile, outfile]
returns [mod = Module(infile, outfile)]
    : (pkg = package_def[mod])?
      (imp = import_def[mod])*
      (typ = type_def[mod])*
    ;


package_def [block]
returns [definition = ""]
    : #(PACKAGE_DEF definition = identifier[block])
    ;


import_def [block]
returns [definition = ""]
    : #(IMPORT definition = identifier_star[block] )
    ;


type_def [block]
returns [klass = block.newClass()]
    : #(CLASS_DEF
          modifiers[klass]
          name = identifier[klass] {klass.name = name}
          ext_clause = extends_clause[klass]
          imp_clause = implements_clause[klass]
          obj_block[klass]
       )
    | #(INTERFACE_DEF
          modifiers[klass]
          name = identifier[klass] {klass.name = name}
          ext_clause = extends_clause[klass]
          interface_block[klass]
       )
    ;


type_spec [block]
returns [spec]
    : #(type0:TYPE type_spec_array[block])
          {spec = type0.getFirstChild().getText()}
    ;


type_spec_array [block]
    : #(ARRAY_DECLARATOR type_spec_array[block])
    | spec = type[block]
    ;


type [block]
returns [typ]
    : typ = identifier[block]   {block.setType(typ)}
    | typ = builtin_type[block] {block.setType(typ)}
    ;


builtin_type [block]
returns [typ]
    : v0:"void"    {typ = v0.getText()}
    | b0:"boolean" {typ = "bool"}
    | y0:"byte"    {typ = y0.getText()}
    | c0:"char"    {typ = c0.getText()}
    | s0:"short"   {typ = s0.getText()}
    | i0:"int"     {typ = i0.getText()}
    | f0:"float"   {typ = f0.getText()}
    | l0:"long"    {typ = l0.getText()}
    | d0:"double"  {typ = d0.getText()}
    ;


modifiers [block, mod=None]
    : #(MODIFIERS (mod = modifier[block])*) {block.addModifier(mod)}
    ;


modifier [block]
returns [mod]
    : pri0:"private"       {mod = pri0.getText()}
    | pub0:"public"        {mod = pub0.getText()}
    | pro0:"protected"     {mod = pro0.getText()}
    | sta0:"static"        {mod = sta0.getText()}
    | tra0:"transient"     {mod = tra0.getText()}
    | fin0:"final"         {mod = fin0.getText()}
    | abt0:"abstract"      {mod = abt0.getText()}
    | nat0:"native"        {mod = nat0.getText()}
    | ths0:"threadsafe"    {mod = ths0.getText()}
    | syn0:"synchronized"  {mod = syn0.getText()}
    | con0:"const"         {mod = con0.getText()}
    | vol0:"volatile"      {mod = vol0.getText()}
    | sfp0:"strictfp"      {mod = sfp0.getText()}
    ;


extends_clause [block]
returns [clause=None]
    : #(EXTENDS_CLAUSE (clause=identifier[block])* )
      {block.addBaseClass(clause)}
    ;


implements_clause [block]
returns [clause=None]
    : #(IMPLEMENTS_CLAUSE (clause=identifier[block])* )
      {block.addBaseClass(clause)}
    ;


interface_block [block]
    : #(OBJBLOCK
           (method_decl[block]
            |variable_def[block]
            |typ = type_def[block]
        )*
    )
    ;


obj_block [block]
    : #(OBJBLOCK
           (ctor_def[block]
            | method_def[block]
            | variable_def[block]
            | typ = type_def[block]
            | #(STATIC_INIT slist[block])
            | #(INSTANCE_INIT slist[block])
        )*
    )
    ;


ctor_def [block]
    {meth = block.newMethod()}
    : #(CTOR_DEF modifiers[meth]
                 method_head[meth]
                 (slist[meth])?)
        {meth.name = "__init__"}
    ;


method_decl [block]
    {
    meth = block.newMethod()
    meth.addSource("raise NotImplementedError()")
    }
    : #(METHOD_DEF modifiers[meth]
                   t=type_spec[meth]
                   method_head[meth])
    ;


method_head [meth]
    : i = identifier[meth]
      {
       meth.name = i
       meth.parent.addVariable(i)
      }
      #(PARAMETERS (parameter_def[meth])* ) (throws_clause[meth])?
    ;


method_def [block]
    {meth = block.newMethod()}
    : #(METHOD_DEF modifiers[meth]
                   typ = type_spec[block]
                   method_head[meth]
                   (slist[meth])?)
    ;


variable_def [block]
    : #(VARIABLE_DEF modifiers[block]
                     t = type_spec[block]
                     d = var_decl[block]
                     v = var_init[block])
        {
            block.addVariable(d)
            d = ("%s", d)
            if v == noassignment:
                v = typeMap.get(t, None)
            block.addSource(("%s = %s", d, v))
        }

    ;


parameter_def [meth]
    : #(PARAMETER_DEF
          modifiers[meth]
          ptype = type_spec[meth]
          ident = identifier[meth]) {meth.addParameter(ident)}
    ;


object_init [block]
    : #(INSTANCE_INIT slist[block])
    ;


var_decl [block]
returns [decl]
    : decl = identifier[block]
    | LBRACK inner = var_decl[block] { decl = "(%s)" % inner  }
    ;


var_init [block]
returns [init = noassignment]
    : #(ASSIGN init = initializer[block])
    | // on purpose
    ;


initializer [block]
returns [init]
    : init = expression[block, False]
    | init = array_initializer[block]
    ;


array_initializer [block]
returns [init]
    : #(ARRAY_INIT (init = initializer[block])*)
    ;


throws_clause [block, ident=None]
    : #("throws" (ident = identifier[block])*)
      { if ident:
            block.addModifier("throws %s" % ident)
      }
    ;


identifier [block]
returns [ident]
    : id0:IDENT {ident = id0.getText()}
    | #(DOT id1 = identifier[block] id2:IDENT)
          {ident = "%s.%s" % (id1, id2.getText())}
    ;


identifier_star [block]
returns [ident]
    : id0:IDENT {ident = id0.getText()}
    | #(DOT id1 = identifier[block] id2:(STAR|IDENT))
          // needs work
          {ident = "%s ****** %s" % (id1, id2)}
    ;


slist [block]
    : #(SLIST (stat[block])*)
    ;


stat [block]
    : typ = type_def[block]
    | variable_def[block]
    | exp = expression[block]
    | #(LABELED_STAT IDENT stat[block])

    | {
          s = block.newStatement("if")
          t = block.newStatement("else")
      }
      #("if" e0=expression[s, False] s0:stat[s] (s1:stat[t])? )
      {
          s.setExpression(e0)
      }


    | #("for"
          #(FOR_INIT ((variable_def[block])+ | el0=elist[block])?)
          #(FOR_CONDITION (r=expression[block])?)
          #(FOR_ITERATOR (el1=elist[block])?)
          stat[block]
        )
        {
            s = block.newStatement("for")
        }

    | #("while" r=expression[block] stat[block])
      {
          s = block.newStatement("while")
      }

    | #("do" stat[block] r=expression[block])
      {
          s = block.newStatement("do-while")
      }

    | #("break" (IDENT)? )
      {
          s = block.newStatement("break")
      }

    | #("continue" (IDENT)? )
      {
          s = block.newStatement("continue")
      }

    | {r = None }
      #("return" (r=expression[block, False])? )
      {
      if r is None:
          block.addSource("return")
      else:
          block.addSource(("return %s", r))
      }


    | #("switch" x=expression[block] (c:case_group[block])*)
      {
          s = block.newStatement("if-switch")
      }

    | #("throw" x=expression[block])
      {
          s = block.newStatement("raise")
      }

    | try_block[block]
    | slist[block]
    | EMPTY_STAT
    ;


case_group [block]
    : #(CASE_GROUP
          (#("case" e=expression[block]) | "default")+
           slist[block]
          )
    ;



try_block [block]
    : #("try" slist[block] (handler[block])* (#("finally" slist[block]))?)
    ;



handler [block]
    : #("catch" parameter_def[block] slist[block])
    ;


elist [block]
returns [seq=()]
{
ex = []
}
    : #(ELIST (r = expression[block, False]
           {
           ex.append(r)
           }
       )*
    )
        {
            seq = ("%s", ) + tuple(ex)
        }
    ;


expression [block, append=True]
returns [exp]
    : #(EXPR exp = expr[block])
    {if append:block.addSource(exp)}
    ;


expr  [block]
returns [exp = unknown]

    // trinary operator
    : #(QUESTION a0=expr[block] b0=expr[block] c0=expr[block])
      {exp = ("(%s and %s or %s)", a0, b0, c0)}

    // binary operators
    | #(ASSIGN left=expr[block] right=expr[block])
      {exp = ("%s = %s", left, right)}

    | #(PLUS_ASSIGN left=expr[block] right=expr[block])
      {exp = ("%s += %s", left, right)}

    | #(MINUS_ASSIGN left=expr[block] right=expr[block])
      {exp = ("%s -= %s", left, right)}

    | #(STAR_ASSIGN left=expr[block] right=expr[block])
      {exp = ("%s *= %s", left, right)}

    | #(DIV_ASSIGN left=expr[block] right=expr[block])
    | #(MOD_ASSIGN left=expr[block] right=expr[block])
    | #(SR_ASSIGN left=expr[block] right=expr[block])
    | #(BSR_ASSIGN left=expr[block] right=expr[block])
    | #(SL_ASSIGN left=expr[block] right=expr[block])
    | #(BAND_ASSIGN left=expr[block] right=expr[block])
    | #(BXOR_ASSIGN left=expr[block] right=expr[block])
    | #(BOR_ASSIGN left=expr[block] right=expr[block])

    | #(LOR left=expr[block] right=expr[block])
      {exp = ("(%s or %s)", left, right)}

    | #(LAND left=expr[block] right=expr[block])
      {exp = ("(%s and %s)", left, right)}

    | #(BOR left=expr[block] right=expr[block])
    | #(BXOR left=expr[block] right=expr[block])
    | #(BAND left=expr[block] right=expr[block])
    | #(NOT_EQUAL left=expr[block] right=expr[block])
      {exp = ("%s != %s", left, right)}

    | #(EQUAL left=expr[block] right=expr[block])
      {exp = ("%s == %s", left, right)}

    | #(LT left=expr[block] right=expr[block])
      {exp = ("(%s < %s)", left, right)}

    | #(GT left=expr[block] right=expr[block])
      {exp = ("(%s > %s)", left, right)}

    | #(LE left=expr[block] right=expr[block])
      {exp = ("(%s <= %s)", left, right)}

    | #(GE left=expr[block] right=expr[block])
      {exp = ("(%s >= %s)", left, right)}

    // shift left, shift right
    | #(SL left=expr[block] right=expr[block])
    | #(SR left=expr[block] right=expr[block])
    | #(BSR left=expr[block] right=expr[block])

    | #(PLUS left=expr[block] right=expr[block])
      {exp = ("(%s + %s)", left, right)}

    | #(MINUS left=expr[block] right=expr[block])
      {exp = ("(%s - %s)", left, right)}

    | #(DIV left=expr[block] right=expr[block])
      {exp = ("(%s / %s)", left, right)}

    | #(MOD left=expr[block] right=expr[block])
      {exp = ("(%s % %s)", left, right)}

    | #(STAR left=expr[block] right=expr[block])
      {exp = ("(%s * %s)", left, right)}

    | #(INC left=expr[block])
      {exp = ("%s += 1", left)}

    | #(DEC left=expr[block])
      {exp = ("%s -= 1", left)}

    | #(POST_INC left=expr[block])
      {exp = ("%s += 1", left)}

    | #(POST_DEC left=expr[block])
      {exp = ("%s -= 1", left)}

    | #(BNOT left=expr[block])
      {exp = ("~%s", left)}

    | #(LNOT left=expr[block])
      {exp = ("not %s", left)}

    | #("instanceof" left=expr[block] right=expr[block])
      {exp = ("isinstance(%s, (%s))", left, right)}

    | #(UNARY_MINUS right=expr[block])
      {exp = ("-%s", right)}

    | #(UNARY_PLUS left=expr[block])
      {exp = ("+%s", right)}

    | exp = primary_expr[block] {exp = ("%s", exp)}
    ;


primary_expr [e]
returns [r=missing]
    : j:IDENT { r = j.getText() }
    | #(DOT
           (x=expr[e]
               (a:IDENT
                | array_index[e]
                | "this"
                | "class"
                | #("new" k:IDENT el0=elist[e] )
                | "super"
                )
            | #(ARRAY_DECLARATOR type_spec_array[e])
            | t = builtin_type[e]("class")?
            )
        ) {r = ("%s.%s", x, a.getText())}

    | array_index[e]
    | #(METHOD_CALL r = primary_expr[e] el2=elist[e])
          {
          if not el2 and isinstance(el2, tuple):
              r = ("%s()", r)
          else:
              r = ("%s(%s)", r, el2)
          }

    | ctor_call[e] {r = "()" }
    | #(TYPECAST t=type_spec[e] r=expr[e]) {r = ("%s", r)}
    | r = new_expression[e] {r = ("%s", r)}
    | r = constant[e] {r = ("%s", r)}
    | "super"
    | "true"  {r = "True"  }
    | "false" {r = "False" }
    | "this"  {r = "self"  }
    | "null"  {r = "None"  }
    // type name used with instanceof
    | t = type_spec[e]
    ;


ctor_call [block]
    : #(CTOR_CALL el0=elist[block] )
    | #(SUPER_CTOR_CALL
           (el0=elist[block]
            | p=primary_expr[block] el2=elist[block]
            )
       )
    ;


array_index [block]
    : #(INDEX_OP 
          r = expr[block] 
          e = expression[block]
          )
      {block.addSource("%s[%s]" % (r, e))}
    ;


constant [block]
returns [value]
    : i0:NUM_INT        {value = i0.getText()}
    | c0:CHAR_LITERAL   {value = c0.getText()}
    | s0:STRING_LITERAL {value = s0.getText()}
    | f0:NUM_FLOAT      {value = f0.getText()}
    | d0:NUM_DOUBLE     {value = d0.getText()}
    | l0:NUM_LONG       {value = l0.getText()}
    ;


new_expression [block]
returns [value = missing]
{
el = ()
}
    : #("new" typ=type[block] 
           (new_array_declarator[block] (a=array_initializer[block])?
            | el=elist[block] (obj_block[block])?
            )
       )
       {value=("%s", el)}
//typeMap.get(typ, typ+"(%s)" % (el, )))}
    ;


new_array_declarator [block]
    : #(ARRAY_DECLARATOR (new_array_declarator[block])? 
                         (e=expression[block])?
       )
    ;
