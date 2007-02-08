#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cStringIO import StringIO

import walker


I = ' '*4
typeMap = {
    'String':"''",
    'int':'0',
    'double':'0.0',
    }


class Source(list):
    def __init__(self, name=''):
        list.__init__(self)
        self.name = name

    def show(self, *nodes):
        for node in nodes:
            print '###', node
        
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
        if isinstance(node, basestring):
            text = node
        elif node:
            text = node.getText()
        else:
            text = '<emtpy>'
        comment = '## %s' % (text, )
        self.append(comment)

    def addNewLine(self):
        self.append('')

    def isExpression(self):
        return self.__class__ is Expression

    def isClass(self):
        return self.__class__ is Class

    def isMethod(self):
        return self.__class__ is Method
    
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
    
    def setName(self, node):
        if not self.name:
            self.name = node.getText()

    def setType(self, node):
        pass

class Module(Source):
    def __init__(self):
        Source.__init__(self)
        self.addSheBang()
        self.addNewLine()
        self.addMainComment()
        self.addNewLine()

    def addSheBang(self):
        self.append('#!/usr/bin/env python')
        self.append('# -*- coding: utf-8 -*-')
        
    def addMainComment(self):
        self.addComment('')
        self.addComment('generated module')
        self.addComment('')    


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
        self.params.append(node.getText())


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

    def setLeft(self, node):
        left = node.getText()
        if self.parent.isClass():
            self.parent.classvars.add(left)
        elif self.parent.isMethod():
            if self.parent.parent.isClass():
                if left in self.parent.parent.classvars:
                    left = 'self.%s' % (left, )
        self.left = left
            
    def setType(self, node):
        self.typ = node.getText()

    def setOp(self, op):
        self.op = op

    def setRight(self, node):
        try:
            self.right = node.getText()
        except (AttributeError, ):
            self.right = node

    def setExpression(self, left, op, right):
        if right.getType() == walker.LITERAL_new:
            right = '%s()' % (right.getFirstChild().getText(), )
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
            #output.write('%s%s %s %s\n' % (I*indent+1, left, op, right))
            self.append('%s %s %s' % (left, op, right))
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

