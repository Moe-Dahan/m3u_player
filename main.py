import PySimpleGUI as sg
from tkinter import filedialog
import vlc

sg.theme('SystemDefault')

def play_video(m3u_url):
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(m3u_url)
    player.set_media(media)
    player.play()

    layout = [
        [sg.Button("STOP", key="stop", button_color='red', size=(80, 50), font=('Arial', 10, 'bold'))]
    ]

    window = sg.Window("", layout, size=(80, 50), no_titlebar=True, grab_anywhere=True, finalize=True,)

    ''' placing the stop button at the bottom of the screen '''
    screen_width, screen_height = sg.Window.get_screen_size()
    window_width, window_height = window.size
    window_x = (screen_width - window_width) // 2
    window_y = screen_height - window_height
    window.move(window_x, window_y)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'stop':
            player.stop()
            window.close()

''' Loads the channels from file '''
class ChannelLoader:
    def __init__(self):
        self.channels = {}

    def load_channels(self, select_file):
        with open(select_file, 'r') as file:
            lines = file.readlines()
            name = url = None
            for line in lines:
                line = line.strip()
                if line.startswith('#EXTINF:'):
                    name = line.split(',', 1)[1]
                elif line.startswith('http'):
                    url = line
                    if name and url:
                        self.channels[name] = url
                        name = url = None

''' this is the main GUI first screen to load file '''
class MainGui:
    def layout():
        layout_frame = [
            [sg.Menu([['&PLAYLIST', ['&Open Playlist']]])]
        ]
        return layout_frame

    def run():
        
        window = sg.Window("m3u player", MainGui.layout(), resizable=True, size=(400, 100))

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == 'Open Playlist':
                window.close()
                filetypes = [("M3U files", "*.m3u"), ("All files", "*.*")]
                select_file = filedialog.askopenfilename(filetypes=filetypes)
                if select_file:
                    channel_loader = ChannelLoader()
                    channel_loader.load_channels(select_file)
                    second_gui(channel_loader.channels)

def second_gui(channels):
    channel_frame = [

    ]
    for name, url in channels.items():
        channel_frame.append([sg.Button(f"{name}", key=name)])
    
    layout = [[sg.Text("Loaded Channels:")],
              [sg.Column(layout=channel_frame, key='channel_frame', scrollable=True, vertical_scroll_only=True )]]
    
    window = sg.Window("Loaded Channels", layout, size=(300, 800))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Close":
            break
        
        if event in channels:
            m3u_url = channels[event]
            play_video(m3u_url)

    window.close()

if __name__ == '__main__':
    MainGui.run()
