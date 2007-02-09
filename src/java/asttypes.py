#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
todo:  add property get/set on duplicate method names
       add property for some modifiers (e.g., syncronized)
       for classes without bases, add object as base
       for classes that implement something, add something as base

done:
       reorder class statements to place inner classes first       

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


class Source:
    def __init__(self, parent=None, name=None):
        self.parent = parent
        self.name = name
        self.modifiers = set()
        self.source = []        
        self.type = None
        self.variables = set()
        
    def __str__(self):
        out = StringIO()
        self.writeTo(out, 0)
        return out.getvalue()

    def addComment(self, text):
        self.addSource('## %s' % text)

    def addNewLine(self):
        self.addSource('')

    def addSource(self, text):
        self.source.append(text)

    def addVariable(self, name):
        ##print "##### %s(name=%s).addVariable(%s)" % (self.__class__.__name__, self.name, name, )                    
        self.variables.add(str(name))

    @property
    def isClass(self):
        return self.__class__ is Class

    @property
    def isMethod(self):
        return self.__class__ is Method
    
    def writeTo(self, output, indent):
        for obj in self.source:
            try:
                obj.writeTo(output, indent)
            except (AttributeError, ):
                output.write('%s%s\n' % (indent*I, obj))
    
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

    def allDecls(self):
        decls = []
        parent = self.parent
        while parent:
            decls.extend(parent.variables)
            parent = parent.parent
        return decls

    def fixDecl(self, *args):
        parent = self.parent
        if parent:
            fixed = []
            scan = list(args)            
            while parent:
                for d in scan[:]:
                    s = 'self.%s' % d
                    if (d in parent.variables) and (s not in fixed):
                        fixed.append(s)
                    elif (d not in fixed):
                        fixed.append(d)
                    scan.remove(d)
                parent = parent.parent
        else:
            fixed = args

        if 'checkConnected' in args:
            #print '#@@@@@@@@@@@@@@@@@', args            
            #print '#!!!!!!!!!!!!!!!!!', fixed
            #print '#$$$$$$$$$$$$$$$$$', 'checkConnected' in self.allDecls()
            pass
        assert len(fixed) == len(args)
        if len(fixed) == 1:
            return fixed[0]
        else:
            return tuple(fixed)

    def setType(self, node):
        self.type = node

    def addModifier(self, mod):
        if mod:
            self.modifiers.add(mod)


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


class Method(Source):
    def __init__(self, parent, name):
        Source.__init__(self, parent=parent, name=name)
        self.parameters = ['self', ]
        
    def writeTo(self, output, indent):
        if self.modifiers:
            output.write('%s## modifiers: %s\n' % (I*indent, str.join(',', self.modifiers)))
        output.write(self.formatDecl(indent))
        output.write('\n')
        if not self.source:
            self.addSource('pass')
        Source.writeTo(self, output, indent+1)

    def formatDecl(self, indent):
        name = rename(self.name)
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
        
    def addParameter(self, node):
        param = self.nodeText(node)
        param = rename(param)
        self.parameters.append(param)


class Class(Source):
    def __init__(self, parent, name):
        Source.__init__(self, parent=parent, name=name)
        self.classvars = set()
        
    def writeTo(self, output, indent):
        if not self.source:
            self.addSource('pass')
        output.write('%sclass %s:\n' % (I*indent, self.name, ))
        Source.writeTo(self, output, indent+1)
        output.write('\n')

    def addParameter(self, *a, **b):
        print '#### warning:  Class.addParameter called (', a, ')'

    def newClass(self):
        c = Class(parent=self, name=None)
        self.source.insert(0, c)
        return c

class Statement(Source):
    def __init__(self, parent, name=None):
        Source.__init__(self, parent=parent, name=name)
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
