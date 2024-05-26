import os
PACKAGES = ["pygame", "pickle", "customtkinter", 'requests']
#for package in PACKAGES:
    #os.system(f'pip install {package}')

import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import pygame
import pickle
import requests
import json
import webbrowser
from sys import exit


pygame.mixer.init()
SAVE_FILE = "soundboard_save.pkl"
CURRENT_VERSION = "1.0.0"

class update:
    def __init__(self, current_version):
        request = requests.get("https://api.github.com/repos/gaelhf/mechanik/releases/latest")
        data = request.content
        data = json.loads(data)

        self.current_version = current_version.replace(".", "")

        version = self.data["tag_name"]
        self.version_m = self.version.replace(".", "")

    def is_update_available(self):
        if int(self.version_m) > int(self.current_version):
            return True
        else:
            return False

    def get_new_version(self):
        return str(self.version)

class SoundboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"AudioBoard - {CURRENT_VERSION}")
        self.root.geometry("300x750")
        self.root.iconbitmap("assets/icon.ico")
        self.sounds = {}
        self.loop = False
        self.update_manager = update(CURRENT_VERSION)

        self.load_sounds()

        self.scrollable_frame = ctk.CTkScrollableFrame(root)
        self.scrollable_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        for sound_name in self.sounds:
            self.create_sound_button(sound_name)

        if self.update_manager.is_update_available():
            self.link_font = ctk.CTkFont(family="underline, bold", underline=True, weight="bold")
            self.new_version = ctk.CTkLabel(master=root, text=f"New Version Available ({self.update_manager.get_new_version()})", width=20, text_color="cyan", fg_color="#2E2E2E", corner_radius=15, font=self.link_font)
            self.new_version.bind("<Button-1>", lambda e:webbrowser.open_new_tab("https://github.com/GaelHF/AudioBoard/releases/latest"))
            self.new_version.pack(side="top", padx=(10, 10), pady=(10, 10))
            self.link_font.configure(family="url_font")
            
        
        self.add_sound_button = ctk.CTkButton(root, text="Add Sound", command=self.add_sound)
        self.add_sound_button.pack(pady=10)

        self.stop_sound_button = ctk.CTkButton(root, text="Stop Sound", command=self.stop_sound)
        self.stop_sound_button.pack(pady=10)

        # Ajouter un label pour le slider de volume
        self.volume_label = ctk.CTkLabel(root, text="Volume")
        self.volume_label.pack(pady=10)

        self.volume_slider = ctk.CTkSlider(root, from_=0, to=1, command=self.set_volume)
        self.volume_slider.set(0.5)  # Initial volume set to 50%
        self.volume_slider.pack(pady=10)

        self.loop_button = ctk.CTkButton(root, text="Loop Off", command=self.toggle_loop)
        self.loop_button.pack(pady=10)

        self.quit_button = ctk.CTkButton(root, text="Exit", command=self.quit_app)
        self.quit_button.pack(pady=10)
        
        self.credit_button = ctk.CTkButton(root, text="Coded By: @GaelHF")
        self.credit_button.pack(pady=10)

    def add_sound(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
        if file_path:
            file_name = os.path.basename(file_path)
            self.sounds[file_name] = file_path
            self.create_sound_button(file_name)
            self.save_sounds()

    def create_sound_button(self, sound_name):
        button = ctk.CTkButton(self.scrollable_frame, text=sound_name, command=lambda: self.play_sound(sound_name))
        button.pack(pady=5, fill=tk.X, expand=True)

    def stop_sound(self):
        pygame.mixer.music.stop()

    def play_sound(self, sound_name):
        self.stop_sound()
        pygame.mixer.music.load(self.sounds[sound_name])
        pygame.mixer.music.play(loops=-1 if self.loop else 0)

    def set_volume(self, value):
        pygame.mixer.music.set_volume(float(value))

    def toggle_loop(self):
        self.loop = not self.loop
        self.loop_button.configure(text="Loop On" if self.loop else "Loop Off")

    def save_sounds(self):
        with open(SAVE_FILE, 'wb') as f:
            pickle.dump(self.sounds, f)

    def load_sounds(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, 'rb') as f:
                self.sounds = pickle.load(f)

    def quit_app(self):
        self.save_sounds()
        self.root.quit()

if __name__ == "__main__":
    root = ctk.CTk()
    app = SoundboardApp(root)
    root.mainloop()

exit()