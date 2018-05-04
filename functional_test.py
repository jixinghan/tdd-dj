from selenium import webdriver

broswer = webdriver.Chrome()
broswer.get('http://localhost:8000')

assert 'Django' in broswer.title
