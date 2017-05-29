from django.template.loader import get_template
from django.http import HttpResponse, JsonResponse
import urllib.request
from bs4 import BeautifulSoup
from .models import Student, Score, LearningClub
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.core.serializers import serialize # User for return json date with ajax
import json
from django.db.models import Q
from selenium import webdriver
from time import sleep 
from selenium.webdriver.common.keys import Keys # Import Keyboard events
import datetime 

def index(request):
	template = get_template('index.html')
	if 'search_name' in request.session:
		search_name = request.session['search_name']
	html = template.render(locals())
	return HttpResponse(html)
	
def scraping(request):
	start_day = datetime.date(2017,2,20) # 
	today = datetime.date.today()
	this_week = int((today - start_day).days / 7 + 1)

	driver = webdriver.Chrome()
	driver.get('http://coding.pu.edu.tw/')

	# Waiting for the wetsite(http://coding.pu.edu.tw/) finish loading
	sleep(3) 

	# Clear input field of account 
	driver.find_element_by_xpath("//div[@id='user_div']/div[@class='PiAll']/table[@class='main']/tbody/tr/td[2]/table/tbody/tr[3]/td/span[2]/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/input").clear()
	# Input account
	driver.find_element_by_xpath("//div[@id='user_div']/div[@class='PiAll']/table[@class='main']/tbody/tr/td[2]/table/tbody/tr[3]/td/span[2]/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/input").send_keys("410328420")
	# Clear input field of password 
	driver.find_element_by_xpath("//div[@id='user_div']/div[@class='PiAll']/table[@class='main']/tbody/tr/td[2]/table/tbody/tr[3]/td/span[2]/table/tbody/tr/td/table[2]/tbody/tr[3]/td[2]/input").clear()
	# Input password
	driver.find_element_by_xpath("//div[@id='user_div']/div[@class='PiAll']/table[@class='main']/tbody/tr/td[2]/table/tbody/tr[3]/td/span[2]/table/tbody/tr/td/table[2]/tbody/tr[3]/td[2]/input").send_keys("lost5270")
	# Submit account and password
	driver.find_element_by_xpath("//div[@id='user_div']/div[@class='PiAll']/table[@class='main']/tbody/tr/td[2]/table/tbody/tr[3]/td/span[2]/table/tbody/tr/td/table[2]/tbody/tr[4]/td[2]/input").click()

	# Waiting for website loading 3 seconds
	sleep(3)
	# Click the class of 課程列表
	driver.find_element_by_xpath("//table[@class='main']/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/span/table/tbody/tr/td/table/tbody/tr[9]/td/nobr").click() 

	# Waiting for website loading 3 seconds
	sleep(3)
	events_list = driver.find_elements_by_xpath("//div[@id='user_div']/div[@class='PiAll']/table[@class='main']/tbody/tr/td[2]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/span[2]/table/tbody/tr")
	# Score.objects.all().delete()

	for event in events_list:
		coding_level = event.find_element_by_xpath("td/table/tbody/tr/td[2]/a/span/nobr/span").get_attribute("innerHTML").split(" ")[0]
		event.find_element_by_xpath("td/table/tbody/tr/td/a").click()
		sleep(10)
		page_length = int(driver.find_element_by_id("sp_1_pager").get_attribute("innerHTML"))
		for page_num in range(1, page_length + 1):
			driver.find_element_by_class_name("ui-pg-input").clear()
			driver.find_element_by_class_name("ui-pg-input").send_keys(page_num)
			driver.find_element_by_class_name("ui-pg-input").send_keys(Keys.ENTER)
			transcripts = driver.find_elements_by_xpath("//div[@class='ui-jqgrid-bdiv']/div/table/tbody/tr")
			for personal_trascript in transcripts:
				if personal_trascript.get_attribute('role') == 'row':
					student_id = personal_trascript.find_element_by_xpath('td[3]').get_attribute("innerHTML")
					student_name = personal_trascript.find_element_by_xpath('td[4]').get_attribute("innerHTML")
					numbers_of_completed_questions = personal_trascript.find_element_by_xpath('td[7]').get_attribute("innerHTML")
					# print("student_id: ", student_id, "student_name: ", student_name, "numbers_of_completed_questions: ", numbers_of_completed_questions)
					# learning_club = LearningClub.objects.get(lc_id = '1')
					# if Student.objects.filter(st_id = student_id).count() == 0:
					# 	data = Score.objects.create(
					# 				st_id = student_id,
					# 				st_name = student_name,
					# 				lc_id = learning_club
					# 			)
					# 	data.save()
					st_id_ref = Student.objects.get(st_id = student_id)
					data = Score.objects.create(
							st_id = st_id_ref,
							sc_num_of_cpl = numbers_of_completed_questions,
							sc_level = coding_level,
							sc_week = this_week
						)
					data.save()

	driver.quit()

	return redirect("/")

def get_personal_score(request):
	name = request.POST.get('search-name')

	if Student.objects.filter(st_name = name).count() != 0:
		obj = Student.objects.get(st_name = name)
		score_data = Score.objects.filter(st_id = obj)
		data = serialize('json', score_data)
	else:
		data = json.dumps({"fail":"fail"})

	return HttpResponse(data, content_type='json')

def search(request):
	template = get_template('search.html')
	request.session['search_name'] = request.POST.get('search-name')
	print(request.POST.get('search-name'))
	if 'search_name' in request.session: 
		search_name = request.session['search_name']
	html = template.render(locals())
	return HttpResponse(html)

def ta_manage(request):
	template = get_template('ta_manage.html')
	html = template.render(locals())
	return HttpResponse(html)

