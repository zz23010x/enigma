# -*-coding:utf-8-*-

import os, sys
import linecache
import time

errorlog = ''

def work_cg(fileurl):
	global errorlog
	fileName = (os.path.basename(fileurl)).split('.')[0] 
	cppFile = os.path.join( sys.path[0] , '.'.join([fileName , 'cpp']))
	hFile = os.path.join( sys.path[0] , '.'.join([fileName , 'h']) )
	fp = open(fileurl,'r',encoding='utf-8')
	fp2 = open(cppFile,'w')	
	fp3 = open(hFile,'w')	
	funcCase = {}
	funcName = ''
	funcExp = ''
	found = False
	for line in fp.readlines():
		if line.find('}') != -1 and found == True:
			found = False
			try:
				funcCase.update({funcName:{'para':funcPar,'expain':funcExp}})
			except Exception as e:
				errorlog = errorlog + funcName + "\t" + str(e) +"\n"
		if found == True and line.find('{') == -1:
			try:
				funcPar.append([line.strip().split(' ')[0],line.strip().split(';')[0].split('=')[0].strip().split(' ')[-1],line.strip().split('//')[-1]])
			except Exception as e:
				errorlog = errorlog + funcName + "\t" + str(e) +"\n"
		if line.find('ReqBody') != -1:
			try:
				funcName = line.strip().split(' ')[1].split('ReqBody')[0]
				funcExp = lined.strip().split('//')[-1]
			except Exception as e:
				errorlog = errorlog + funcName + "\t" + str(e) +"\n"
			found = True
			funcPar = []
		lined = line
	for key,val in funcCase.items():
		headPar = ''
		bodyPar = ''
		bodyVar = ''
		for k,v in enumerate(val['para']):
			if v[0] == 'uint32' or v[0] == 'int32':
				localbodyVar = 'request%s.body().m_%s = %s; //%s' % (key, v[1], v[1], v[2])
				headPar = headPar + v[0] + ' ' + v[1] + ' = 0, '
				bodyPar = bodyPar + v[0] + ' ' + v[1] + ', '
			elif v[0] == 'string':
				localbodyVar = 'request%s.body().m_%s = %s; //%s' % (key, v[1], v[1], v[2])
				headPar = headPar + v[0] + ' ' + v[1] + ' = "", '
				bodyPar = bodyPar + v[0] + ' ' + v[1] + ', '
			elif v[0] == 'bool':
				print(v[0], v[1], v[2])
				localbodyVar = 'request%s.body().m_%s = %s; //%s' % (key, v[1], v[1], v[2])
				headPar = headPar + v[0] + ' ' + v[1] + ' = false, '
				bodyPar = bodyPar + v[0] + ' ' + v[1] + ', '
			else:
				localbodyVar = '//request%s.body().m_%s = %s; //%s' % (key, v[1], v[1], v[2] + " " + v[0])
			bodyVar = localbodyVar.join([bodyVar,'\n'])
		headPar = headPar[:-2]
		bodyPar = bodyPar[:-2]
		funcHead = 'int %s(%s); //%s\n' % (key, headPar, val['expain'])
		funcText = 'int GameTransfer::%s(%s)\n{\n%sRequest request%s;\n%s%sResponse* response%s = NULL;\n\nreturn send_game_message(request%s, response%s);\n}\n' % (key, bodyPar, key, key, bodyVar, key ,key, key, key)
		# print >> fp2, 'hellp'
		fp2.write(funcText)
		fp3.write(funcHead)

	fp.close()
	fp2.close()
	fp3.close()
			
if __name__=="__main__":
	for k,v in enumerate(sys.argv):
		if k != 0:
			# try:
				work_cg(v)
			# except Exception as e:
				# errorlog = errorlog + v + "\t" + str(e) +"\n"
	if errorlog != "" :
		lfname = "Error " + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) +".log"
		lfurl = os.path.join( sys.path[0] , lfname)
		lf = open(lfurl,'w');
		lf.write(errorlog);
		lf.close();