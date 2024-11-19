import tkinter as tk
import random
import win32api
from win32api import GetSystemMetrics
root=tk.Tk()
root.withdraw()
pipe_windows_geometries=[]
pipe_windows=[]
monitor_width, monitor_height=GetSystemMetrics(0), GetSystemMetrics(1)
bird_acceleration=0
running=True

def update():
	global bird_x, bird_y, bird_acceleration, running, pipe_speed, pipe_x, pipe_windows_geometries, pipe_windows

	#collision detection
	if bird_y<0 or bird_y+bird_height>monitor_height:
		running=False
	for geometry in pipe_windows_geometries:
		if (bird_y<geometry[1] or bird_y+bird_height>geometry[7]) and (geometry[2]<bird_x+window_widths and bird_x<geometry[2]+window_widths):
			running=False
	if not running:
		return
	
	#move bird
	bird_y+=bird_acceleration
	bird_acceleration+=1
	bird_window.geometry(f'{window_widths}x{bird_height}+{bird_x}+{bird_y}')

	#prepare pipes to move
	for geometry in pipe_windows_geometries:
		geometry[2]-=pipe_speed
		geometry[6]-=pipe_speed
	pipe_x-=pipe_speed

	#move pipes
	for i, geometry in enumerate(pipe_windows_geometries):
		if i*2<len(pipe_windows) and i*2+1<len(pipe_windows):
			pipe_windows[i*2].geometry(f'{geometry[0]}x{geometry[1]}+{geometry[2]}+{geometry[3]}')
			pipe_windows[i*2+1].geometry(f'{geometry[4]}x{geometry[5]}+{geometry[6]}+{geometry[7]}')

	#destroy offscreen windows
	if pipe_windows_geometries and pipe_windows_geometries[0][2]+window_widths<0:
		pipe_windows[0].destroy()
		pipe_windows[1].destroy()
		pipe_windows_geometries.pop(0)
		pipe_windows.pop(0)
		pipe_windows.pop(0)

	#create new pipes
	while pipe_x<=monitor_width:
		random_pipe_length=random.randint(100, monitor_height-pipe_gap-100)
		geometry=[window_widths, random_pipe_length, pipe_x, 0, window_widths, monitor_height-random_pipe_length-pipe_gap, pipe_x, random_pipe_length+pipe_gap]
		pipe_windows_geometries.append(geometry)

		pipe_top=tk.Toplevel(root)
		pipe_top.title('pipe')
		pipe_top.geometry(f'{geometry[0]}x{geometry[1]}+{geometry[2]}+{geometry[3]}')
		pipe_top.configure(bg='#00ff00')

		pipe_bottom=tk.Toplevel(root)
		pipe_bottom.title('pipe')
		pipe_bottom.geometry(f'{geometry[4]}x{geometry[5]}+{geometry[6]}+{geometry[7]}')
		pipe_bottom.configure(bg='#00ff00')

		pipe_windows.append(pipe_top)
		pipe_windows.append(pipe_bottom)

		pipe_x+=pipe_distance

	#schedule next frame
	bird_window.after(16, update)

def key_press(event):
	global bird_acceleration, running
	if event.keysym=='space' and bird_acceleration>=0:
		bird_acceleration=-15
	elif event.keysym=='Escape':
		running=False
		root.destroy()

bird_y=200
bird_x=150
pipe_speed=5
window_widths=125
bird_height=125
pipe_gap=400
pipe_distance=500
pipe_x=750

bird_window=tk.Toplevel(root)
bird_window.title('bird')
bird_window.geometry(f'{window_widths}x{bird_height}+{bird_x}+{bird_y}')
bird_window.configure(bg='#ff0000')

root.bind_all('<KeyPress>', key_press)
update()
root.mainloop()