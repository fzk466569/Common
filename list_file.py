import os,sys
if sys.getdefaultencoding() != 'gbk':
	reload(sys)
	sys.setdefaultencoding('gbk')
dir=r'I:\UltraEdit'
files = os.listdir(dir)
l=[]
fileslist=[]
word_list=['word1','word2','word3']
for root, dirs, files in os.walk(dir):
	for name in files:
		l.append(os.path.join(root, name))
print l
for i in l:
	# if os.path.splitext(i)[1]=='.asp':
		fileslist.append(i)
		buf=open(i).read()
		if 'key' in buf:
			print i