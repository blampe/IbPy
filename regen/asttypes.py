#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
todo:
       add decorator for overloaded methods
       fix compound expressions
       fix statements
done:
       add property get/set on duplicate method names
       reorder class statements to place inner classes first       
       fix missing self references (in expressions w/o all values defined)
       add property for some modifiers (e.g., syncronized)
       for classes without bases, add object as base
       for classes that implement something, add something as base
       
"""
from cStringIO import StringIO

import astextra
from lib import walker


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

modifierRenameMap = {
    'synchronized':'@synchronized(mlock)'
}


class Source:
    def __init__(self, parent=None, name=None):
        self.parent = parent
        self.name = name
        self.modifiers = set()
        self.preable = []
        self.lines = []        
        self.type = None
        self.variables = set()
        
    def __str__(self):
        out = StringIO()
        self.writeTo(out, 0)
        return out.getvalue()

    def addComment(self, text):
        self.addSource('## %s' % text)

    def addModifier(self, mod):
        if mod:
            self.modifiers.add(mod)

    def addNewLine(self):
        self.addSource('')

    def addSource(self, text):
        self.lines.append(text)

    def addVariable(self, name):
        self.variables.add(name)

    @property
    def isBlock(self):
        return self.name in ('if', 'while', 'for', 'else', 'elif')

    @property
    def isClass(self):
        return self.__class__ is Class

    @property
    def isMethod(self):
        return self.__class__ is Method

    def newClass(self):
        c = Class(parent=self, name=None)
        self.addSource(c)
        return c

    def newMethod(self, name=''):
        m = Method(parent=self, name=name)
        self.addNewLine()
        self.addSource(m)
        return m

    def newStatement(self, name):
        s = Statement(parent=self, name=name)
        self.addSource(s)
        return s

    def nodeText(self, node):
        try:
            return node.getText()
        except (AttributeError, ):
            return node

    def reFormat(self, seq):
        try:
            return seq[0] % tuple([self.reFormat(s) for s in seq[1:]])
        except:
            return self.fixDecl(seq)

    def reName(self, item):
        try:
            return renameMap[item]
        except (KeyError, ):
            return item

    def setType(self, node):
        self.type = node

    def writeTo(self, output, indent):
        offset = I*indent
        for obj in self.lines:
            if callable(obj):
                obj = obj()
            elif isinstance(obj, (tuple, list)):
                obj = self.reFormat(obj)
            try:
                obj.writeTo(output, indent)
            except (AttributeError, ):
                output.write('%s%s\n' % (offset, obj))
        
    def fixDecl(self, *args):
        parent = self.parent
        if parent:
            fixed = []
            scan = list(args)            
            while parent:
                for d in scan[:]:
                    s = 'self.%s' % (d, )
                    if (d in parent.variables) and (s not in fixed):
                        fixed.append(s)
                    elif (d not in fixed):
                        fixed.append(d)
                    scan.remove(d)
                parent = parent.parent
        else:
            fixed = args
        assert len(fixed) == len(args)
        if len(fixed) == 1:
            return fixed[0]
        else:
            return tuple(fixed)


class Module(Source):
    def __init__(self, infile, outfile):
        Source.__init__(self, parent=None, name=None)
        self.infile = infile
        self.outfile = outfile
        self.addHeading()

    def addHeading(self):
        self.addSource('#!/usr/bin/env python')
        self.addSource('# -*- coding: utf-8 -*-')
        self.addNewLine()
        self.addComment('')
        self.addComment('Source file: "%s"' % (self.infile, ))
        self.addComment('Target file: "%s"' % (self.outfile, ))
        self.addComment('')        
        self.addComment('Original file copyright original author(s).')
        self.addComment('This file copyright Troy Melhase <troy@gci.net>.')        
        self.addComment('')        
        self.addNewLine()
        for line in astextra.headings.get(self.infile, ()):
            self.addSource(line)
        self.addNewLine()

class Class(Source):
    def __init__(self, parent, name):
        Source.__init__(self, parent=parent, name=name)
        self.bases = []

    def addBaseClass(self, clause):
        if clause and clause not in self.bases:
            ## in case java ever grows MI... (giggle)
            self.bases.append(clause) 

    def addParameter(self, *a, **b):
        print '#### warning:  Class.addParameter called (', a, ')'

    def formatDecl(self):
        bases = self.bases or ['object', ]
        bases = str.join(', ', bases)
        return 'class %s(%s):' % (self.name, bases)
        
    def writeTo(self, output, indent):
        self.propertyMethodScan()
        self.overloadMethodScan()
        
        name = self.name
        offset = I*(indent+1)
        output.write('%s%s\n' % (I*indent, self.formatDecl()))
        output.write('%s""" generated source for %s\n\n' % (offset, name))
        output.write('%s"""\n' % (offset, ))
        Source.writeTo(self, output, indent+1)
        output.write('\n')

    def newClass(self):
        c = Class(parent=self, name=None)
        ## move inner classes to the top; allows for referencing
        ## later in this class definition.
        self.lines.insert(0, c)
        return c

    def propertyMethodScan(self):
        lines = self.lines
        methods = [m for m in lines if getattr(m, 'isMethod', False)]
        mapping = [(m.name, len(m.parameters)) for m in methods]
        propmap = {}
        for meth in methods:
            if (meth.name, 1) in mapping and (meth.name, 2) in mapping:
                argc = len(meth.parameters)
                pmmap = propmap.setdefault(meth.name, {1:None, 2:None})
                pmmap[argc] = meth
                meth.name = 'get_%s' if argc == 1 else 'set_%s' % meth.name
        for methname, propmethods in propmap.items():
            lines.remove(propmethods[1])
            lines.remove(propmethods[2])
        if lines:
            while not lines[-1]:
                lines.pop()
        for methname, propmethods in propmap.items():
            assert propmethods[1]
            assert propmethods[2]
            lines.append('')
            lines.append(propmethods[1])
            lines.append(propmethods[2])            
            lines.append('%s = property(%s, %s)' % (methname, propmethods[1].name, propmethods[2].name))
            
    def overloadMethodScan(self):
        pass


class Method(Source):
    def __init__(self, parent, name):
        Source.__init__(self, parent=parent, name=name)
        self.parameters = ['self', ]

    def addModifier(self, mod):
        try:
            mod = modifierRenameMap[mod]
        except (KeyError, ):
            Source.addModifier(self, mod)
        else:
            if mod not in self.preable:
                self.preable.append(mod)

    def addParameter(self, node):
        param = self.nodeText(node)
        param = self.reName(param)
        self.parameters.append(param)

    def formatDecl(self, indent):
        name = self.reName(self.name)
        parameters = self.parameters
        if len(parameters) > 5:
            first, others = parameters[0], parameters[1:]            
            prefix = '%sdef %s(%s, ' % (I*indent, name, first, )
            offset = '\n' + (' ' * len(prefix))
            decl = '%s%s):' % (prefix, str.join(', '+offset, others))
        else:
            params = str.join(', ', self.parameters)            
            decl = '%sdef %s(%s):' % (I*indent, name, params)
        return decl

    def writeTo(self, output, indent):
        offset = I * indent
        if self.modifiers and astextra.defaults['writemods']:
            output.write('%s## modifiers: %s\n' % (offset, str.join(',', self.modifiers)))
        for obj in self.preable:
            output.write('%s%s\n' % (offset, obj))
        output.write('%s\n' % (self.formatDecl(indent), ))
        if not self.lines:
            self.addSource('pass')
        Source.writeTo(self, output, indent+1)


class Statement(Source):
    def __init__(self, parent, name=None):
        Source.__init__(self, parent=parent, name=name)
        self.expr = None
        
    def writeTo(self, output, indent):
        output.write('%s%s' % (I*(indent), self.name))
        if self.expr is not None:
            expr = self.reFormat(self.expr)
            output.write(' %s' % (expr))
        if self.isBlock:
            output.write(':')
        output.write('\n')
        Source.writeTo(self, output, indent+1)

    def setExpression(self, e):
        self.expr = e
