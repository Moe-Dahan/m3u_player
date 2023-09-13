m3u ZIP File Contains a .exe built with cx_freeze

This Python script is a simple m3u playlist player built using the PySimpleGUI library and VLC media player. It allows you to load and play m3u playlists from local files or URLs. You can also give each playlist a name for easy identification.

Dependencies
Before running the script, make sure you have the following dependencies installed:

Python
PySimpleGUI
VLC Media Player
Requests
You can install the Python dependencies using pip:

bash
Copy code
pip install PySimpleGUI vlc requests
Usage
Run the script using Python: python m3u_player.py

The main window will appear. Here's how to use the player:

Open Playlist: Click on the "PLAYLIST" menu, and then select "Open Playlist" to browse your local system for an m3u playlist file. You'll be prompted to enter a name for the playlist.

Load from URL: From the "PLAYLIST" menu, select "Load from URL" to enter the URL of an m3u playlist hosted online. You'll also be prompted to enter a name for the playlist.

Playing a Playlist: Once you've loaded a playlist, the playlist name will appear in the main window. Click on a playlist name to load and play its channels.

Stop Playback: While a playlist is playing, you can click the "STOP" button to stop playback.

The selected playlist will be displayed in a new window. You can click on individual channel names to play them.

To close the player, simply close the main window or the playback window.

Playlist Storage
The script stores your playlists and their names in a JSON file called m3uLinks.json. This allows you to easily access your playlists in future sessions.

Customization
You can customize the appearance of the player and the playlist window by modifying the code. The script uses the PySimpleGUI library for creating the GUI, so you can change the colors, fonts, and layout to suit your preferences.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Enjoy your m3u playlist player!


![Screenshot 2023-09-07 085916](https://github.com/Moe-Dahan/m3u_player/assets/83793097/61a4e1e1-c2d7-4349-8258-1f0f415a211b)
![Screenshot 2023-09-07 085931](https://github.com/Moe-Dahan/m3u_player/assets/83793097/1af4b01e-ea6e-41c1-9af9-92985fbdc339)
![Screenshot 2023-09-07 085956](https://github.com/Moe-Dahan/m3u_player/assets/83793097/127aaa25-cf0d-4de8-ac80-3dfc64bd4360)
![Screenshot 2023-09-07 090016](https://github.com/Moe-Dahan/m3u_player/assets/83793097/f3bc8237-9ffc-4440-b356-83ead365bf92)
![Screenshot 2023-09-07 090044](https://github.com/Moe-Dahan/m3u_player/assets/83793097/f0ffd626-ceed-420e-8ed6-6530b0fc460d)
![Screenshot 2023-09-07 090213](https://github.com/Moe-Dahan/m3u_player/assets/83793097/cb1081a5-3c3a-457c-8763-fef7c7dec9ff)
![Screenshot 2023-09-07 090327](https://github.com/Moe-Dahan/m3u_player/assets/83793097/9fe98c1c-8718-41ce-a23e-9796185741f2)
