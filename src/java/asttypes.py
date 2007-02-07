from cStringIO import StringIO

I = ' '*4

typeMap = {
    'String':"''",
    'int':'0',
    'double':'0.0',
}


class Source:
    def __init__(self):
        self.objects = []
        self.name = ''
        
    def __str__(self):
        out = StringIO()
        self.writeTo(out, 0)
        return out.getvalue()

    def writeTo(self, output, indent):
        for obj in self.objects:
            try:
                obj.writeTo(output, indent)
            except (AttributeError, ):
                print >> output, '%s%s' % (indent*I, obj)

    def klass(self):
        cls = Class()
        self.addNewLine()        
        self.objects.append(cls)
        return cls

    def method(self):
        meth = Method(self)
        self.addNewLine()
        self.objects.append(meth)
        return meth

    def expression(self):
        expr = Expression(self)
        self.objects.append(expr)
        return expr
    
    def addIdent(self, node):
        if node and not self.name:
            self.name = node.getText()

    def addNewLine(self):
        self.objects.append('')

    def addComment(self, node):
        if isinstance(node, basestring):
            text = node
        elif node:
            text = node.getText()
        else:
            text = '<emtpy>'
        comment = '## %s' % (text, )
        self.objects.append(comment)

    def addVariableDef(self, typ, name, init):
        if name:
            name = name.getText().strip()
        if init:
            expr = init.getText()
            val = init.getFirstChild().getFirstChild().getText()
        else:
            expr = '='
            typ = typeMap.get(typ.getFirstChild().getText(), 'None')
            val = '%s' % (typ, )
        self.objects.append('%s %s %s' % (name, expr, val, ))


class Module(Source):
    def __init__(self):
        Source.__init__(self)
        self.addSheBang()
        self.addNewLine()
        self.addMainComment()
        self.addNewLine()

    def addSheBang(self):
        self.objects.append('#!/usr/bin/env python')
        
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
        print >> output, '%sdef %s(%s):' % (I*indent, self.name, params)
        Source.writeTo(self, output, indent+1)

    def addParameters(self, node):
        if node:
            param = node.getText()
            self.params.append(param)


class Class(Source):
    def __init__(self):
        Source.__init__(self)
        self.classvars = set()
        
    def writeTo(self, output, indent):
        print >> output, '%sclass %s:' % (I*indent, self.name, )
        Source.writeTo(self, output, indent+1)
        
    def addVariableDef(self, typ, name, init):
        if name:
            self.classvars.add(name.getText().strip())
        Source.addVariableDef(self, typ, name, init)


class Expression(Source):
    def __init__(self, parent):
        Source.__init__(self)
        self.parent = parent
        self.expr = []
        self.typ = None

    def addUnary(self, rh, op):
        right = ''
        if rh:
            right = rh.getText()
            if right in self.classvars:
                right = 'self.%s' % right
        self.expr = [op, right, ]
        
    def addBinary(self, lh, rh, op):
        left = right = ''
        if lh:
            left = lh.getText()
            if left in self.classvars:
                left = 'self.%s' % left
        if rh:
            right = rh.getText()
            if right == 'new':
                right = '%s()' % (rh.getFirstChild().getText(), )
            elif right in self.classvars:
                right = 'self.%s' % right
        self.expr = [left, op, right]


    def addReturn(self, value):
        if value:
            value = value.getFirstChild().getText()
            if value in self.classvars:
                value = 'self.%s' % (value, )
        else:
            value = 'None'
        self.expr = ['return', value]


    def writeTo(self, output, indent):
        expr = self.expr
        expc = len(expr)
        args = [I*indent, ] + expr
        if expc == 3:
            if args[3] == 'new':
                args[3] = self.typ
            print >> output, '%s%s %s %s' % tuple(args)
        elif expc >= 2 and (expr[0] == 'return'):
            print >> output, '%s%s %s' % tuple(args)
        elif expc == 2:
            print >> output, '%s%s %s' % tuple(args)
        elif expc == 1:
            print >> output, '%s%s' % tuple(args)

    @property
    def classvars(self):
        p = self.parent
        while p:
            if hasattr(p, 'parent'):
                p = p.parent
            else:
                break
        return getattr(p, 'classvars', ())

