# -*- coding: utf-8 -*-

import os
import urllib
import json
import subprocess

songList = None
# 获取歌曲列表的URL，注意不同channel的值对应不同的列表
PLAY_LIST_URL = 'http://douban.fm/j/mine/playlist?type=n&channel='
# 获取验证码ID的URL
CAPTCHA_ID_URL = 'http://douban.fm/j/new_captcha'
# 获取验证码的URL，尾部加上验证码ID
CAPTCHA_URL = 'http://douban.fm/misc/captcha?size=m&id='
# 登录URL
LOGIN_URL = 'http://douban.fm/j/login'
# 存音乐大根目录
MUSIC_PATH = 'music'

def login(username, password):
	print '获取验证码...'
	pageSource = None
	# 获取验证码ID
	try:
		pageSource = urllib.urlopen(CAPTCHA_ID_URL)
	except Exception, data:
		print Exception, ":", data
	captchaId = pageSource.read().strip('"')
	# 获取验证码
	try:
		pageSource = urllib.urlopen(CAPTCHA_URL + captchaId)
	except Exception, data:
		print Exception, ":", data
	captchaContent = pageSource.read()
	# 保存验证码
	saveCaptcha(captchaContent)

	captcha = raw_input('验证码：')
	openCaptcha()

	print '正在登录...'
	# 添加登录参数
	params = urllib.urlencode({
		'source': 'radio',
		'alias': username,
		'form_password': password,
		'captcha_solution': captcha,
		'captcha_id': captchaId,
		'remember': 'on',
		'task': 'sync_channel_list'})
	# 登录
	try:
		pageSource = urllib.urlopen(LOGIN_URL, params)
	except Exception, data:
		print Exception, ":", data
	# 获取服务器返回数据
	response = json.loads(pageSource.read())
	if 'err_msg' in response.keys():
		print response['err_msg']
		return False
	else:
		print '登录成功'
		return True

# 保存验证码图片
def saveCaptcha(content):
	file = open('captcha.jpg', 'wb')
	file.write(content)
	file.close()

# 保存音乐，包括专辑封面和音乐文件
def saveMusic(title, artist, coverUrl, musicUrl):
	# 为每一首音乐存储单独的文件夹
	musicPath = title + '_' + artist
	if os.path.exists(musicPath) and os.path.isfile(musicPath):
		os.remove(musicPath)
	if not os.path.exists(musicPath):
		os.mkdir(musicPath)
	# 更改当前路径
	os.chdir(musicPath)

	pageSource = None
	# 保存封面
	coverName = coverUrl.split('/')[-1]
	try:
		pageSource = urllib.urlopen(coverUrl)
	except Exception, data:
		print Exception, ":", data
	file = open(coverName, 'wb')
	file.write(pageSource.read())
	file.close()
	# 保存音乐
	musicName = musicUrl.split('/')[-1]
	try:
		pageSource = urllib.urlopen(musicUrl)
	except Exception, data:
		print Exception, ":", data
	file = open(musicName, 'wb')
	file.write(pageSource.read())
	file.close()

	# 回退到之前到路径
	os.chdir('..')

# 打开验证码图片
def openCaptcha():
	pass

def getPlayList(result = False):
	channel = '0'
	if result:
		channel = '-3'

	pageSource = None
	# 获取歌曲列表
	try:
		pageSource = urllib.urlopen(PLAY_LIST_URL + channel)
	except Exception, data:
		print Exception, ":", data
	playList = json.loads(pageSource.read())

	if playList['song'] == []:
		print '获取歌曲列表失败'
		return

	# 创建音乐存储根路径
	if os.path.exists(MUSIC_PATH) and os.path.isfile(MUSIC_PATH):
		os.remove(MUSIC_PATH)
	if not os.path.exists(MUSIC_PATH):
		os.mkdir(MUSIC_PATH)
	# 更改当前路径
	os.chdir(MUSIC_PATH)
	# 存储音乐
	for song in playList['song']:
		title = song['title']
		artist = song['artist']
		coverUrl = song['picture']
		musicUrl = song['url']

		saveMusic(title, artist, coverUrl, musicUrl)

	# 回退到之前到路径
	os.chdir('..')

def main():
	#username = raw_input('用户名：')
	#password = raw_input('密码：')
	username = 'double0291@126.com'
	password = 'double19891102'
	result = login(username, password)
	getPlayList(result)

if __name__ == '__main__':
	main()


