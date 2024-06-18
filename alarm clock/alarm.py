import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import time
import pygame

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock")
        self.root.geometry("400x400")
        
        self.alarm_time = tk.StringVar()
        
        self.label_time = tk.Label(self.root, text="", font=("Helvetica", 48))
        self.label_time.pack(pady=20)
        
        self.label_alarm = tk.Label(self.root, text="Set Alarm Time (HH:MM AM/PM):", font=("Helvetica", 14))
        self.label_alarm.pack()
        
        self.entry_alarm = tk.Entry(self.root, textvariable=self.alarm_time, font=("Helvetica", 14))
        self.entry_alarm.pack(pady=10)
        
        self.btn_set_alarm = tk.Button(self.root, text="Set Alarm", font=("Helvetica", 14), command=self.set_alarm)
        self.btn_set_alarm.pack(pady=10)
        
        self.btn_stop_alarm = tk.Button(self.root, text="Stop Alarm", font=("Helvetica", 14), command=self.stop_alarm, state=tk.DISABLED)
        self.btn_stop_alarm.pack(pady=10)
        
        self.alarm_active = False
        self.update_clock()
        
        # Initialize pygame mixer for sound
        pygame.mixer.init()

    def update_clock(self):
        """Update the digital clock display."""
        current_time = datetime.now().strftime("%I:%M:%S %p")  # Format for 12-hour clock with AM/PM
        self.label_time.config(text=current_time)
        self.label_time.after(1000, self.update_clock)
    
    def set_alarm(self):
        """Set the alarm based on user input."""
        alarm_time_str = self.alarm_time.get()
        
        try:
            alarm_time_obj = datetime.strptime(alarm_time_str, "%I:%M %p")
            current_time_obj = datetime.now()
            
            # If the alarm time is earlier than the current time, add one day to the alarm time
            if alarm_time_obj < current_time_obj:
                alarm_time_obj += timedelta(days=1)
            
            self.alarm_active = True
            self.btn_set_alarm.config(state=tk.DISABLED)
            self.btn_stop_alarm.config(state=tk.NORMAL)
            
            while True:
                current_time = datetime.now().strftime("%I:%M %p")
                if current_time == alarm_time_obj.strftime("%I:%M %p") and self.alarm_active:
                    messagebox.showinfo("Alarm", "Wake Up!")
                    self.play_alarm_sound()
                    break
                time.sleep(1)
                
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter time in HH:MM AM/PM format.")
            return
    
    def play_alarm_sound(self):
        """Play the alarm sound using pygame."""
        try:
            alarm_sound = pygame.mixer.Sound('alarm.wav')  # Replace with your alarm sound file
            alarm_sound.play()
            pygame.time.wait(2000)  # Wait for 2 seconds
            alarm_sound.stop()
        except pygame.error as e:
            print(f"Error playing alarm sound: {e}")
    
    def stop_alarm(self):
        """Stop the active alarm."""
        self.alarm_active = False
        self.btn_set_alarm.config(state=tk.NORMAL)
        self.btn_stop_alarm.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()
