import gdata.photos.service
import datetime, time, os
import ConfigParser

import subprocess
from subprocess import call


config = ConfigParser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'login.ini'))

email    = config.get('DEFAULT','email')
password = config.get('DEFAULT','password')
username = config.get('DEFAULT','username')
album_name = config.get('DEFAULT','album_name')
loop_hrs = config.getint('DEFAULT','hrs_to_loop')
interval = config.getint('DEFAULT','interval')

# it takes 5-6 seconds to actually take a picture. Compensate for that
if (interval >6 ):
    interval -= 6


start_time = datetime.datetime.now().time().hour 
cur_time = datetime.datetime.now().time().hour


picasa = gdata.photos.service.PhotosService(email=email,password=password)
picasa.ProgrammaticLogin()
#album = picasa.InsertAlbum(title="Python Test", summary="test summary", access="private")

albums = picasa.GetUserFeed(user=username)
for album in albums.entry:
  if album.title.text==album_name:
    album_url = '/data/feed/api/user/default/albumid/%s' % (album.gphoto_id.text)
    
filename  = "/tmp/rpiTmp.jpg"

while (cur_time - start_time < loop_hrs):
    call(["raspistill -rot 180 -w 2048 -o " + filename ], shell=True)
    photo = picasa.InsertPhotoSimple(album_url,'New Photo','',filename,content_type='image/jpeg')
    cur_time = datetime.datetime.now().time().hour
    time.sleep(interval)


