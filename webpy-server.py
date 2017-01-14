#encoding=utf8
import os
import re
import sys
import web
import time
import model
import urllib
import pandas
import requests
from pyquery import PyQuery
import HTMLParser
html_parser = HTMLParser.HTMLParser()

urls = (
	'/', 'Index',
	'/test/', 'Test',
	'/parse/(.*)', 'Parse',
	'/do/(.*)', 'Do',
	'/(.*)/(css|img|js)/(.*)', 'Static',
	'/(css|img|js)/(.*)', 'Static',
)

proxy = None
proxy = {"http": "http://127.0.0.1:8087"}
task_max_page = 10

def html_decode(html):
	html = html.replace("&#13;", "")
	html = html_parser.unescape(html)
	html = html.replace("$", "jQuery")
	return html.encode("utf8")

def notfound():
	return web.notfound("Sorry, the page you were looking for was not found.")

class Index:
	def GET(self):
		return render.index()

class Test:
	def GET(self):
		return render.test()

class Static:
	def GET(self, *args):
		dir, name = args[-2:]
		dir_path = 'templates/%s/' %dir
		ext = name.split(".")[-1]
		cType = {
			"css": "text/css",
			"png": "images/png",
			"jpg": "images/jpeg",
			"gif": "images/gif",
			"ico": "images/x-icon",
			"js" : "text/javascrip",
		}
		if name in os.listdir(dir_path):
			web.header("Content-Type", cType[ext])
			file_path = '%s/%s' %(dir_path, name)
			return open(file_path, "rb").read()
		else:
			raise web.notfound()

class Parse:
	def GET(self, _):
		user_data = web.input()
		# web.debug(user_data)
		url = user_data.url.encode("utf8")
		url = urllib.unquote(url)
		data = requests.get(url, proxies=proxy, verify=False).content
		dom = PyQuery(data)

		protocol = "http"
		if url.startswith("https://"):
			protocol = "https"
			www_part = url.replace("https://", "")
		elif url.startswith("http://"):
			protocol = "http"
			www_part = url.replace("http://", "")

		www_host = www_part.split("/", 1)[0]
		base_path = www_part.rsplit("/", 1)[0]

		head = html_decode(dom("head").html())
		body = html_decode(dom("body").html())

		css_links = dom("head link")
		css_links_rep = []
		for i in range(len(css_links)):
			link_url = css_links.eq(i).attr("href")
			stylesheet = css_links.eq(i).attr("rel")
			if not link_url or stylesheet != "stylesheet":
				continue
			link_url = link_url.encode("utf8")

			# web.debug("find css link: %s" %link_url)

			if link_url.startswith("https://"):
				continue
			elif link_url.startswith("http://"):
				continue
			elif link_url.startswith("//"):
				# web.debug("css link startswith: //")
				full_link_url = "http:%s" %(link_url)
				css_links_rep.append((link_url, full_link_url))
			elif link_url.startswith("/"):
				# web.debug("css link startswith: /")
				full_link_url = "%s://%s%s" %(protocol, www_host, link_url)
				css_links_rep.append((link_url, full_link_url))
			else:
				# web.debug("css link startswith: else")
				full_link_url = "%s://%s/%s" % (protocol, base_path, link_url)
				css_links_rep.append((link_url, full_link_url))

		js_links = dom("head script")
		js_links_rep = []
		for i in range(len(js_links)):
			link_url = js_links.eq(i).attr("src")
			if not link_url:
				continue
			link_url = link_url.encode("utf8")
			if link_url.startswith("https://"):
				continue
			elif link_url.startswith("http://"):
				continue
			elif link_url.startswith("//"):
				full_link_url = "http:%s" %(link_url)
				js_links_rep.append((link_url, full_link_url))
			elif link_url.startswith("/"):
				full_link_url = "%s://%s%s" %(protocol, www_host, link_url)
				js_links_rep.append((link_url, full_link_url))
			else:
				full_link_url = "%s://%s/%s" % (protocol, base_path, link_url)
				js_links_rep.append((link_url, full_link_url))

		for rep in css_links_rep:
			href_old, href_new = rep
			head = head.replace(href_old, href_new)

		for rep in js_links_rep:
			src_old, src_new = rep
			head = head.replace(src_old, src_new)

		raw_html = {
			# "head": "TEST",
			# "body": "TEST",
			"head": head,
			"body": body,
			"url" : url,
		}
		# return render.parse(raw_html1)
		return render.parse(raw_html)

class Do:
	def GET(self, _):
		user_data = web.input()
		selected_items = user_data.selected_items.encode("utf8")
		selected_items = urllib.unquote(selected_items)
		pagination = user_data.pagination.encode("utf8")
		pagination = urllib.unquote(pagination)
		task_url = user_data.task_url.encode("utf8")
		task_url = urllib.unquote(task_url)

		model.submit_job(task_url, selected_items, pagination)

		values = []
		columns = ["Page", "Text"]
		flag = True
		for page in range(1, task_max_page+1):
			url = pagination % page
			data = requests.get(url, proxies=proxy, verify=False).content
			dom = PyQuery(data)
			for selected_item in selected_items.split("|"):
				result = dom(selected_item)
				for i in range(len(result)):
					element = result.eq(i)
					t = [page]
					text = element.text().encode("utf8")
					href = element.attr("href")
					src  = element.attr("src")
					href = href.encode("utf8") if href else ""
					src  = src.encode("utf8") if src else ""

					t.append(text)
					if href:
						if "Href" not in columns:
							columns.append("Href")
						t.append(href)

					if src:
						if "src" not in columns:
							columns.append("Src")
						t.append(src)
					values.append(t)

		data_frame = pandas.DataFrame(values, columns=columns)
		file_name = "result/result-%d.csv" %(time.time())
		data_frame.to_csv(file_name, index=False)


app = web.application(urls, globals())
render = web.template.render('templates/')
app.notfound = notfound

if __name__ == '__main__':
	app.run()