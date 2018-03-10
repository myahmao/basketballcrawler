#!/usr/local/bin/python
# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

'''import pandas as pd

xl = pd.ExcelFile("/Users/yonwang/myproject/xls/CD Archive  By Category Thru A-211.xls")
df = xl.parse(0)
#print df

column = df.columns.tolist()
rows = df.iterrows()
i=0

for row in rows:
	print type(row), row
	#print i
	i+=1
	break

DataFrame = pd.read_excel("/Users/yonwang/Downloads/vPC_conv_HSK2.xlsx")
#print DataFrame
'''
import pymongo
from pymongo import MongoClient
import datetime

def xldate_to_datetime(xldate):
	temp = datetime.datetime(1900, 1, 1)
	delta = datetime.timedelta(days=xldate)
	return temp+delta

def none_value_count(row):
	count = 0
	for element in row:
		if element.value != '':
			count+=1
	return count
class Dict(dict):
	def __add__(self, other):
		copy = self.copy()
		copy.update(other)
		return copy
	def __radd__(self, other):
		copy = other.copy()
		copy.update(self)
		return copy

def if_audio_exists(programs, audio_link):
	if audio_link in programs.keys():
		print 148, 'yes'
		return True
	return False

import xlrd
from xlrd import open_workbook
from xlrd.sheet import ctype_text

wb = open_workbook("/Users/yonwang/myproject/xls/CD Archive  By Category Thru A-211.xls")
sheet = wb.sheet_by_index(0)
print sheet.nrows
for row in range (sheet.nrows):

	if none_value_count(sheet.row(row)) == 0 :
		continue
	if none_value_count(sheet.row(row)) == 1 and row == sheet.nrows-1:
		continue	 
	print 'row', row
	#print sheet.row(row), sheet.row(row)[0], sheet.row(row)[1]
	if none_value_count(sheet.row(row)) == 1:
		for element in sheet.row(row):
			if element.value != '':
				#print element.value
				client = MongoClient('localhost', 27017)
				coll_name = element.value.replace(' ', '_').lower()
				print coll_name
				db = client['audio_clips']
				#db.authenticate(user[1], user[2])
				collection = db[coll_name]    
	else:


		element = sheet.row(row)[1]
		if element.value != '':
			firstname=element.value.strip().title()
			print 'firstname',firstname
			lastname = sheet.row(row)[0].value.strip().title()
		else :
			name = sheet.row(row)[0].value.title()
			if ',' in name:
				names =  name.split(',')
			if '/' in name:
				names = name.split('/')
			else:
				name = name.split(' ')

			lastname = names[0].strip()
			firstname = names[1].strip()
			print lastname, firstname

		element = sheet.row(row)[2]
		if ctype_text.get(element.ctype) == 'xldate':
			bdate = xldate_to_datetime(element.value)
		else:
			bdate = element.value.strip().decode('utf-8')
		print bdate
		
		element = sheet.row(row)[4]
		if ctype_text.get(element.ctype) == 'number':
			audio_clip = int(element.value)
		else:
			audio_clip =  element.value
		print 'audio_clip', audio_clip

		element = sheet.row(row)[5]
		program = ''
		if element.value !='':
			print 'program type', ctype_text.get(element.ctype)
			if ctype_text.get(element.ctype) == 'number':
				program = int(element.value)
			if ctype_text.get(element.ctype) == 'text':
				program = element.value.strip().lower()
			if ctype_text.get(element.ctype) == 'xldate':
				program = xldate_to_datetime(element.value)

			print row, program

		audio_link = sheet.row(row)[7].value.strip()
		print audio_link

		userRecord = collection.find_one({'lastname': lastname, 'firstname': firstname})
		if not userRecord:
			index = 'index'+str(1)
			index = audio_link
			programs = {index:{'broadcast_date': bdate,
                                 'audio_clip' : audio_clip,
                                 'program'     : program,
                                 'audio_link'   : audio_link,

			} }
			collection.insert({'firstname'    : firstname,
                                 'lastname'   : lastname,
                                 'programs'   :programs,
                                })
		else:
			programs = userRecord['programs']
			index_num = len(programs.keys())+1
			#print 'index', index_num
			index = 'index'+str(index_num)
			index = audio_link
			
			if not if_audio_exists(programs, audio_clip):
				programs = programs + Dict({index:{'broadcast_date': bdate,
                                 'audio_clip' : audio_clip,
                                 'program'     : program,
                                 'audio_link'   : audio_link,

				}})
				collection.update_one(
                  {'lastname': lastname, 'firstname': firstname},
                  {
                    "$set" :  {'programs':programs,
                              },
                  }
                )
			
		'''
		for element in sheet.row(row):
			if element.value != '':
				print element.ctype, element, ctype_text.get(element.ctype)
				if element.ctype ==3:
					print xldate_to_datetime(element.value)
				else:
					if ctype_text.get(element.ctype) == 'number':
						print int(element.value)
					else:
						if ctype_text.get (element.ctype) == 'text':
							print element.value.strip().decode('utf-8')
						else:
							print element.value
						#print str(element).split(':')[1]
	    '''