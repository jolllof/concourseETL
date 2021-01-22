#log name to include some form of date/time

from os import system, environ
import requests
import json
from datetime import datetime
from multiprocessing import Pool
import pandas as pd
from sqlalchemy import types, create_engine
import time
import logging
from transform import *
import concoursefig as cfg

api_key= cfg.cred['key']
HEADER={'X-AUTH-KEY': api_key}
params=['past', 'present', 'future']
logfile=cfg.cred['desktop'] + f'zconcourse.log'
logging.basicConfig(filename= logfile, level=logging.DEBUG)

system('cls')

domain=cfg.cred['url']

def course_ids(url):
	logging.debug('getting course ids')
	url += 'course_ids&year=2021&timeframe=current_future'

	r=requests.get(url, headers=HEADER)
	response=r.json()
	return [sid['id'] for sid in response] #just ids not ext_id

def course_info(course_id):
	url=domain + f'course_info&course_id={course_id}'
	r=requests.get(url, headers=HEADER)
	response=r.json()

	return response

def oracle_connect():
	#Database credentials
	dbuser=cfg.cred['proxyuser']
	dbpass=cfg.cred['password']
	dbase=cfg.cred['WHD']

	connstr="oracle://{}:{}@{}".format(dbuser,dbpass,dbase)
	conn=sqlalchemy.create_engine(connstr)

	#creates oracle connection
	# conn=cx_Oracle.connect(dbuser, dbpass, dbase, encoding="UTF-8", nencoding="UTF-8")

	return conn

def oracle_run(SQL, conn):
 	#runs SQL queries
	cursor=conn.cursor()
	cursor.execute(SQL)
	return cursor

def main():
	start_time=time.time()
	logging.debug('start time:', start_time)

	idlist=course_ids(domain)

	total_items=len(idlist)
	logging.debug('processing', total_items, 'items')

	transformer=Transform() #creating a transformer object


	with Pool() as p:
		res=p.map(course_info, idlist)

	for item in res:
		transformer.master(item)



	syllabus=pd.DataFrame(data=transformer.syl)
	permissions=pd.DataFrame(data=transformer.perm)
	description=pd.DataFrame(data=transformer.desc)
	information=pd.DataFrame(data=transformer.info)
	rationale=pd.DataFrame(data=transformer.rati)
	outcomes=pd.DataFrame(data=transformer.outc)
	resources=pd.DataFrame(data=transformer.reso)
	assignment=pd.DataFrame(data=transformer.assi)
	grading=pd.DataFrame(data=transformer.grad)
	policy=pd.DataFrame(data=transformer.poli)
	schedule=pd.DataFrame(data=transformer.sche)

	print('syllabus\n', syllabus, '\n')
	print('permissions\n', permissions, '\n')
	print('description\n', description, '\n')
	print('contact info\n', information, '\n')
	print('rationale\n',rationale, '\n')
	print('outcomes\n',outcomes, '\n')
	print('resources\n',resources, '\n')
	print('assignment\n',assignment, '\n')
	print('grading\n',grading, '\n')
	print('policy\n',policy, '\n')
	print('schedule\n', schedule, '\n')

	total_time=round(float(time.time()-start_time) / 60, 2)
	message='TOTAL RUNTIME for' + str(total_items) +'items was: ' + str(total_time)+'minutes'
	logging.debug(message)


if __name__ == '__main__':
	main()
