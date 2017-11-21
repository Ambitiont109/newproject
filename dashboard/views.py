# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

import requests
# Create your views here.
def index(request):
	r = requests.get('https://www.dashninja.pl/api/masternodes/?pubkeys=["Xn1iu5Cg9yHRZFqQggmzjWzWcxqorHvCP8"]',verify='/home/boris/Desktop/ca.crt')
	if (r.status_code != 200):	#Fail
		return HttpResponse("Get Data From Third Party Failed")
	dict_data = r.json()		# convert returned value 'r' from requets.get() to Dictionary data. Here r is Json Data.
	data1 = dict_data['data'][0] # Get MainData from parsed Data.
	return render(request,'dashboard/index.html',{'data':data1})  #show index.html. Here {'data':data1} menas that indicate data1 with data in .html