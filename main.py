import wave
import pyaudio  

class Space(object):
    def __init__(self, nw, se, filename=None):
        self.nw = nw
        self.se = se
        self.subspaces = []
        self.filename = filename

    def contains_point(self, p):
        return self.se.x >= p.x and self.nw.x <= p.x and self.se.y >= p.y and self.nw.y <= p.y

    def add_subspace(self, s):
        if self.contains_point(s.nw) and self.contains_point(s.se):
            self.subspaces.append(s)
        else:
            raise Exception("Subspace outside parent space.")

    def _play_sound(self, p):
        for s in self.subspaces:
            if s.contains_point(p):
                return s._play_sound(p)
        return play_clip(self.filename)

    def play_sound(self, p):
        if self.contains_point(p):
            self._play_sound(p)
            
    def __repr__(self):
        return "<Space at {}, {}: {}, {}>".format(self.nw.x, self.nw.y, self.se.x, self.se.y)


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


def play_clip(file_name):
    #define stream chunk   
    chunk = 1024  

    #open a wav format music  
    f = wave.open(file_name,"rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(chunk)  

    #play stream  
    while data:  
        stream.write(data)  
        data = f.readframes(chunk)  

    #stop stream  
    stream.stop_stream()  
    stream.close()  

    #close PyAudio  
    p.terminate()

nw = Point(0,0)
se = Point(10,10)
s = Space(nw, se)


s1 = Space(Point(0, 0), Point(5, 10), "./rain.wav")
s2 = Space(Point(0, 5), Point(10, 10), "./boom.wav")

s.add_subspace(s1)
s.add_subspace(s2)

me = Point(7, 7)

s.play_sound(me)

