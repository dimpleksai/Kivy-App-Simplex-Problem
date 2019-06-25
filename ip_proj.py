from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.textinput import TextInput
from collections import defaultdict
import sys
import numpy as np
from fractions import Fraction
Builder.load_string("""
<CenteredTextInput@TextInput>:
	multiline: False
	font_size:26
	on_text: root.update_padding()
	padding_x: (self.width - self.text_width)/2
	padding_y: (self.height - (self.text_width+30))/2
<CenteredTextOutput@FloatLayout>:
	first: frst
	TextInput:
		font_size:20
		id: frst
		text: "0"
		pos_hint: {"center_x":.5,"center_y":.5}
		multiline:  False

<SimplexProblem>:
	screen_manager:_screen_manager
	products: no_products
	max: cst
	constraints: no_constraints
	input_matrix : input_mat
	input_matrix2: input_mat2
	output_matrix: output_mat
	BoxLayout:
		ScreenManager:
			id: _screen_manager
			Screen:
				color:0,0,0
				name: 'screen1'
				BoxLayout:
					orientation: "vertical"
					Label:
						text: "Simplex Problem" 
						text_size: self.width, None
						size_hint: 1, 0.3
						font_size: 45
						italic: True
						bold: True
						halign: 'center'
					GridLayout:
						row: 1
						cols: 2
						padding:10
						spacing:10
						size_hint:1,0.2
						Label: 
							text: " Number of Products :"
							font_size: 26
						TextInput:
							padding_x: 170
							padding_y: 15
							font_size: 26
							id: no_products
					GridLayout:
						row: 1
						cols: 2
						padding:10
						spacing:10
						size_hint:1,0.2
						Label: 
							text: " Number of Constraints :"
							font_size: 26
						TextInput:
							id: no_constraints
							padding_x: 170
							padding_y: 15
							font_size: 26
					Button:
						size_hint:1,0.18
						text: 'Go to Screen 2'
						on_press: root.take_input()

			Screen:
				name: 'screen2'
				BoxLayout:
					orientation: "vertical"
					Label:
						text: "Enter names for constraints" 
						text_size: self.width, None
						size_hint: 1, 0.3
						font_size: 45
						italic: True
						bold: True
						halign: 'center'
					GridLayout:
						id: input_mat
						row: 3
						cols: 2
						padding:10
						spacing:10
						size_hint:1,0.2
						TextInput:
							padding_x: 170
							padding_y: 15
							font_size: 26
					GridLayout:
						row:1
						cols:2
						padding: 10
						spacing: 10
						size_hint:1,0.18
						Button:
							text: 'Previous'
							on_press: _screen_manager.current = 'screen1'
						Button:
							text: 'Next'
							on_press: root.take_names()
			Screen:
				name: 'screen3'
				BoxLayout:
				GridLayout:
					id : input_mat2
					row: 3
					cols: 2
					padding: 5
					spacing: 5
					size_hint:1,0.8
					pos_hint:{"center_x":0.5 ,"center_y":0.58 }
				GridLayout:
					row:1
					cols:2
					padding: 10
					spacing: 10
					size_hint:1,0.18
					Button:
						text: 'Previous'
						on_press: _screen_manager.current = 'screen2'
					Button:
						text: 'Next'
						on_press: root.generate_output()
			Screen:
				name: 'screen4'
				BoxLayout:
				GridLayout:
					id : output_mat
					row: 3
					cols: 2
					padding: 5
					spacing: 5
					size_hint:1,0.8
					pos_hint:{"center_x":0.5 ,"center_y":0.58 }
				GridLayout:
					row:1
					cols:2
					padding: 10
					spacing: 10
					size_hint:1,0.18
					Label:
						text: "Max: "
						font_size: 26
					Label:
						id: cst
						text: "max"
						font_size: 26
					Button:
						text: 'Previous'
						on_press: _screen_manager.current = 'screen3'
					Button:
						text: 'Restart'
						on_press: _screen_manager.current = 'screen1'
			""")

class CenteredTextInput(TextInput):
	text_width = NumericProperty()

	def update_padding(self,*args):
		self.text_width = self._get_text_width(self.text,self.tab_width,self._label_cached)

class CenteredTextOutput(FloatLayout):
	def update(self,f):
		self.first.text = str(f)

class SimplexProblem(BoxLayout):
	const_num = 0
	prod_nums = 0
	equation_values = []
	const_names = []
	prod_names = []
	z_eq = []
	col_values = []
	final_rows = []
	solutions = []
	x1 = 'X'
	z2_equation = []
	removable_vars = []
	no_solution = ""


	def take_input(self):
		self.screen_manager.current  = "screen2"
		self.const_num = int(self.products.text) 
		self.prod_nums = int(self.constraints.text) 
		self.input_matrix.row = self.const_num
		self.input_matrix.cols = 1
		for i in range(len(self.input_matrix.children)):
			self.input_matrix.remove_widget(self.input_matrix.children[0])
		for i in range(1,self.prod_nums + 1):
			self.input_matrix.add_widget(CenteredTextInput(id = str(i)))




	def take_names(self):
		self.screen_manager.current  = "screen3"
		for child in self.input_matrix.children[::-1]:
			self.prod_names.append(child.text)
		self.input_matrix2.cols =self.const_num + 1
		self.input_matrix2.row = self.prod_nums + 1
		for i in range(len(self.input_matrix2.children)):
			self.input_matrix2.remove_widget(self.input_matrix2.children[0])
		for i in range(self.prod_nums + 1):
			for j in range(self.const_num + 1):
				self.input_matrix2.add_widget(CenteredTextInput(id = str(i)+str(j)))


	def generate_output(self):
		self.screen_manager.current = "screen4"
		for i in range(1,self.const_num + 1):
			val =self.x1 + str(i)
			self.const_names.append(val)
		self.output_matrix.row = self.prod_nums + 1
		self.output_matrix.cols = self.const_num + self.prod_nums + 1
		for child in self.input_matrix2.children[::-1]:
			self.equation_values.append(int(child.text))
		self.equation_values = np.array(self.equation_values).reshape((self.prod_nums + 1,self.const_num + 1))
		print(self.equation_values)
		for i in range (self.prod_nums + 1):
			for j in range (self.const_num + 1):
				if i == 0:
					self.z_eq.append(0-int(self.equation_values[i][j]))
				if i != 0:
					self.col_values.append(float(self.equation_values[i][j]))
		while len(self.z_eq) <= (self.const_num + self.prod_nums):
			self.z_eq.append(0)
		print("col vals before")
		print(self.col_values)
		print("Z_eq")
		print(self.z_eq)
		final_cols =self.stdz_rows(self.col_values)
		print("col vals before")
		print(final_cols)
		i = len(self.const_names) + 1
		while len(self.const_names) < len(final_cols[0]) - 1:
			self.const_names.append('X' + str(i))
			self.solutions.append('X' + str(i))
			i += 1
		self.solutions.append(' Z')
		self.const_names.append('Solution')
		final_cols.append(self.z_eq)
		cols_vals = np.array(final_cols)
		a = 0
		print("Z_eq")
		print(self.z_eq)
		for _ in self.z_eq:
			row = cols_vals[:,a]
			print("row after split")
			print(row)
			row = np.array(row).tolist()
			self.final_rows.append(row)
			a = a+ 1
		for i in range(len(self.output_matrix.children)):
			self.output_matrix.remove_widget(self.output_matrix.children[0])
		self.maximization(final_cols,self.final_rows)



	def maximization(self,final_cols, final_rows):
		res = np.zeros((self.prod_nums + 1,self.const_num + self.prod_nums + 1))
		row_app = []
		final_new_row = []
		last_col = final_cols[-1]
		min_last_col = min(last_col)
		print(final_cols[-1],last_col,min_last_col)
		min_manager = 1
		count = 2
		pivot_element = 2
		print("here")
		print(min_last_col,min_manager,pivot_element)
		while min_last_col < 0 and min_manager == 1 and pivot_element > 0:
			print("in while")
			last_col = final_cols[-1]
			last_row = final_rows[-1]
			min_last_col = min(last_col)
			index_of_min = last_col.index(min_last_col)
			pivot_row = final_rows[index_of_min]
			index_pivot_row = final_rows.index(pivot_row)
			row_div_val = []
			i = 0
			for _ in last_row[:-1]:
				try:
					val = float(last_row[i] / pivot_row[i])
					if val <= 0:
						val = 10000000000
					else:
						val = val
					row_div_val.append(val)
				except ZeroDivisionError:
					val = 10000000000
					row_div_val.append(val)
				i += 1
			min_div_val = min(row_div_val)
			index_min_div_val = row_div_val.index(min_div_val)
			pivot_element = pivot_row[index_min_div_val]
			pivot_col = final_cols[index_min_div_val]
			index_pivot_col = final_cols.index(pivot_col)
			row_app[:] = []
			index_pivot_elem = pivot_col.index(pivot_element)
			for col in final_cols:
				if col is not pivot_col and col is not final_cols[-1]:
					form = col[index_pivot_elem] / pivot_element
					i = 0
					for elem in col:
						value = (elem - float(form * pivot_col[i]))
						row_app.append(round(value, 2))
						i += 1
				elif col is pivot_col:
					for elems in pivot_col:
						value = float(elems / pivot_element)
						row_app.append(round(value, 2))
				else:
					form = abs(col[index_pivot_elem]) / pivot_element
					i = 0
					for elem in col:
						value = elem + float(form * pivot_col[i])
						row_app.append(round(value, 2))
						i += 1

			final_cols[:] = []
			final_new_row[:] = []
			final_new_row = [row_app[x:x + len(self.z_eq)] for x in range(0, len(row_app), len(self.z_eq))]
			for list_el in final_new_row:
				final_cols.append(list_el)
			cols_vals = np.array(final_cols)
			a = 0
			final_rows[:] = []
			for _ in self.z_eq:
				row = cols_vals[:,a]
				row = np.array(row).tolist()
				final_rows.append(row)
				a += 1
			if min(row_div_val) != 10000000000:
				min_manager = 1
			else:
				min_manager = 0
			self.solutions[index_pivot_col] = self.const_names[index_pivot_row]
			i = 0
			for cols in final_cols:
				res[i,:] = cols[:]
				i += 1
			print(res)
			last_col = final_cols[-1]
			min_last_col = min(last_col)
			count += 1
			last_col = final_cols[-1]
			last_row = final_rows[-1]
			min_last_col = min(last_col)
			index_of_min = last_col.index(min_last_col)
			pivot_row = final_rows[index_of_min]
			index_pivot_row = final_rows.index(pivot_row)
			row_div_val = []
			i = 0
			for _ in last_row[:-1]:
				try:
					val = float(last_row[i] / pivot_row[i])
					if val <= 0:
						val = 10000000000
					else:
						val = val
					row_div_val.append(val)
				except ZeroDivisionError:
					val = 10000000000
					row_div_val.append(val)
				i += 1
			min_div_val = min(row_div_val)
			index_min_div_val = row_div_val.index(min_div_val)
			pivot_element = pivot_row[index_min_div_val]
			if pivot_element < 0:
				print(no_solution)
		for i in range (self.const_num + self.prod_nums):
			res[self.prod_nums,i] = 0 - (res[self.prod_nums,i])
		print(res)
		for i in range (self.prod_nums + 1):
			for j in range (self.const_num + self.prod_nums + 1):
				widget = CenteredTextOutput()
				widget.update(res[i,j])
				widget.first.padding_x = (2 * widget.first.width - widget.first._get_text_width(
					widget.first.text,
					widget.first.tab_width,
					widget.first._label_cached)) / 2
				widget.first.padding_y = widget.first.height / 1.5
				self.output_matrix.add_widget(widget)
		self.max.text = str(res[self.prod_nums][self.const_num + self.prod_nums])




	def stdz_rows(self,column_values):
		final_cols = [column_values[x:x + self.const_num + 1] for x in range(0, len(column_values), self.const_num + 1)]
		for cols in final_cols:
			while len(cols) < (self.const_num + self.prod_nums):
				cols.insert(-1, 0)
		i = self.const_num
		for sub_col in final_cols:
			sub_col.insert(i, 1)
			i += 1
		return final_cols

class SimplexProblemApp(App):
	def build(self):
		return SimplexProblem()

if __name__ == '__main__':
	SimplexProblemApp().run()
