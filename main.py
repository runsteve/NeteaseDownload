import eyed3
import json
import requests
import re
 
 
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title
#登录 可以不登录
#login_get=requests.get("http://localhost:3000/login?email=&password=")

login_get_json=json.loads(login_get.text)
if login_get_json['code']== 200:
    print("登录成功")
else :
    print("登录失败")

#歌单id直接填
playlist_id=

playlist_detail_get=requests.get("http://localhost:3000/playlist/detail?id="+str(playlist_id))
playlist_detail_json=json.loads(playlist_detail_get.text)
 
track_count=playlist_detail_json['playlist']['trackCount']
sum=1

while sum <= track_count:
    song_id=playlist_detail_json['playlist']['trackIds'][sum-1]['id']
    song_detail_get=requests.get("http://localhost:3000/song/detail?ids="+str(song_id))
    song_detail_json=json.loads(song_detail_get.text)
    name=song_detail_json['songs'][0]['name']
    al_name=song_detail_json['songs'][0]['al']['name']
    al_pic_url=song_detail_json['songs'][0]['al']['picUrl']
    al_pic_get=requests.get(al_pic_url)
    al_pic=al_pic_get.content
    author=song_detail_json["songs"][0]["ar"][0]["name"]

    song_url_get=requests.get("http://localhost:3000/song/url?id="+str(song_id))
    song_url_json=json.loads(song_url_get.text)
    song_url=song_url_json['data'][0]['url']

    song_lyric_get=requests.get("http://localhost:3000/lyric?id="+str(song_id))
    song_lyric_json=json.loads(song_lyric_get.text)
    filename=name+'-'+ author
    filename=validateTitle(filename)

    file=open(filename+'.mp3','wb')
    song_file=requests.get(song_url)
    file.write(song_file.content)
    file.close()
    audio=eyed3.load(filename+'.mp3')
    
    audio.initTag()
    audio.tag.artist=author
    audio.tag.title=name
    audio.tag.album=al_name
    audio.tag.images.set(3,al_pic,'image/jpeg')
    if 'lrc' in song_lyric_json:
        if 'lyric' in song_lyric_json['lrc']:
            print("有歌词")
            lyric=song_lyric_json['lrc']['lyric']
            audio.tag.lyrics.set(lyric)
    
    audio.tag.save()

    sum += 1  

logout=requests.get('http://localhost:3000/logout')