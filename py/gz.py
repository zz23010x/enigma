import os, sys
import gzip

for k,v in enumerate(sys.argv):
	if k != 0:
		try:
			f_in = open(v, 'rb')
			f_out = gzip.open('%s.gz' % (os.path.splitext(v)[0]), 'wb')
			f_out.writelines(f_in)
		except Exception as e:
			print(v, e)
			input()
		finally:
			f_out.close()
			f_in.close()