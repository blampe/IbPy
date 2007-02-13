#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
todo:
       add project override, file override options
done:
       fix empty type declarations
       fix while, for statements
       add decorator for overloaded methods
       fix compound expressions
       add property get/set on duplicate method names
       reorder class statements to place inner classes first       
       fix missing self references (in expressions w/o all values defined)
       add property for some modifiers (e.g., syncronized)
       for classes without bases, add object as base
       for classes that implement something, add something as base
"""
from cStringIO import StringIO
import re

import defaultconfig
import walker


I = ' ' * 4


def import_item(name):
    """ import_item(name) -> import an item from a module by dotted name

    """
    names = name.split('.')
    modname, itemname = names[0:-1], names[-1]
    mod = import_name(str.join('.', modname))
    return getattr(mod, itemname)


def set_config(names, includeDefault=True):
    if includeDefault:
        names.insert(0, 'lib.defaultconfig')
    Source.config = Config(*names)


class Config:
    def __init__(self, *names):
        self.configs = [import_name(name) for name in names]
        
    def get(self, name, default=None):
        for config in self.configs:
            if hasattr(config, name):
                return getattr(config, name)
        return default

    def all(self, name, missing=None):
        return [getattr(config, name, missing) for config in self.configs]


class Source:
    typeTypeMap = {
        'String':'str',
        'int':'int',
        'double':'float',
        'Vector':'list',
        'boolean':'bool',
    }

    typeValueMap = {
        'String':'""',
        'int':'0',
        'double':'0.0',
        'Vector':'[]',
        'boolean':'False',
        'str':'""',
    }

    renameMap = {
        'this':'self',
        'null':'None',
        'false':'False',
        'true':'True',
        'equals':'__eq__',
    }

    modifierDecoratorMap = {
        'synchronized':'@synchronized(mlock)'
    }


    emptyAssign = ('%s', '<empty>')
    missingValue = ('%s', '<missing>')
    unknownExpression = ('%s', '<unknown>')
    config = Config()
    
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
        source = out.getvalue()
        #for sub in astextra.globalSubs:
        #    source = re.sub(sub[0], sub[1], source)
        return source
    
    def addComment(self, text):
        self.addSource('## %s' % text)

    def addModifier(self, mod):
        if mod:
            self.modifiers.add(mod)

    def addNewLine(self):
        self.addSource('')

    def addSource(self, value):
        self.lines.append(value)

    def addVariable(self, name, force=False):
        if force or (name and self.isClass):
            self.variables.add(name)

    @property
    def allDecls(self):
        for parent in self.allParents:
            for v in parent.variables:
                yield v

    @property
    def allParents(self):
        previous = self.parent
        while previous:
            yield previous
            previous = previous.parent

    @property
    def blockMethods(self):
        return [m for m in self.lines if getattr(m, 'isMethod', False)]

    @property
    def isClass(self):
        return self.__class__ is Class

    @property
    def isMethod(self):
        return self.__class__ is Method

    def fixDecl(self, *args):
        decls = list(self.allDecls)
        fixed = list(args)
        for i, arg in enumerate(args):
            if arg in decls:
                fixed[i] = "self.%s" % (arg, )
        assert len(fixed) == len(args)
        if len(fixed) == 1:
            return fixed[0]
        else:
            return tuple(fixed)

    def newClass(self):
        c = Class(parent=self, name=None)
        self.addSource(c)
        return c

    def newFor(self):
        s = Source(self)
        f = Statement(self, 'while')
        self.addSource(s)
        self.addSource(f)
        return s, f
    
    def newMethod(self, name=''):
        m = Method(parent=self, name=name)
        self.addSource(m)
        return m

    def newSwitch(self):
        s = Statement(self, 'if')
        s.expr = 'False'
        self.addSource(s)
        return s
    
    def newStatement(self, name):
        s = Statement(parent=self, name=name)
        self.addSource(s)
        return s

    def formatExpression(self, s):
        if isinstance(s, basestring):
            return self.fixDecl(s)
        if isinstance(s[0], basestring) and isinstance(s[1], basestring):
            return self.fixDecl(s[0]) % self.fixDecl(s[1])
        if isinstance(s[0], basestring) and isinstance(s[1], tuple):
            return self.fixDecl(s[0]) % self.formatExpression(s[1])
        if isinstance(s[0], tuple) and isinstance(s[1], basestring):
            return self.formatExpression(s[0]) % self.formatExpression(s[1])
        if isinstance(s[0], tuple) and isinstance(s[1], tuple):
            return (self.formatExpression(s[0]), self.formatExpression(s[1]))

    def reName(self, value):
        try:
            return self.renameMap[value]
        except (KeyError, ):
            return value

    def setName(self, name):
        self.name = name
        
    def writeTo(self, output, indent):
        offset = I * indent
        for line in self.lines:
            if isinstance(line, tuple):
                line = self.formatExpression(line)
            try:
                line.writeTo(output, indent)
            except (AttributeError, ):
                output.write('%s%s\n' % (offset, line))


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
        #for line in astextra.headings.get(self.infile, ()):
        #    self.addSource(line)
        self.addNewLine()


class Class(Source):
    def __init__(self, parent, name):
        Source.__init__(self, parent=parent, name=name)
        self.bases = []

    def addBaseClass(self, clause):
        if clause and (clause not in self.bases):
            ## in case java ever grows MI... (giggle)
            self.bases.append(clause) 

    def formatDecl(self):
        bases = self.bases or ['object', ]
        bases = str.join(', ', bases)
        return 'class %s(%s):' % (self.name, bases)

    def newClass(self):
        c = Class(parent=self, name=None)
        ## move inner classes to the top; allows for referencing
        ## later in this class definition.
        self.lines.insert(0, c)
        return c
        

    def scanPropMethods(self):
        lines = self.lines
        methods = self.blockMethods
        mapping = [(m.name, len(m.parameters)) for m in methods]
        propmap = {}

        for meth in methods:
            name = meth.name
            if (name, 1) in mapping and (name, 2) in mapping:
                argc = len(meth.parameters)
                methmap = propmap.setdefault(name, {1:None, 2:None})
                methmap[argc] = meth
                meth.name = ('get_%s' if argc==1 else 'set_%s') % name

        for name, meths in propmap.items():
            lines.remove(meths[1])
            lines.remove(meths[2])

        if lines:
            while not lines[-1]:
                lines.pop()

        format = '%s = property(%s, %s)'                
        for name, meths in propmap.items():
            lines.append(meths[1])
            lines.append(meths[2])            
            lines.append(format % (name, meths[1].name, meths[2].name))
            
    def scanOverloadMethods(self):
        methods = self.blockMethods
        overloads = {}

        for method in methods:
            name = method.name
            overloads[name] = 1 + overloads.setdefault(name, 0)

        for name, count in overloads.items():
            if count == 1:
                del(overloads[name])

        for name, count in overloads.items():
            renames = [m for m in methods if m.name == name]
            #renames.sort(key=lambda m:len(m.parameters))
            first, remainder = renames[0], renames[1:]

            first.preable.append('@overloaded')
            firstname = first.name

            for index, method in enumerate(remainder):
                params = str.join(', ', [p[0] for p in method.parameters])
                method.preable.append('@%s.register(%s)' % (firstname, params))
                method.name = '%s_%s' % (method.name, index)

        def sorter(x, y):
            try:
                if x.isMethod and y.isMethod:
                    return cmp(x.name, y.name)
            except:
                pass
            return 0

        if 0: # make a project option
            self.lines.sort(sorter)

    def writeTo(self, output, indent):
        self.scanPropMethods()
        self.scanOverloadMethods()
        name = self.name
        offset = I * (indent+1)
        output.write('%s%s\n' % (I * indent, self.formatDecl()))
        output.write('%s""" generated source for %s\n\n' % (offset, name))
        output.write('%s"""\n' % (offset, ))
        Source.writeTo(self, output, indent+1)
        output.write('\n')


class Method(Source):
    def __init__(self, parent, name):
        Source.__init__(self, parent=parent, name=name)
        self.parameters = [('object', 'self'), ]

    def addModifier(self, mod):
        try:
            mod = self.modifierDecoratorMap[mod]
        except (KeyError, ):
            Source.addModifier(self, mod)
        else:
            if mod not in self.preable:
                self.preable.append(mod)

    def addParameter(self, typ, name):
        name = self.reName(name)
        self.parameters.append((typ, name))

    def formatDecl(self, indent):
        name = self.reName(self.name)
        parameters = self.parameters
        if len(parameters) > 5:
            first, others = parameters[0], parameters[1:]            
            prefix = '%sdef %s(%s, ' % (I * indent, name, first[1], )
            offset = '\n' + (' ' * len(prefix))
            decl = '%s%s):' % (prefix, str.join(', '+offset, [o[1] for o in others]))
        else:
            params = str.join(', ', [p[1] for p in parameters])
            decl = '%sdef %s(%s):' % (I * indent, name, params)
        return decl

    def writeTo(self, output, indent):
        offset = I * indent
        output.write('\n')
        #if self.modifiers and astextra.defaults['writemods']:
        #    output.write('%s## modifiers: %s\n' % (offset, str.join(',', self.modifiers)))
        for obj in self.preable:
            output.write('%s%s\n' % (offset, obj))
        output.write('%s\n' % (self.formatDecl(indent), ))
        if not self.lines:
            self.addSource('pass')
        Source.writeTo(self, output, indent+1)


class Statement(Source):
    def __init__(self, parent, name=None, expr=None):
        Source.__init__(self, parent=parent, name=name)
        self.expr = expr

    @property
    def isBadLabel(self):
        if self.name in ('break', 'continue'):
            parent_names = [p.name for p in self.allParents]
            if 'while' not in parent_names and 'for' not in parent_names:
                return True
    @property
    def isNoOp(self):
        return self.name in ('else', 'finally') and (not self.lines)

    @property
    def isBlock(self):
        return self.name in ('if', 'while', 'for', 'else', 'elif', 'try', 'except', 'finally')

    def writeTo(self, output, indent):
        name = self.name
        parents = self.allParents
        lines = self.lines
        
        if self.isBadLabel or self.isNoOp:
            return

        offset = I * indent
        output.write('%s%s' % (offset, name))
        if self.expr is not None:
            expr = self.formatExpression(self.expr)
            output.write(' %s' % (expr, ))
        #if self.isBlock:
        #    output.write(':')
        output.write(':\n')
        if (not lines) and name not in ('break', 'continue', ):
            self.addSource('pass')
        Source.writeTo(self, output, indent+1)

    def setExpression(self, value):
        self.expr = value
