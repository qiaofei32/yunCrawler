#encoding=utf8
import web
import time

db = web.database(dbn='mysql', db='yun_crawler', user='root', pw='root')

def submit_job(task_url, selected_items, pagination):
	task_add_time = time.strftime("%Y-%d-%m %H:%M:%S")
	db.insert('task_list',
			  task_url=task_url,
			  task_match_dom=selected_items,
			  task_pagination=pagination,
			  task_add_time = task_add_time
	)

