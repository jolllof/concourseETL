# ['Course Description', 'Rationale', 'Measurable Learning Outcomes', 
# 'Course Resources', 'Course Assignment', 'Course Grading', 'Policy', 'Schedule']


"""I call master with course id results, master calls children to get all item pretty names
	in syllabus and then calls parser to get specific item into a dictionary and stores it
	in the appropriate initialized list. parser also calls permissions which pulls perms
	for that item and stores it in its app
"""
import pandas as pd
class Transform():
	def __init__(self):
		self.syl = []	#Syllabus
		self.perm = []	#Permissions
		self.desc = []	#Course Description
		self.info = []	#Contact Information
		self.rati = []	#Rationale
		self.outc = []	#Measurable Learning Outcomes
		self.reso = []	#Course Resources
		self.assi = []  #Course Assignments
		self.grad = []	#Course Grading
		self.poli = []	#Policy
		self.sche = []  #Schedule


	def master(self,dictt):
		main_id = dictt['id'] #so that each table can contain the main syllabus id
		self.syllabus(dictt)
		items = self.items(dictt["syllabus"]["children"])

		try:
			self.desc.append(self.parser(items['Course Description'],main_id))
			self.info.append(self.parser(items['Contact Information'],main_id))
			self.rati.append(self.parser(items['Rationale'],main_id))
			self.outc.append(self.parser(items['Measurable Learning Outcomes'],main_id))
			self.reso.append(self.parser(items['Course Resources'],main_id))
			self.assi.append(self.parser(items['Course Assignment'],main_id))
			self.grad.append(self.parser(items['Course Grading'],main_id))
			self.poli.append(self.parser(items['Policy'],main_id))
			self.sche.append(self.parser(items['Schedule'],main_id))

		except KeyError as e:
			pass

	def items(self,items):
		"""creates dict of dicts from a list of dicts with each item pretty name as key"""
		return{item['pretty_name']:item for item in items}

	def parser(self, dictt, main_id):
		
		exceptions = ['children', 'permissions','fields']
		d={item:value for (item,value) in dictt.items() if item not in exceptions}
		d.update(dictt['fields'])
		d.update({'syllabus_id':main_id})
		#print(dictt['pretty_name'])

		#recursive until all children are pulled up
		if dictt['children']:
			child = self.parser(dictt['children'][0],main_id)
			d.update(child)
		try:
			self.permissions(dictt, d['id'], dictt['pretty_name'], main_id)
		except:
			pass

		return d

	def syllabus(self,dictt):
		exceptions = ['department','campus','sections','syllabus']
		d= {item:value for (item,value) in dictt.items() if item not in exceptions}
		d.update({"department":dictt["department"]["name"],
					"department_id":dictt["department"]["external_id"],
					"campus":dictt["campus"]["name"],
					"campus_id":dictt["campus"]["external_id"],
					"notes":dictt["syllabus"]["fields"]["notes"],
					"comments":dictt["syllabus"]["fields"]["comments"],
					"is_locked":dictt["syllabus"]["is_locked"],
					"is_linked":dictt["syllabus"]["is_linked"],})
		
		try:
			d.update(dictt['sections'][0])
		except IndexError:
			pass
		
		self.syl.append(d)
		#id is passed twice below perms keeps item id and then syllabus id which is
		#the same in this instance
		self.permissions(dictt["syllabus"], dictt['id'], 'Syllabus', dictt['id'])

	def permissions(self, dictt, id, name, main_id):
		perms = {"id": id}
		perms.update({'syllabus_id':main_id})
		perms.update({"pretty_name":name})
		perms.update(dictt["permissions"])
		self.perm.append(perms)
