#coding= utf8
import requests,json
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime,date
import os,time,sys
import pandas,numpy
import urllib.parse
import re
import random
import json

# now_page=1

def getHtml(url,retry=0):

	headers1 = {
    	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) '
					'Version/9.1.3 Safari/601.7.8 '
	}
	headers2 = {
	    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) '
	                  'Version/10.0.3 Safari/602.4.8'
	}
	headers3 = {
	    'user-agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) '
	                  'Version/4.0.4 Mobile/7B334b Safari/531.21.10 '
	}
	headers4 = {
		"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.160 Safari/537.22"
	}
	headers5 = {
	    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
	                  'Chrome/55.0.2883.87 Safari/537.36 '
	}
	headers=[headers1, headers2, headers3, headers4, headers5]
	maxRetryTimes=5
	try:
		res=requests.get(url,headers=headers[random.randint(0,4)], timeout=10)
		res.encoding='utf-8'
		res.raise_for_status()
		source_code=res.text
		return source_code
	except:
		source_code = 'error'
		while (source_code == 'error'):
			if retry <= maxRetryTimes:
				retry += 1
				time.sleep(3)
				print ('Retry times :',str(retry))
				return getHtml(url,retry)
			else:
				# soup='URL error'
				print ('Please check URL')
				return sys.exit()


def singlePage(url):

	save_path=os.path.dirname(__file__)
	chrome_path='D:/chromedriver_win32/chromedriver.exe'
	p_path='C:/phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs.exe'
	tag_n='9487'

	web = webdriver.Chrome(chrome_path)
	# web = webdriver.PhantomJS(executable_path=p_path)
	web.get(url)
	time.sleep(3)
	# js="var q=document.documentElement.scrollTop=10000"
	# web.execute_script(js)
	web.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(3)
	# print(type(web.page_source))
	source=web.page_source
	# print(web.page_source)
	# source.replace('')
	soup=BeautifulSoup(web.page_source,'lxml')
	print('*'*50)
	# print(soup)

	web.close()
	web.quit()
	
	page=0
	reply_author_list=[]
	reply_date_list=[]
	reply_time_list=[]
	reply_content_list=[]

	#看板名稱ok-------------------------------------------
	Board_name=soup.find('div',{'class','sidebar-category'})
	Board_name=Board_name.find('li',{'class','active'})
	Board_name=Board_name.find_all('a')
	Board_name=Board_name[0].get_text()

	print("看板名稱:"+Board_name)

	#日期區間ok-------------------------------------------
	Date_range=soup.find('div',{'class','forum-topic-date'})
	Date_range=Date_range.get_text()
	Date_range_year=Date_range[0:4]#只擷取字串前4字元
	Date_range_month=Date_range[5:7]
	Date_range=Date_range_year+'-'+Date_range_month

	# print("日期區間"+Date_range)

	#文章類型ok-------------------------------------------
	Type=soup.find('div',{'class','sidebar-category'})
	Type=Type.find('li',{'class','active'})
	Type=Type.find('li',{'class','active'})
	if Type == None :
		Type=Board_name
	else:
		Type=Type.find_all('a')
		Type=Type[0].get_text()
	# print("文章類型:"+Type)

	#文章標題ok-------------------------------------------
	Title=soup.find('div',{'class','forum-topic-reverse'})
	Title=Title.find_all('h1')
	Title=Title[0].get_text()

	# print("文章標題"+Title)

	#文章id ok-------------------------------------------
	ID=url.find("topic_id")
	ID=url[ID+9:]
	# print("文章id:"+ID)

	#文章日期ok----------------------------------------------
	Date=soup.find('div',{'class','forum-topic-date'})
	Date=Date.get_text()
	Date_day=Date[8:10]
	Date=Date_range+'-'+Date_day
	# print("文章日期:"+Date)

	#文章時間ok----------------------------------------------
	Time=soup.find('div',{'class','forum-topic-date'})
	Time=Time.get_text()
	Time=Time[11:]#只擷取字串前10字元
	# print("文章時間:"+Time)

	#[文章作者id]ok----------------------------------------------
	Author=soup.find('div',{'class','forum-topic-profile'})
	Author=Author.find_all('a')
	Author=Author[0].get_text()

	# print("文章作者id:"+Author)

	#文章內文ok----------------------------------------------
	Content=soup.find('div',{'class','forum-topic-body'})
	Content=Content.get_text()
	whole_Content=str(Content)
	whole_Content=Content.replace("\xa0","")
	whole_Content=Content.replace("\u3000","")
	# print("文章內文:"+whole_Content)

	#回應者ok----------------------------------------------
	Reply_num=soup.find('span',{'class','cmt-num'})
	Reply_num=int(Reply_num.get_text())
	# print("回應總數",Reply_num)
	
	Reply_author=soup.find_all('a',{'class','forum-reply-name'})
	for each_author in Reply_author:
		Reply_author=each_author.get_text()
		reply_author_list.append(Reply_author)
	# print("回應者",reply_author_list)

	#回應日期ok-------------------------------------------------
	Reply_date=soup.find_all('div',{'class','forum-reply-date'})
	for each_date in Reply_date :
		Reply_date=each_date.get_text()
		Reply_date=Reply_date[0:4]+'-'+Reply_date[5:7]+'-'+Reply_date[8:10]
		reply_date_list.append(Reply_date)
	#回應時間ok-------------------------------------------------
		reply_time_list.append(Reply_date[11:16])
	# print(reply_date_list)
	# print(reply_time_list)

	#回應內容ok-------------------------------------------------
	Reply_content=soup.find_all('div',{'class','forum-reply-body'})
	for each_content in Reply_content :
		Reply_content=each_content.get_text()
		Reply_content=str(Reply_content)
		Reply_content=Reply_content.replace("\xa0","")
		Reply_content=Reply_content.replace("\u3000","")
		reply_content_list.append(Reply_content)
	# print(reply_content_list)

	article={
		'Board_name':Board_name,
		'Type':Type,
		'Title':Title,
		'ID':ID,
		'Date':Date,
		'Time':Time,
		'Author':[Author],
		'Url':url,
		'Content':whole_Content,
		'Reply':[],
	}
	reply_count=0
	if Reply_num != 0 :
		for reply_each in reply_author_list :
			article_reply={}
			article_reply["Reply_author"]=reply_each
			article_reply["Reply_date"]=reply_date_list[reply_count]
			article_reply["Reply_time"]=reply_time_list[reply_count]
			article_reply["Reply_content"]=reply_content_list[reply_count]
			article["Reply"].append(article_reply)
			reply_count+=1
		return article

def getIndex(index_url):

	save_path=os.path.abspath(os.path.dirname(__file__))
	chrome_path='D:/chromedriver_win32/chromedriver.exe'
	p_path='C:/phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs.exe'
	web = webdriver.Chrome(chrome_path)
	web.get(index_url)
	time.sleep(10)
	web.execute_script("window.scrollTo(0, document.body.scrollHeight);") #滑視窗
	time.sleep(3)
	source=web.page_source
	soup=BeautifulSoup(web.page_source,'lxml')
	print('*'*50)
	web.close()
	web.quit()
# ##########################################################

	category=soup.find('div',{'class','sidebar-category'})
	category=category.find('li',{'class','active'})
	category=category.find_all('a')
	category=category[0].get_text().replace(' ','')

	# print('Category :',category)
	#文章名稱ok-------------------------------------------
	title=soup.find('ul',{'id':'forum-list'})
	title_url=title.find_all('a')
	# print("文章名稱",title_url)

	# 文章發布日期----------------------------------------
	datetime=soup.find_all('div',{'class':'forum-date'})

	# 文章回應數----------------------------------------
	Reply_num=soup.find_all('div',{'class','forum-comments'})


	print('*'*30)

	url_list=[]#儲存每一頁的文章超連結
	all_article={}
	url_list=[]
	now_page=1#若留言數大於一則翻頁
	error_article=[]
	a=0#計算文章數

	for t_url in title_url:
		each_url='https://fgforum.fashionguide.com.tw'+t_url.get('href')
		url_list.append(each_url)
		article=singlePage(each_url)
		page=(int(Reply_num[a].get_text())//10)+1#除法只取整數
		while now_page < page: #記錄翻頁留言
			now_page+=1
			article2=singlePage(each_url+'&page='+str(now_page))
			for each_article in article2["Reply"] :
				article["Reply"].append(each_article)
		if article == None:
			error_article.append(each_url)
		Date_range=datetime[a].get_text()
		datetime_year=Date_range[0:4]#只擷取字串前4字元
		datetime_month=Date_range[5:7]
		Date_range=datetime_year+'-'+datetime_month
		if Date_range not in all_article:
			all_article[Date_range]=[]
			all_article[Date_range].append(article)
		else:
			all_article[Date_range].append(article)
		time.sleep(0.87)
		# print(all_article)
		a+=1

	print('Creating Json...')
	if not os.path.exists(save_path+'/fg/'):
		os.mkdir(save_path+'/fg/')
	if not os.path.exists(save_path+'/fg/'+category):
		os.mkdir(save_path+'/fg/'+category)
	#創建error記錄檔
	if not os.path.exists(save_path+'/fg/'+category+'/error.json'):
		with open(save_path+'/fg/'+category+'/error.json','w',encoding='utf-8') as output:
				json.dump(error_article,output,indent=4,ensure_ascii=False)
	else:
		with open(save_path+'/fg/'+category+'/error.json','r',encoding='utf-8') as raw:
				raw_data=json.load(raw)
		for each_error in error_article:
			raw_data.append(each_error)
		with open(save_path+'/fg/'+category+'/error.json','w',encoding='utf-8') as output:
				json.dump(raw_data,output,indent=4,ensure_ascii=False)

	for Date_range in all_article:
		print(Date_range)
		if not os.path.exists(save_path+'/fg/'+category+'/'+Date_range+'.json'):
			all_article={
				'Source_type':'社群論壇',
				'Source_name':'fashionguide',
				'Board_name':category,
				'Date_range':Date_range,
				'Articles':all_article[Date_range]
			}
			with open(save_path+'/fg/'+category+'/'+Date_range+'.json','w',encoding='utf-8') as output:
				json.dump([all_article],output,indent=4,ensure_ascii=False)
		
		else:

			with open(save_path+'/fg/'+category+'/'+Date_range+'.json','r',encoding='utf-8') as raw:
				raw_data=json.load(raw)
				raw_data=raw_data[0]
			for art in all_article[Date_range]:
				if art not in raw_data['Articles']:
					raw_data['Articles'].append(art)
				else:
					pass
			with open(save_path+'/fg/'+category+'/'+Date_range+'.json','w',encoding='utf-8') as json_update:
				json.dump([raw_data],json_update,indent=4,ensure_ascii=False)	

def main():
	
	url="https://fgforum.fashionguide.com.tw/newest_list?forum_id=1"
	getIndex(url)
	
	a=2
	while a < 5 :#論壇翻頁
		url="https://fgforum.fashionguide.com.tw/newest_list?forum_id=1&page="
		url+=str(a)
		getIndex(url)
		a+=1


if __name__ == '__main__':
	# main(sys.argv[1])
	main()
