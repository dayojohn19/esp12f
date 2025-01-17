import time
try:
    import mpy.ota_git
except Exception as e:
    print("ERROR IMPORTING ota_git ",e)
    import mpy.networkconfig

# import lcd
import gc
gc.collect()
files_to_update=["main.py","configs/listnames.txt","configs/esp12settings.json",'test3.txt','test4.txt','test5.txt']
giturl= "https://github.com/dayojohn19/esp12f/"


print("get try versioning 111 for v8")
print('Added in git')


