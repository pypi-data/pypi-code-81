

from __future__ import unicode_literals
import youtube_dl



class YouTubeDownloader:
    
    
    @staticmethod
    def download(urls, path=None):
        urls = [urls] if isinstance(urls, str) else urls
        if not path:
            path = 'C:/tmp'

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': path + '/%(title)s.%(ext)s',
        }


        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(urls)

if __name__ == '__main__':
    dl = YouTubeDownloader()
    dl.download('https://www.youtube.com/watch?v=0AwdihHME1M', 'E:/_audio/ztmp')