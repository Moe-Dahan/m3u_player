import PySimpleGUI as sg
from tkinter import filedialog
import vlc
import requests
import os
import json


sg.theme("SystemDefaultForReal")

playlist_data = {}
playlist_path = 'm3uLinks.json'
        
screen_width, screen_height = sg.Window.get_screen_size()
window_width, window_height = 400, 100

def read_existing_playlist(playlist_path):
    if os.path.exists(playlist_path):
        with open(playlist_path, 'r') as file:
            existing_data = json.load(file)
        return existing_data
    return {}

def open_playlist(select_file, playlistName):
    if select_file and playlistName:
        existing_playlist = read_existing_playlist(playlist_path)
        existing_playlist[playlistName] = select_file
        
        with open(playlist_path, 'w') as file:
            json.dump(existing_playlist, file)

        names_links = [sg.Text(playlistName, key=playlistName, enable_events=True)]
        MainGui.current_row.append(names_links)
        
        channel_loader = ChannelLoader()
        channel_loader.load_channels(select_file)
        second_gui(channel_loader.channels, player=play_video)

def play_video(m3u_url, window):
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(m3u_url)
    player.set_media(media)
    player.set_hwnd(window['-VIDEO-'].Widget.winfo_id())
    player.play()

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'stop':
            player.stop()
            player.release()
            break

class ChannelLoader:
    def __init__(self):
        self.channels = {}

    def load_channels(self, select_file):
        encodings_to_try = ['utf-8', 'iso-8859-1', 'cp1252']
        for encoding in encodings_to_try:
            try:
                with open(select_file, 'r', encoding=encoding) as file:
                    lines = file.readlines()

            except FileNotFoundError:
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

class MainGui:
    current_row = []
    if os.path.isfile(playlist_path):
        with open(playlist_path, 'r') as file:
            playlist = json.load(file)
        playlist_names = playlist.keys()
        for names in playlist_names:
            names_links = [sg.Text(names, key=names, enable_events=True)]
            current_row.append(names_links)

    elif FileNotFoundError:
        pass
        
    def layout():
        layout_frame = [
            [sg.Menu([['&PLAYLIST', ['&Open Playlist', '&Load from url']]])],
            [sg.Frame("", layout=MainGui.current_row, key='playlist_loaded_names')]
        ]
        return layout_frame
    
    def run():
        window = sg.Window("m3u player", MainGui.layout(), resizable=True, size=(400, 400), icon='videofolder_99361.ico')

        while True:
            event, values = window.read(timeout=100)
            if event == sg.WIN_CLOSED:
                break

            if event in MainGui.playlist_names:
                select_file = MainGui.playlist.get(event)
                open_playlist(select_file=select_file, playlistName=event)
            
            if event == 'Open Playlist':
                select_file = filedialog.askopenfilename(filetypes=[("M3U files", "*.m3u"), ("All files", "*.*")], icon='videofolder_99361.ico')
                playlistName = sg.popup_get_text('Enter your name:', icon='videofolder_99361.ico')
                open_playlist(select_file, playlistName)
                    
            elif event == 'Load from url':
                url_to_grab = sg.popup_get_text("Enter URL for Playlist", icon='videofolder_99361.ico')
                playlistName = sg.popup_get_text('Enter your name:', icon='videofolder_99361.ico')
                if url_to_grab:
                    url_content = requests.get(url_to_grab).content.decode('utf-8')
                open_playlist(select_file=url_content, playlistName=playlistName)

def second_gui(channels, player):
    for i in range(0, len(channels)):
        max_buttons_per_row = i//1
    channel_buttons = []
    current_row = []

    for name, url in channels.items():
        button = [sg.Text(name, key=name, enable_events=True, text_color='blue')]
        current_row.append(button)
        if len(current_row) == max_buttons_per_row:
            channel_buttons.append(current_row)
            current_row = []

    if current_row:
        channel_buttons.append(current_row)

    all_chan = [ 
        [sg.Column(layout=row) for row in channel_buttons]
    ]

    layout = [
        [sg.Column(layout=all_chan, expand_x=True, scrollable=True, vertical_scroll_only=True, sbar_relief='raised')]
    ]
    
    video_frame = [
        [sg.Button("STOP", key="stop", button_color=('white', 'red'), font=("Arial", 9, 'bold'))],
        [sg.Column(layout=[[]], key='-VIDEO-', size=(screen_width, screen_height), expand_x=True, expand_y=True)],
    ]

    lay_frame = [
        [sg.Frame("", layout=layout, key='all', expand_x=False, expand_y=True, size=(300, 30), visible=True), 
         sg.Column(layout=video_frame, expand_x=True, expand_y=True)]
    ]

    window = sg.Window("Loaded Channels", lay_frame, size=(screen_width, screen_height), resizable=True, icon='videofolder_99361.ico', finalize=True)

    while True:
        event, values = window.read(timeout=100)
        if event == sg.WINDOW_CLOSED or event == "Close":
            break
        if event in channels:
            m3u_url = channels[event]
            play_video(m3u_url, window=window)

    window.close()

if __name__ == '__main__':
    MainGui.run()
