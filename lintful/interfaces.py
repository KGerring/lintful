#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = interfaces
# author= KGerring
# date = 4/14/18
# from startups import *
"""


class IMyInterface(Interface):
	'''Interface documentation'''
	
@implementer(IMyInterface)
class MyInterface(object):
	pass
	
	
class My(object): pass

class My0(object): pass

classImplements(My0, IMyInterface)

	
m = My()
directlyProvides(m, IMyInterface)

IMyInterface.providedBy(m) == True          for instance usage
IMyInterface.implementedBy(My) == True      for class usage
zope.component.implementedBy(My)(IMyInterface) == True


m.__provides__(IMyInterface) == True

providedByFallback(m)(IMyInterface) == True
zope.component.providedBy(m)(IMyInterface) == True
Provides(My0)(IMyInterface) == True


My0.__implemented__(IMyInterface) == True
My0.__implemented__(zope.interface.Interface) = True

	
	
mm = My()
_m = provider(IMyInterface)(mm)
	
	
	
provider(self.interfaces)(obj) == directlyProvides(obj, *self.interfaces)
	
	
Now can call with provider(interfaces) on an object

implementer(IMyInterface) can call on a class

	
	
o You assert that your object implement the interfaces.
	zope.interface.implements in your class definition.
	zope.interfaces.directlyProvides on your object.
		
	
	zope.interface.classImplements to assert that instances of a class implement an interface.
		classImplements(some_class, some_interface)
		
"""
from __future__ import absolute_import, unicode_literals # isort:skip
__all__ = ['SITE_MANAGER',"INSTANCES","REGISTRY", 'REGISTERED_UTILITIES', 'INTERFACES', 'register_utility']
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip
#from startups.helpers.decorators import ExportsList
#__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__
EXAMPLE = 'https://docs.zope.org/zope.interface/human.html'


from lintful.config import resolve
import pylint.interfaces
from pylint.interfaces import implements as pylint_implements, IReporter
import sphinx.ext.inheritance_diagram
from sphinx.ext.inheritance_diagram import import_classes
from startups.misc import attrgetter

import zope.component
import zope.event
import zope.interface


from zope.component import (adapter,
                            adapts,
                            adapter_hook,
                            adaptedBy,
                            getAdapter,
                            queryAdapter,
                            getAllUtilitiesRegisteredFor)

from zope.interface import (
    declarations,
    implementedBy,
    Interface,
    invariant,
    noLongerProvides,
    providedBy,
    taggedValue,)

from zope.interface.adapter import AdapterRegistry
from zope.interface.declarations import (
	InstanceDeclarations,
    alsoProvides,
	classImplements,
	classImplementsOnly,
	classProvides,
    directlyProvidedBy,
	directlyProvides,
	getObjectSpecificationFallback,
    implementedByFallback,
	implementer,
	implementer_only,
	Implements,
	named,
    providedByFallback,
	provider,
	Provides,
	_implements_name,
)

from zope.interface.interface import (
    adapter_hooks,
    Attribute,
    InterfaceBase,
    InterfaceClass,
    SpecificationBasePy,
    InterfaceBasePy,
)

from zope.interface.verify import verifyObject, verifyClass, _verify

implements_only =           zope.interface.implementsOnly
implemented_by =            zope.interface.implementedBy
provided_by =               zope.interface.providedBy
directly_provides =         zope.interface.directlyProvides
directly_provided_by =      zope.interface.directlyProvidedBy
class_implements =          zope.interface.declarations.classImplements


DECORATORS = (adapter, provider, implementer, implementer_only)

REGISTRY = registry = AdapterRegistry()
GSM = SITE_MANAGER = zope.component.getGlobalSiteManager()



def hook(provided, object):
	adapter = REGISTRY.lookup1(zope.interface.providedBy(object), provided, '')
	return adapter(object)


if hook not in adapter_hooks:
	adapter_hooks.append(hook)


def adapted_by(obj):
	"""
	
	:param obj:
	:return:
	"""
	return getattr(obj, '__component_adapts__', None)



def verifyClass(iface, candidate, tentative=0):
	return _verify(iface, candidate, tentative, vtype='c')
	if vtype == 'c':
		tester = iface.implementedBy
	else:
		tester = iface.providedBy
	
	if not tentative and not tester(candidate):
		return False
	
	
def register_utility(klass, *interfaces):
	classImplements(klass, *interfaces)
	zope.component.provideUtility(klass, interfaces[0], klass.__name__)
	return GSM.utilities.names([], interfaces[0])


#__conform__


#m.__providedBy__(lintful.plugins.base.ReporterMessage)
#m.__provides__(lintful.plugins.base.ReporterMessage)
#M = ss.BaseMessage(ss.ReporterMessage)
#ib.implementedBy(s.ReporterMessage)
#ib = s.implementedBy(s.ReporterMessage)
#RM = s.provider(s.ReporterMessage)

#ib = s.implementedBy(s.ReporterMessage)

class PyLintInterface(Interface):

	def is_implemented_by(instance):
		"classmethod for pylint.interfaces.implements"

class_implements(resolve('pylint.interfaces', 'Interface'), PyLintInterface)


class IBaseReporter(Interface):
	"""base class for reporters

	    symbols: show short symbolic names for messages.
	    """
	extension = Attribute('')
	
	def handle_message(msg):
		"""Handle a new message triggered on the current file."""
	
	def set_output(output=None):
		"""set output stream"""
	
	def writeln(string=''):
		"""write a line in the output buffer"""
	
	def display_reports(layout):
		"""display results encapsulated in the layout tree"""
	
	def _display(layout):
		"""display the layout"""
	
	def display_messages(layout):
		"""Hook for displaying the messages of the reporter

		This will be called whenever the underlying messages
		needs to be displayed. For some reporters, it probably
		doesn't make sense to display messages as soon as they
		are available, so some mechanism of storing them could be used.
		This method can be implemented to display them after they've
		been aggregated.
		"""
	
	def on_set_current_module(module, filepath):
		"""Hook called when a module starts to be analysed."""
	
	def on_close(stats, previous_stats):
		"""Hook called when a module finished analyzing."""


class_implements(resolve('pylint.reporters', 'BaseReporter'), IBaseReporter)


class IDict(Interface):
	""""""

class IMessage(Interface):
	"""Interface for Messages"""

class IMessageComp(Interface):
	"""Interface for TupleComp"""
	
	comp_select_list = Attribute("""The comparisons""")


from pstats import TupleComp



@implementer(IMessageComp)
class MessageComp(TupleComp):
	
	adapts(IMessage)
	
	def compare_attr(self, left, right):
		for index, direction in self.comp_select_list:
			l = getattr(left, index)
			r = getattr(right, index)
			if l < r:
				return -direction
			if l > r:
				return direction
			return 0


GSM.registerAdapter(MessageComp, (IMessage,), IMessageComp, '')
REGISTRY.register([IMessage], IMessageComp, '', MessageComp)

classImplements(resolve('lintful.plugins.base', 'ReporterMessage'), IMessage)
classImplements(resolve('pylint.utils', '_MsgBase'), IMessage)

GSM.registerUtility(resolve('pylint.utils', '_MsgBase'), IMessage, '')
GSM.registerUtility(resolve('lintful.plugins.base', 'ReporterMessage'), IMessage, '')



#I.GSM.getAllUtilitiesRegisteredFor



	
REGISTERED_UTILITIES = sorted(GSM.registeredUtilities(), key=attrgetter('provided.__identifier__'))


INTERFACES = list(GSM._utility_registrations_cache._cache)

#print(list(ReporterMessage.__implemented__))

#GSM.utilities.registered([], I.IMessage)




#verifyClass(IMessage, ReporterMessage)

#implementedBy(ReporterMessage)(IMessage)


#list(I.implemented_by(I.ReporterMessage))
#list(I.implemented_by(I.Message))
#I.implemented_by(I.ReporterMessage)(I.IMessage)
#I.providedBy(a)(I.IMessage)

INSTANCES = dict(InstanceDeclarations)



if __name__ == '__main__': print(__file__)
