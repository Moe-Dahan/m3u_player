import PySimpleGUI as sg
from tkinter import filedialog
import vlc
import requests

sg.theme('SystemDefault')
''' play video function with small button as a added gui to stop player '''
def play_video(m3u_url):
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(m3u_url)
    player.set_media(media)
    player.play()

    layout = [
        [sg.Button("STOP", key="stop", button_color='red', size=(80, 50), font=('Arial', 10, 'bold'))]
    ]
    window = sg.Window("", layout, size=(80, 50), no_titlebar=True, grab_anywhere=True, finalize=True, keep_on_top=True)

    ''' places the stop button to the top right side of screen '''
    screen_width, screen_height = sg.Window.get_screen_size()
    window_width, window_height = 400, 100
    window_x = screen_width - window_width
    window_y = 0
    window.move(window_x, window_y)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'stop':
            player.stop()
            window.close()
            break

''' loads the channels through a m3u file '''
class ChannelLoader:
    def __init__(self):
        self.channels = {}
        
    def load_channels(self, select_file):
        encodings_to_try = ['utf-8', 'iso-8859-1', 'cp1252']  # Add more encodings as needed
        ''' checks the encoding type from encodings_to_try list '''
        for encoding in encodings_to_try:
            try:
                with open(select_file, 'r', encoding=encoding) as file:
                    lines = file.readlines()
            except FileNotFoundError: # if its not a file will load url
                    lines = select_file.splitlines()
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

''' main gui class '''
class MainGui:

    def layout():
        layout_frame = [
            [sg.Menu([['&PLAYLIST', ['&Open Playlist', '&Load from url']]])]
        ]
        return layout_frame

    def run():

        window = sg.Window("m3u player", MainGui.layout(), resizable=True, size=(400, 100))

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            
            if event == 'Open Playlist':
                window.close()
                filetypes = [("M3U files", "*.m3u"), ("All files", "*.*")]
                select_file = filedialog.askopenfilename(filetypes=filetypes)
                if select_file:
                    channel_loader = ChannelLoader()
                    channel_loader.load_channels(select_file)
                    second_gui(channel_loader.channels)

            elif event == 'Load from url':
                window.close()
                url_to_grab = sg.popup_get_text("Enter URL for Playlist")
                if url_to_grab:
                    url_content = requests.get(url_to_grab).content.decode('utf-8')
                channel_loader = ChannelLoader()
                channel_loader.load_channels(select_file=url_content)
                second_gui(channel_loader.channels)

''' once playlist is loaded and channels load play channel from this gui '''
def second_gui(channels):
    for i in range(0, len(channels)):
        max_buttons_per_row = i//2  # divide by the amount of rows we want 3 will == 3 rows 4 == 4 rows etc..
    channel_buttons = []
    current_row = []

    for name, url in channels.items():
        button = [sg.Text(name, key=name, enable_events=True, text_color='blue)]
        current_row.append(button)
        if len(current_row) == max_buttons_per_row:
            channel_buttons.append(current_row)
            current_row = []

    if current_row:
        channel_buttons.append(current_row)

    all_chan = [ # just used for scrolling making it look neater then a scroll bar on every column created
        [sg.Column(layout=row) for row in channel_buttons]
    ]

    layout = [
        [sg.Column(layout=all_chan, expand_x=True, scrollable=True, vertical_scroll_only=True)]
    ]

    window = sg.Window("Loaded Channels", layout, size=(700, 500), resizable=True)

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
