# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import requests
# Create your views here.
import math

def millify(n):
	millnames = ['',' K',' M',' B',' Trillion']
	n = float(n)
	millidx = max(0,min(len(millnames)-1,
					int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

	return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])
def get_data_from_api(url): # as you can realize from name of method, this gets data from api what you provide.
	r = requests.get(url)
	# r = requests.get(url,verify='/home/boris/Desktop/ca.crt')
	if (r.status_code != 200):	#Fail
		return None
	dict_data = r.json()		# convert returned value 'r' from requets.get() to Dictionary data. Here r is Json Data.
	return dict_data
def index(request):
	api_url = 'https://www.dashninja.pl/api/masternodes/?pubkeys=["Xn1iu5Cg9yHRZFqQggmzjWzWcxqorHvCP8"]'
	data = get_data_from_api(api_url)
	if (data is None):	#Fail
		return HttpResponse("Get Data From Third Party Failed")
	return render(request,'dashboard/index.html',{'data':data})  #show index.html. Here {'data':data1} means that indicate data1 with data in .html

class Key_met(View):
	def get(self,request):
		convert_info = None
		if convert_info is not None:
			self.global_url = "https://api.coinmarketcap.com/v1/global/?convert="+convert_info
			self.dash_url = "https://api.coinmarketcap.com/v1/ticker/dash/?convert="+convert_info
		else:
			self.global_url = "https://api.coinmarketcap.com/v1/global/"
			self.dash_url = "https://api.coinmarketcap.com/v1/ticker/dash/"
		result = {}
		# Get Glo
		global_data = get_data_from_api(self.global_url)
		if global_data is None:
			return render(request,"error.html")
		print(global_data)
		result['cmp'] = global_data['total_market_cap_usd']
		dash_data = get_data_from_api(self.dash_url)
		if dash_data is None:
			return render(request,"error.html")
		print(dash_data)
		dash_data = dash_data[0]
		result['rank'] = dash_data['rank']		# Dash Market Position
		result['dmp'] = dash_data['market_cap_usd'] # Dash Market Captiality
		result['dpp'] = dash_data['price_usd']
		result['dcs'] = dash_data['available_supply']
		result['dv'] = dash_data['24h_volume_usd']
		for key in result:
			if(key == 'rank'):
				continue
			result[key] = millify(float(result[key]))
		return render(request,"dashboard/dash.html",{'dash_info':result})