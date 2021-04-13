
import deezer as deezer
import requests, json, os, re

from deezer import request

localdir = os.getcwd()
headers = {'content-type': 'application/json',
               'Authorization': 'Token bb1131f893f91f1bf5461285b26c0b622d21a37e'}
def crawl_auto(gmail, password, arl, sv, ip, output):
    dez = deezer.Login(gmail, password, arl)
    tracks = requests.get("http://54.39.49.17:8031/api/tracks/?status=0&sv={}".format(sv)).json()['results']
    for track in tracks:
        print("Update Status audio: " + str(track['deezer_id']) + " - " + track['title'] + " - " + track['artist'])
        track['status'] = True
        try:
            requests.put("http://54.39.49.17:8031/api/tracks/{}/".format(track['id']),
                         data=json.dumps(track), headers=headers)
        except:
            requests.put("http://54.39.49.17:8031/api/tracks/{}/".format(track['id']),
                         data=json.dumps(track), headers=headers)
            pass

    for track in tracks:
        try:
            print("crawl audio: " + str(track['deezer_id']) + " - " + track['title'] + " - " + track['artist'])
            track['status'] = True
            track = dez.download(track['deezer_id'], track,ip, output)
            if (os.path.exists(track['url_128'])):
                track['error_code'] = 0
            else:
                track['error_code'] = 1
            try:
                requests.put("http://54.39.49.17:8031/api/tracks/{}/".format(track['id']),
                             data=json.dumps(track), headers=headers)
            except:
                requests.put("http://54.39.49.17:8031/api/tracks/{}/".format(track['id']),
                             data=json.dumps(track), headers=headers)
                pass
        except Exception as e:
            print("error Download:" + str(e))
            pass
def find_audio(deezer_id):
    tracks = requests.get("http://54.39.49.17:8031/api/tracks/?deezer_id={}".format(deezer_id)).json()['results']
    return tracks
def get_info(deezer_id,ip,output,quality):
    token_txt=requests.get("http://54.36.172.148/mslc/token.txt").text
    dez = deezer.Login("getmoneykhmt5@gmail.com", "asd123a@", token_txt)
    track={}
    track_j=requests.get("https://api.deezer.com/track/"+deezer_id).json()
    track['deezer_id']=track_j['id']
    track['title']=track_j['title'][:255]
    track['title_short'] = track_j['title_short'][:255]
    track['isrc'] =  track_j['isrc']
    track['duration'] = track_j['duration']
    track['rank'] = track_j['rank']
    track['explicit_lyrics'] = track_j['explicit_lyrics']
    track['status']=1
    track['artist']= track_j['artist']['name']
    track = dez.download(track['deezer_id'], track, ip, output,quality)
    track['error_code'] = 0
    track['status'] = 1
    try:
        requests.post("http://54.39.49.17:8031/api/tracks/",
                     data=json.dumps(track), headers=headers)
    except:
        requests.post("http://54.39.49.17:8031/api/tracks/",
                      data=json.dumps(track), headers=headers)
    return track

def get_audio(deezer_id,ip,output,quality,force):
    tracks = find_audio(deezer_id)
    if len(tracks) == 0:
        print(json.dumps(get_info(deezer_id, ip, output,quality)))
    else:
        track = tracks[0]
        if track['url_128'] == None or force:
            if force:
                dataD={}
                dataD['paths']=[track['url_128'],track['url_320'],track['url_flac']]
                if track['url_128']:
                    try:
                        requests.post(re.findall(r'http:\/\/[\d\.]+\/',track['url_128'])[0]+"clientMusic/delete_music.php",
                              data=json.dumps(dataD), headers=headers)
                    except:
                        pass
            token_txt = requests.get("http://54.36.172.148/mslc/token.txt").text
            dez = deezer.Login("getmoneykhmt5@gmail.com", "asd123a@", token_txt)
            track = dez.download(track['deezer_id'], track, ip, output,quality)
            track['error_code'] = 0
            track['status'] = 1
            try:
                requests.put("http://54.39.49.17:8031/api/tracks/{}/".format(track['id']),
                             data=json.dumps(track), headers=headers)
            except:
                requests.put("http://54.39.49.17:8031/api/tracks/{}/".format(track['id']),
                             data=json.dumps(track), headers=headers)
        print(json.dumps(track))




