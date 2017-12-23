import  os
import urllib.parse #用于解码post方法中的汉字
from post import insert
class server:
    def __init__(self):
        self.method = ''
        self.url = ''
        self.entity = {}
        self.requestline = []
        self.headerline = {}
        self.request = ''
        self.File_Dir = ''
        self.state_404 = bytes('HTTP/1.x 404 Not Found\r\n\r\n','gbk')
        self.state_200 = bytes('HTTP/1.x 200 ok\r\n','gbk')
    def read(self, str):
        self.request = str
        self.requestline = []
        self.headerline = {}
        self.entity = {}
        for req in str.split('\r\n',2)[0].split(' '):
            self.requestline.append(req)
        try:
            self.method = self.requestline[0]
            self.url = self.requestline[1]
        except:
            print('解析请求行出错！')
            return
        for header in str.split('\r\n')[1:-1]:
            if len(header.split(': ', 2)) < 2:
                break
            self.headerline[header.split(': ',2)[0]] = header.split(' ',2)[1]
        if self.method == 'POST':
            for enty in str.split('\r\n\r\n')[1].split('&'):
                self.entity[enty.split('=',2)[0]] = enty.split('=',2)[1]

    def __str__(self):
        return self.request
    def url2dir(self):
        if self.url == '/':
            self.url = '/index.html'
        dir = ''
        try:
            suf = self.url.split('.')[-1]
            suf = suf.split('#')[0]
            suf = suf.split('?')[0]
            dir = self.File_Dir + self.url.split('.')[-2] + '.' + suf
        except:
            suf = None
        if not os.path.exists(dir) or suf == None:
            return None,None
        else:
            return dir,suf
    def get_state(self,suf):
        if suf == 'html' or suf == 'css':
            return self.state_200 + bytes('Content-Type: text/'+suf+'\r\n\r\n','gbk')
        if suf == 'jpg' or suf == 'png' or suf == 'bmp':
            return self.state_200 + bytes('Content-Type: image/'+suf+'\r\n\r\n','gbk')
        if suf == 'js':
            return self.state_200 + bytes('Content-Type: application/x-javascript'+'\r\n\r\n','gbk')
        if suf == 'avi':
            return self.state_200 + bytes('Content-Type: video/avi'+'\r\n\r\n','gbk')
        if suf == 'mp4':
            return self.state_200 + bytes('Content-Type: video/mpeg4' + '\r\n\r\n', 'gbk')
        if suf == 'mp3':
            return self.state_200 + bytes('Content-Type: audio/mp3'+'\r\n\r\n','gbk')
        return self.state_404
    def response(self):
        if self.method == 'GET':
            dir , suf = self.url2dir()
            content = self.get_state(suf)
        elif self.method =='POST':
            dir, suf = self.url2dir()
            comment = self.entity.get('comment',None)
            if comment != None:
                comment = urllib.parse.unquote(comment)
                insert(comment,dir,self.url)
            content = self.get_state(suf)
        else:
            content = self.state_404
        if content != self.state_404 and os.path.exists(dir):
            file = open(dir, 'rb')
            content += file.read()
            file.close()
        return content
