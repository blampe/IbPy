#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cStringIO import StringIO

import astextra
import walker


I = ' '*4
typeMap = {
    'String':"''",
    'int':'0',
    'double':'0.0',
    }


renameMap = {
    'this':'self',
    'null':'None',
    'false':'False',
    'true':'True',
    }


def rename(item):
    try:
        return renameMap[item]
    except (KeyError, ):
        pass
    item = item.replace('p_', '').replace('m_', '')
    return item


class Source(list):
    def __init__(self, name=''):
        list.__init__(self)
        self.name = name

    def __str__(self):
        out = StringIO()
        self.writeTo(out, 0)
        return out.getvalue()

    def writeTo(self, output, indent):
        for obj in self:
            if callable(obj):
                obj = obj()
            try:
                obj.writeTo(output, indent)
            except (AttributeError, ):
                output.write('%s%s\n' % (indent*I, obj))

    def addComment(self, node):
        try:
            text = node.getText()
        except (AttributeError, ):
            text = node
        comment = '## %s' % (text, )
        self.append(comment)

    def addNewLine(self):
        self.append('')

    def isExpression(self):
        return (self.__class__ is Expression)

    def isClass(self):
        return (self.__class__ is Class)

    def isMethod(self):
        return (self.__class__ is Method)
    
    def newClass(self):
        c = Class(self)
        self.addNewLine()
        self.append(c)
        return c

    def newMethod(self):
        m = Method(self)
        self.addNewLine()
        self.append(m)
        return m

    def newExpression(self):
        e = Expression(self)
        self.append(e)
        return e

    def newIf(self):
        i = If(self)
        self.append(i)
        return i
    
    def setName(self, node):
        if self.name:
            return
        try:
            name = node.getText()
        except (AttributeError, ):
            name = node
        self.name = name

class Module(Source):
    def __init__(self, infile, outfile):
        Source.__init__(self)
        self.infile = infile
        self.outfile = outfile
        self.addSheBang()
        self.addNewLine()
        self.addMainComment()
        self.addNewLine()
        self.addExtraImports()
        self.append('')
        
    def addSheBang(self):
        self.append('#!/usr/bin/env python')
        self.append('# -*- coding: utf-8 -*-')
        
    def addMainComment(self):
        self.addComment('')
        self.addComment('source: "%s"' % (self.infile, ))
        self.addComment('input source code copyright original author(s)')
        self.addComment('')    
        self.addComment('target: "%s"' % (self.outfile, ))
        self.addComment('output source code (this file) copyright Troy Melhase <troy@gci.net>')        
        self.addComment('')        

    def addExtraImports(self):
        imports = astextra.imports.get(self.infile, [])
        for line in imports:
            self.append(line)


class Method(Source):
    def __init__(self, parent):
        Source.__init__(self)
        self.parent = parent
        self.params = ['self', ]

    def writeTo(self, output, indent):
        params = str.join(', ', self.params)        
        output.write('%sdef %s(%s):\n' % (I*indent, self.name, params))
        Source.writeTo(self, output, indent)

    def addParameter(self, node):
        param = node.getText()
        param = rename(param)
        self.params.append(param)


class Class(Source):
    def __init__(self, parent):
        Source.__init__(self)
        self.parent = parent
        self.classvars = set()
        
    def writeTo(self, output, indent):
        output.write('%sclass %s:\n' % (I*indent, self.name, ))
        Source.writeTo(self, output, indent+1)
        
    def addVariableDef(self, typ, name, init):
        if name:
            self.classvars.add(name.getText().strip())
        #Source.addVariableDef(self, typ, name, init)


class Expression(Source):
    def __init__(self, parent):
        Source.__init__(self)
        self.parent = parent
        self.expr = []
        self.typ = None
        self.switch = None
        self.right = self.left = self.op = None
        self.prefix = self.suffix = ''
        
    def setLeft(self, node):
        try:
            left = node.getText()
        except (AttributeError, ):
            left = node
            
        if self.parent.isClass():
            self.parent.classvars.add(left)
        elif self.parent.isMethod():
            if self.parent.parent.isClass():
                if left in self.parent.parent.classvars:
                    left = 'self.%s' % (left, )
        left = rename(left)
        self.left = left
            
    def setType(self, node):
        self.typ = node.getText()

    def setOp(self, op):
        self.op = op

    def setRight(self, node):
        try:
            right = node.getText()
        except (AttributeError, ):
            right = node
        self.right = rename(right)
        
    def setExpression(self, left, op, right):
        try:
            if right.getType() == walker.LITERAL_new:
                right = '%s()' % (right.getFirstChild().getText(), )
        except (AttributeError, ):
            pass
        self.setLeft(left)
        self.setOp(op)
        self.setRight(right)
        
    def writeTo(self, output, indent):
        left = self.left
        op = self.op
        right = self.right
        typ = self.typ
        if right is None:
            right = typeMap.get(typ, None)
        if not (left == right == op == None):
            if self.prefix:
                prefix = '%s ' % (self.prefix)
            else:
                prefix = ''
            suffix = self.suffix
            self.append('%s%s %s %s%s' % (prefix, left, op, right, suffix))
        if self.parent.isMethod():
            indent += 1
        Source.writeTo(self, output, indent)

        
    @property
    def classvars(self):
        p = self.parent
        while p:
            if hasattr(p, 'parent'):
                p = p.parent
            else:
                break
        return getattr(p, 'classvars', ())


    def setPrefix(self, value):
        self.prefix = value

    def setSuffix(self, value):
        self.suffix = value

class If(Expression):
    def setClause(self, *v):
        return
        print "#####",
        for a in v:
            #print a.getType(), a.getText(),
            print a
            print
        
