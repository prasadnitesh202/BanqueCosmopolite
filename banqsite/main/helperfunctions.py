import datetime


def datefield_parse(date):
	date = date[0:19]
	res_date = datetime.datetime.strptime(date,"%Y-%m-%dT%H:%M:%S")
	return res_date



