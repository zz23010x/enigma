import sys, os

print("选中ftp行复制资源地址 关闭界面直点x")
maskingword = ['.svn','资源地址.py']
for filename in os.listdir(os.path.dirname(__file__)):
	if all(word not in filename for word in maskingword):
		print('资源名:%s\nftp://192.168.12.34/pub/Resources/%s/list.csv.gz' % (filename,filename))
while (1):
	pass