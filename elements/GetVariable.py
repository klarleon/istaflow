# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
import console
import dialogs
import ui

class GetVariable(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None
		self.params = []
		self.name = None
		self.setup_params()

	def setup_params(self):
		self.params.append(ElementParameter(name='fm:runtime_variables',type='*'))
		self.params.append(ElementParameter(name='VariableName',display=True,type='string'))

	def get_status(self):
		return self.status

	def get_input_type(self):
		return None

	def get_output(self):
		return self.output

	def get_output_type(self):
		return '*'

	def get_params(self):
		return self.params

	def set_params(self, params = []):
		self.params = params

	def get_description(self):
		return 'Get a variable to be used within the flow.'

	def get_title(self):
		return 'Get Variable'

	def get_icon(self):
		return 'iob:ios7_gear_32'

	def get_category(self):
		return 'Utility'
	
	def selected_callback(self, item):
		print item
		self.name = item.name
		self.status = 'complete'
		self.get_param_by_name('fm:nav_view').value.pop_view()
		
	def run(self):
		np = self.get_param_by_name('VariableName')
		rv = self.get_param_by_name('fm:runtime_variables')
		keysavailablestring = ''
		for k in rv.value.keys():
			keysavailablestring += k + ' '
		keysavailablemessage = 'Keys to choose from are: ' + keysavailablestring
		if np.value == None:
			try:
				key = dialogs.list_dialog('Vars',rv.value.keys())
				self.name = key
			except :
				# if dialogs isnt available then fall back to console input
				self.name = console.input_alert(title='Please enter variable title', message=keysavailablemessage)
				
		else:
			self.name = np.value
		if self.name == None:
			self.name = console.input_alert(title='Please enter variable title', message=keysavailablemessage)
		return rv.value[self.name]