# coding: utf-8

from __future__ import absolute_import
import json
import os
import time
import copy
import appex
import sys

class FlowManager (object):
	def __init__(self, elementchangecb):
		self.elementchangecb = elementchangecb
		self.runtime_variables = {}
		self.nav_view = None
		self.dir = 'flows/'
		if not os.path.exists(self.dir):
			os.mkdir(self.dir)
		
	def get_flows(self, appexonly):
		flows = os.listdir(self.dir)
		if appexonly:
			return [f for f in flows if self.get_type_for_flow(f) == 'Action Extension']
		else:
			return flows
	
	def save_flow(self, title, elements, type):
		names = []
		for ele in elements:
			params = {p.name: {'value':p.value if not p.askAtRuntime else None, 'useVariable':p.useVariable, 'variableName':p.variableName if not p.askAtRuntime else '', 'askAtRuntime':p.askAtRuntime} for p in (ele.get_params() or []) if p.display}
			ob = {'title':ele.get_title(),'params':params}
			names.append(ob)
		fl = {'type':type,'elements':names}
		f = open(self.dir+title+'.flow','w')
		f.write(json.JSONEncoder().encode(fl))
		f.close()
	
	def delete_flow(self, title):
		if os.path.exists(self.dir+title):
			os.remove(self.dir+title)
	
	def get_element_details_for_flow(self, flow):
		with open(self.dir+flow,'r') as f:
			return json.JSONDecoder().decode(f.read())['elements']
	
	def get_type_for_flow(self, flow):
		with open(self.dir+flow,'r') as f:
			return json.JSONDecoder().decode(f.read())['type']
		
	def run_flow(self, elements, navview, type):
		output = None
		prevOutputType = None
		elementNumber = 1
		foreachstore = None
		forstore = None
		ifstore = None
		self.nav_view = navview
		self.runtime_variables = {}
		if type == 'Action Extension' and not appex.is_running_extension():
			return False, 'Flow type: Action Extension flow not running in extension'
		try:
			while elementNumber<= len(elements):
				element = elements[elementNumber-1]
				self.elementchangecb(elementNumber)
				elementType = element.get_type()
				self.set_runtime_element_params(element)
				if element.get_input_type() == None:
					output = element.run()
				else:
					if prevOutputType == element.get_input_type() or element.get_input_type() == '*':
						if output == None or not output.isList or element.can_handle_list():
							output = element.run(output)
						else:
							raise ValueError('List provided to ' + element.get_title() + ' and cant handle list')
					else:
						raise ValueError('Invalid input type provided to ' + element.get_title())
				self.get_runtime_element_params(element)
				prevOutputType = output.type if output else element.get_output_type()
				if elementType == 'Foreach':
					foreachstore = [copy.deepcopy(output),elementNumber,len(output.value),0]
					output.value = foreachstore[0].value[foreachstore[3]]
					self.handle_foreach()
				elif elementType == 'EndForeach':
					foreachstore[3] += 1
					if foreachstore[3] < foreachstore[2]:
						elementNumber = foreachstore[1]
						output.type = foreachstore[0].type
						output.value = foreachstore[0].value[foreachstore[3]]
					else:
						foreachstore = None
						output = None
				elif elementType == 'For':
					forcount = element.get_param_by_name('forcount')
					if forcount == None:
						return False, 'For element count parameter not setup correctly'
					forstore = [elementNumber,forcount.value,0]
				elif elementType == 'EndFor':
					output = None
					forstore[2] += 1
					if forstore[2] < forstore[1]:
						elementNumber = forstore[0]
					else:
						forstore = None
				elif elementType == 'If':
					ifresult = element.get_param_by_name('ifresult')
					if ifresult == None or ifresult.value == None:
						return False, 'Result from if not found or is None, uisomething is wrong'
					if not ifresult.value:
						elsefound= False
						i = elementNumber
						skipnumber = 0
						while not elsefound:
							if i >= len(elements):
								return False, 'Else not found for if block'
							if elements[i].get_type() == 'If':
								skipnumber = skipnumber + 1
							if elements[i].get_type() == 'Else':
								if skipnumber > 0:
									skipnumber = skipnumber - 1
									i = i + 1
								else:
									elsefound = True
									elementNumber = i+1
							else:
								i = i+1
				elif elementType == 'Else':
					endiffound = False
					i = elementNumber
					skipnumber = 0
					while not endiffound:
						if i >= len(elements):
							return False, 'End If not found for if block'
						if elements[i].get_type() == 'If':
								skipnumber = skipnumber + 1
						if elements[i].get_type() == 'EndIf':
							if skipnumber > 0:
								skipnumber = skipnumber - 1
								i = i + 1
							else:
								endiffound = True
								elementNumber = i
						else:
							i = i+1
				elif elementType == 'EndIf':
					output = None
					ifstore = None
				
				elementNumber += 1
			elementNumber = 0
			self.elementchangecb(elementNumber)
			return True, 'Flow completed successfully'
		except KeyboardInterrupt:
			return False, 'Cancelled by user'
		except:
			return False, str(sys.exc_info()[1])
	
	def set_runtime_element_params(self, element):
		params = element.get_params()
		if params:
			for param in params:
				if param.name =='fm:runtime_variables':
					param.value = self.runtime_variables
				if param.name == 'fm:nav_view':
					param.value = self.nav_view
				if param.useVariable:
					element.get_runtime_variable_for_parameter(param)
			element.set_params(params)
			
	def get_runtime_element_params(self, element):
		for param in element.get_params() or []:
			if param.name == 'fm:runtime_variables':
				self.runtime_variables = param.value
	
	def handle_foreach(self):
		pass



