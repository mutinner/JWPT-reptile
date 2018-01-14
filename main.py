import requests
from bs4 import BeautifulSoup
import re

r = requests.session()

def getJPG():
	url = 'http://jwpt.tjpu.edu.cn/validateCodeAction.do'
	path = 'code.jpg'
	jpg = r.get(url)
	with open(path, 'wb') as f:
		f.write(jpg.content)
		f.close()

def postHTML(url):
	postdata = {
		'zjh': '',
		'mm': '',
		'v_yzm': ''
	}
	getJPG()
	postdata['zjh']=input('username:')
	postdata['mm']=input('password:')
	postdata['v_yzm']=input('verification code:')
	s = r.post(url, data = postdata)
	soup = BeautifulSoup(s.text, 'html.parser')
	if(soup.title.string.find('错误')!=-1):
		print('System Error!')
	if(soup.title.string.find('URP')!=-1):
		print('Verification code Error!')
		return 1
	return 0

# def updateHTML(url, name):
# 	path = 'C://Users/mutin/Desktop/html/' + name
# 	s = r.get(url)
# 	s.encoding = s.apparent_encoding
# 	soup = BeautifulSoup(s.text, 'html.parser')
# 	with open(path, 'w', encoding = 'utf-8') as f:
# 		f.write(soup.prettify())
# 		f.close()
# 		print('Write Sucess!')

def drawUrl(url, root):
	s = r.get(url)
	s.encoding = s.apparent_encoding
	soup = BeautifulSoup(s.text, 'html.parser')
	table = soup.find_all('table')[4].tr.td.table.find_all('tr')[1:]
	info = []
	for tr in table:
		tds = tr.contents
		string = BeautifulSoup(tds[17].string,'html.parser').img.attrs['onclick']
		info.append([re.findall(r'\s+?(.+?)\r', tds[5].string)[0][10:], root + re.findall(r'[^\'/]+', string)[1]])
	return info

def getGrade(ulist):
	info = []
	for it in ulist:
		s = r.get(it[1])
		soup = BeautifulSoup(s.text, 'html.parser')
		table = soup.find_all('table')[4].tr.td.table.find_all('tr')[2].find_all('td')[1].table.tr.td.table
		trs = table.find_all('tr')[2:]
		cnt = []
		for tr in trs:
			for td in tr.find_all('td')[1:]:
				num = ""
				for i in td.string.split():
					num += i
				cnt.append(num)
		info.append([it[0],cnt])
	return info

def showInterface(url, semester, cName = ''):
	cnt = getGrade( drawUrl(url + semester ,url))
	if cName == '':
		for i in cnt:
			showGrade(i)
	else :
		pass

def showGrade(ulist):
	grade = ulist[1]
	print('{0:^10}\t{1:^40}'.format('课程名',ulist[0],chr(12288)))
	print('{0:^10}\t{1:^10}\t{2:^10}\t{3:^10}\t{4:^10}'.format('成绩分类','平时成绩','期中成绩','期末成绩','分类总成绩',chr(12288)))
	print('{0:^10}\t{1:^10}\t\t{2:^10}\t\t{3:^10}\t\t{4:^10}'.format('课堂成绩',grade[0],grade[1],grade[2],grade[3],chr(12288)))
	print('{0:^10}\t{1:^10}\t\t{2:^10}\t\t{3:^10}\t\t{4:^10}'.format('实验成绩',grade[4],grade[5],grade[6],grade[7],chr(12288)))
	print('{0:^10}\t{1:^10}\t\t{2:^10}\t\t{3:^10}\t\t{4:^10}'.format('实践成绩',grade[8],grade[9],grade[10],grade[11],chr(12288)))
	print('{0:^10}\t{1:^40}'.format('总成绩',grade[12],chr(12288)))
	for i in range(1,3):
		print()

def main():
	url = 'http://jwpt.tjpu.edu.cn/'
	login = 'loginAction.do'
	semester = 'gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=5600'
	while postHTML(url + login) == 1:
		pass
	showInterface(url, semester)

main()