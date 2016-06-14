# coding: utf-8

from __future__ import absolute_import
import ui

class FlowsView(object):
	def __init__(self, flows, flowselectedcb, flowdeletedcb, thememanager):
		self.flows = flows or []
		self.flowselectedcb = flowselectedcb
		self.flowdeletedcb = flowdeletedcb
		self.thememanager = thememanager

	def tableview_did_select(self, tableview, section, row):
		self.flowselectedcb(self.flows[row])
		
	def tableview_title_for_header(self, tableview, section):
		pass

	def tableview_number_of_sections(self, tableview):
		return 1

	def tableview_number_of_rows(self, tableview, section):
		return len(self.flows)
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		cell.text_label.text = self.flows[row]
		cell.background_color = self.thememanager.main_background_colour
		cell.text_label.text_color = self.thememanager.main_text_colour
		cell.selectable = True
		return cell
	
	def tableview_can_delete(self, tableview, section, row):
		# Return True if the user should be able to delete the given row.
		return True

	def tableview_can_move(self, tableview, section, row):
		# Return True if a reordering control should be shown for the given row (in editing mode).
		return True

	def tableview_delete(self, tableview, section, row):
		# Called when the user confirms deletion of the given row.
		self.flowdeletedcb(self.flows[row])
		self.flows.pop(row)
		table_view.delete_rows([row])

	def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
		# Called when the user moves a row with the reordering control (in editing mode).
		pass

table_view = ui.TableView()
def get_view(flows, selectedcb, deletedcb, thememanager):
	dbo = FlowsView(flows = flows, flowselectedcb = selectedcb, flowdeletedcb = deletedcb, thememanager=thememanager)
	table_view.name = 'Flows'
	table_view.background_color=thememanager.main_background_colour
	table_view.data_source = dbo
	table_view.delegate = dbo
	return table_view


