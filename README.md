# Intro

Tools to help you migrate files from hexo to hugo.

# Usage

```
usage: hexo2hugo.py [-h] [--src SRC] [--dest DEST] [--remove-date-from-name]
                    [--verbose]

optional arguments:
  -h, --help            show this help message and exit
  --src SRC             Hexo posts directory
  --dest DEST           Destination directory
  --remove-date-from-name
                        Remove date from file name
  --verbose             Output level
```

Example:

```
$ ./hexo2hugo.py --src=./t/hexo/ --dest=./t/hugo/ --remove-date-from-name --verbose
Hexo2hugo (Hexo): [INFO] Total 3 files found
Hexo2hugo (Hexo): [INFO] Process 2016-07-30-LLD-in-zabbix.markdown now, meta: {'title': 'Test file', 'date': datetime.datetime(2016, 7, 30, 14, 9, 58), 'permalink': 'Just a test', 'tags': ['zabbix', 'monitor'], 'categories': ['Test', 'te']}, body length: 71
Hexo2hugo (Hexo): [INFO] Write to LLD-in-zabbix.markdown, meta: title = "Test file"
date = "2016-07-30T14:09:58+08:00"
tags = ["zabbix", "monitor"]
categories = ["Test", "te"]
description = ""
slug = "Just a test"

Hexo2hugo (Hexo): [INFO] Process test-html.html now, meta: {'title': 'test html', 'date': datetime.datetime(2016, 7, 30, 14, 9, 58), 'permalink': 'Just-a-test', 'tags': 'zabbix'}, body length: 147
Hexo2hugo (Hexo): [INFO] Write to test-html.html, meta: title = "test html"
date = "2016-07-30T14:09:58+08:00"
tags = ["zabbix"]
description = ""
slug = "Just-a-test"

Hexo2hugo (Hexo): [INFO] Process test.md now, meta: {'title': 'ttttt', 'date': datetime.datetime(2016, 7, 30, 14, 9, 58), 'permalink': 'Just-a-test', 'tags': 'zabbix'}, body length: 5
Hexo2hugo (Hexo): [INFO] Write to test.md, meta: title = "ttttt"
date = "2016-07-30T14:09:58+08:00"
tags = ["zabbix"]
description = ""
slug = "Just-a-test"
```

It is used by me and may not fit your situation, feel free to fork and modify :)
