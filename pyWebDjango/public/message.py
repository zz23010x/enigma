# -*-coding:utf-8-*-

import os, sys
import linecache

comm_msg = {}
#static const map<string, uint8>::value_type caituan[] =
#{
	#map<string, uint32>::value_type("com.smartspace.lwzr.yueka", 1),
#};
#static const map<string, uint8> caituanyan(caituan, caituan + sizeof(caituan) / sizeof(caituan[0]));

def work_msg(dic):
	for key,val in dic.items():
		body = []
		if ('enum' in val['type']):
			head = 'static const map<uint32, string>::value_type %ssize[] =\n{\n' % (key.lower())
			for k,v in enumerate(val['body']):
				if ('=' not in v):
					continue
				body.append('map<uint32, string>::value_type(%s::%s, "%s"),' % (key,v.strip().split('=')[0].strip(),v.strip().split('//')[-1].strip()))
			title = '\n};\nstatic const map<uint32, string> struct_%s(%ssize, %ssize + sizeof(%ssize) / sizeof(%ssize[0]));\n' % (key,key.lower(),key.lower(),key.lower(),key.lower())
			print('%s %s %s' % (head,'\n'.join(body), title))
		# elif ('message' in val['type']):
		# 	head = 'static const map<uint32, string>::value_type %ssize[] =\n{\n' % (key.lower())
		# 	for k,v in enumerate(val['body']):
		# 		if (';' not in v):
		# 			continue
		# 		body.append('map<uint32, string>::value_type(%s, "%s"),  // %s' % (k,v.strip().split('//')[-1].strip(),v.strip().split(';')[0].strip().split(' ')[-1]))
		# 	title = '\n};\nstatic const map<uint32, string> struct_%s(%ssize, %ssize + sizeof(%ssize) / sizeof(%ssize[0]));\n' % (key,key.lower(),key.lower(),key.lower(),key.lower())
		# 	print('%s %s %s' % (head,'\n'.join(body), title))
		elif ('error' in val['type']):
			error_name = input('//结构名称:')
			head = 'static const map<uint32, string>::value_type %ssize[] =\n{\n' % (error_name.lower())
			for k,v in enumerate(val['body']):
				if ('=' not in v):
					if('//' in v):
						print(v)
					continue
				body.append('map<uint32, string>::value_type(%s::%s, "%s"),' % (key,v.strip().split('=')[0].strip(),v.strip().split('//')[-1].strip()))
				#body.append('map<uint32, string>::value_type(%s, "%s"),' % (v.strip().split(';')[0].split('=')[-1].strip(),v.strip().split('//')[-1].strip()))
			title = '\n};\nstatic const map<uint32, string> struct_%s(%ssize, %ssize + sizeof(%ssize) / sizeof(%ssize[0]));\n' % (error_name.upper(),error_name.lower(),error_name.lower(),error_name.lower(),error_name.lower())
			print('%s %s %s' % (head,'\n'.join(body), title))

def work_common(fileurl):
	fp = open(fileurl,'r',encoding='utf-8')
	found = False
	comm_type = ''
	comm_name = ''
	comm_text = ''
	comm_body = []
	str = ''
	num = 0
	for line in fp.readlines():
		if found == True:
			str = str + line
			comm_body.append(line)
		if line.find('{') != -1:
			comm_type = lined.strip().split(' ')[0]
			comm_name = lined.strip().split('//')[0].split(' ')[-1]
			num = num + 1
			found = True
		if line.find('}') != -1:
			num = num - 1
			if (num != 0):
				continue
			comm_text = ''.join(str.split('}')).strip()
			if len(comm_body) != 0:
				 comm_body.pop();
			comm_msg.update({comm_name : {'type' : comm_type ,'body' : comm_body, 'text' : comm_text}})

			str = ''
			num = 0
			comm_body = []
			found = False
		lined = line
	work_msg(comm_msg)
	fp.close()

def work_error(fileurl):
	fp = open(fileurl,'r',encoding='utf-8')
	found = False
	comm_type = ''
	comm_name = ''
	comm_text = ''
	comm_body = []
	str = ''
	num = 0
	for line in fp.readlines():
		if found == True:
			str = str + line
			comm_body.append(line)
		if line.find('{') != -1:
			comm_name = lined.strip().split('//')[0].split(' ')[-1]
			num = num + 1
			found = True
		if line.find('}') != -1:
			num = num - 1
			if (num != 0):
				continue
			comm_text = ''.join(str.split('}')).strip()
			if len(comm_body) != 0:
				 comm_body.pop();
			comm_msg.update({comm_name : {'type' : 'error' ,'body' : comm_body, 'text' : comm_text}})

			str = ''
			num = 0
			comm_body = []
			found = False
		lined = line
	work_msg(comm_msg)
	fp.close()

if __name__=="__main__":
	try:
		for k,v in enumerate(sys.argv):
			if k != 0:
				if "msg_xx_common" in v or "msg_w" in v:
					work_common(v)
				elif "msg_xx_error" in v:
					work_error(v)
	except Exception as e:
		print(v, e)
		input("ERROR")
	finally:
		input("press any key exit")
