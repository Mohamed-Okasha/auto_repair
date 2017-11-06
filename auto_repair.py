import re
import subprocess
import pickle

handel=open('history_r.pickle','wrb+')
if handel.tell()!=0:
   history=pickle.load(handel)
else:
   history={}
handel.close()



text=open("/home/okasha/Documents/message.log") # test log message
txt=text.read()

timestamp =re.compile(r'timestamp: .*? ')

   

matchObj=re.compile(r' Table .*? is marked as crashed')



table_path= matchObj.search(txt).group(0)
objects=table_path.split('\'')
objects=objects[1].split('/') # [.,database_name,table_name]
table_name=objects[2]

time_trigger=timestamp.search(txt).group()

if table_name in history:
   if time_trigger == history[table_name]:
      exit()
else:
   history[table_name]=time_trigger
   status=subprocess.call(["mysqlcheck", "-r"] + objects[1:])
   if status.find('OK')==-1:
     print 'There is an error'
   else:
     print 'Auto repair process finished with out any error!'

      
handel=open('history_r.pickle','wb')
pickle.dump(history, handle, protocol=pickle.HIGHEST_PROTOCOL)
handel.close()


