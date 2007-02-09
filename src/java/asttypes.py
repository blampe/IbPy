#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
todo:  add property get/set on duplicate method names
       indent long method signatures
       reorder class statements to place inner classes first
       add property for some modifiers (e.g., syncronized)

"""
from cStringIO import StringIO

import astextra
import walker


I = ' '*4
typeMap = {
    'String':"''",
    'int':'0',
    'double':'0.0',
    'Vector':'[]',
    }
renameMap = {
    'this':'self',
    'null':'None',
    'false':'False',
    'true':'True',
    'equals':'__eq__',
    }
conflictRenameMap = {
    '__init__':'new',
}


def rename(item):
    try:
        return renameMap[item]
    except (KeyError, ):
        pass
    ##item = item.replace('p_', '').replace('m_', '')
    return item


class Source(list):
    isClass = isMethod = False
    
    def __init__(self, name=''):
        list.__init__(self)
        self.name = name
        self.decls = set()
        self.modifiers = set()
        
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

    def addComment(self, text):
        comment = '## %s' % (text, )
        self.append(comment)

    def addNewLine(self):
        self.append('')
    
    def newClass(self):
        c = Class(self)
        self.append(c)
        return c

    def newMethod(self, name=''):
        m = Method(self)
        m.name = name
        self.append('')
        self.append(m)
        return m

    def newExpression(self):
        e = Expression(self)
        self.append(e)
        return e

    def newStatement(self, name):
        s = Statement(self, name)
        self.append(s)
        return s

    def addDecl(self, name):
        self.decls.add(name)

    def fixDecl(self, *decls):
        if self.isMethod:
            r = []
            for d in decls:
                if d in self.parent.decls:
                    d = 'self.%s' % (d, )
                r.append(d)
        else:
            r = decls
        if len(r) == 1:
            return r[0]
        else:
            return tuple(r)

    def setType(self, node):
        #self.typ = node
        pass

    def addModifier(self, mod):
        if mod:
            self.modifiers.add(mod)


class Module(Source):
    def __init__(self, infile, outfile):
        Source.__init__(self)
        self.infile = infile
        self.outfile = outfile
        self.addSheBang()
        self.addNewLine()
        self.addMainComment()
        self.addNewLine()
        self.addHeading()
        self.append('')
        
    def addSheBang(self):
        self.append('#!/usr/bin/env python')
        self.append('# -*- coding: utf-8 -*-')
        
    def addMainComment(self):
        self.addComment('')
        self.addComment('source: "%s"' % (self.infile, ))
        self.addComment('target: "%s"' % (self.outfile, ))
        self.addComment('')        
        self.addComment('input source code copyright original author(s)')
        self.addComment('output source code (this file) copyright Troy Melhase <troy@gci.net>')        
        self.addComment('')        

    def addHeading(self):
        for line in astextra.headings.get(self.infile, ()):
            self.append(line)


class Method(Source):
    isMethod = True
    
    def __init__(self, parent):
        Source.__init__(self)
        self.parent = parent
        self.params = ['self', ]
        
    def writeTo(self, output, indent):
        params = str.join(', ', self.params)
        name = rename(self.name)
        if self.modifiers:
            output.write('%s## modifiers: %s\n' % (I*indent, str.join(',', self.modifiers)))
        output.write('%sdef %s(%s):\n' % (I*indent, name, params))
        Source.writeTo(self, output, indent+1)

    def addParameter(self, node):
        try:
            param = node.getText()
        except (AttributeError, ):
            param = node
        param = rename(param)
        self.params.append(param)


class Class(Source):
    isClass = True
    
    def __init__(self, parent):
        Source.__init__(self)
        self.parent = parent
        self.classvars = set()
        
    def writeTo(self, output, indent):
        output.write('%sclass %s:\n' % (I*indent, self.name, ))
        Source.writeTo(self, output, indent+1)

    def addParameter(self, *a, **b):
        print '#### warning:  Class.addParameter called (', a, ')'

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
            
        if self.parent.isClass:
            self.parent.classvars.add(left)
        elif self.parent.isMethod:
            if self.parent.parent.isClass:
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
        
    def __writeTo(self, output, indent):
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
        if self.parent.isMethod:
            indent += 1
        Source.writeTo(self, output, indent)

    def toString(self):
        out = StringIO()
        self.writeTo(out, 0)
        return out.getvalue()
    
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


class Statement(Source):
    def __init__(self, parent, name=''):
        Source.__init__(self, name)
        self.parent = parent
        self.expr = None
        
    def writeTo(self, output, indent):
        output.write('%s%s' % (I*(indent), self.name))
        if self.expr is not None:
            output.write(' %s' % (self.expr, ))
        if self.isBlock:
            output.write(':')
        output.write('\n')
        Source.writeTo(self, output, indent+1)

    def setExpression(self, e):
        self.expr = e

        

    @property
    def isBlock(self):
        return self.name in ('if', 'while', 'for', 'else', 'elif')
