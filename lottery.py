import pyxel
import random
import time

class LotteryApp:
    def __init__(self):
        self.names = [
            "Keever Bradley Kyo",
            "Fujii Hana",
            "Hotoda Umeno",
            "Asahina Izumi",
            "Acchedyaswastha Naradama",
            "Obrien Ross",
            "Nguyen Le Phuong Linh",
            "Shinji Miyu",
            "Nagatomi Rei",
            "Pan Ziming",
            "Putra Mukti Ali Al Mughni",
            "Yang Tiancong",
            "Yeung Hei Richard",
            "Lee Siheon",
            "Maeda Sahara",
            "Ito Haruka",
            "Kanai Yuito",
            "Kawasaki Karin",
            "Nguyen Tran Quang Minh",
            "Goto Lina",
            "Ho Quynh Trang",
            "Ho Kate",
            "Nagaki Seijiro",
            "Takamoto Kentaro",
            "Ochiai Kanon"
        ]
        
        self.state = "start"
        self.selected_name = ""
        self.animation_frame = 0
        self.animation_speed = 0
        self.current_display_name = ""
        self.lottery_duration = 0
        self.lottery_start_time = 0
        self.sound_played = False
        
        random.seed()
        
        pyxel.init(400, 300, title="Presentation Lottery")
        
        # Define sound effects
        pyxel.sounds[0].set(
            "c3e3g3c4c4", "t", "6", "n", 15
        )
        pyxel.sounds[1].set(
            "c4e4g4c4", "t", "7", "n", 10
        )
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if self.state == "start":
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.state = "lottery"
                self.lottery_start_time = time.time()
                self.lottery_duration = 3.0
                self.animation_speed = 1
                self.sound_played = False
                pyxel.play(0, 0)
        
        elif self.state == "lottery":
            self.animation_frame += 1
            
            elapsed_time = time.time() - self.lottery_start_time
            
            if elapsed_time < self.lottery_duration:
                if self.animation_frame % max(1, int(10 - elapsed_time * 3)) == 0:
                    self.current_display_name = random.choice(self.names)
            else:
                if not self.sound_played:
                    pyxel.play(0, 1)
                    self.sound_played = True
                self.selected_name = random.choice(self.names)
                self.current_display_name = self.selected_name
                self.state = "result"
    
    def draw(self):
        pyxel.cls(0)
        
        if self.state == "start":
            pyxel.text(140, 120, "Lottery starts", 7)
            pyxel.text(130, 150, "Press ENTER to start", 6)
            
        elif self.state == "lottery":
            pyxel.text(180, 100, "Drawing...", 10)
            
            if self.current_display_name:
                name_width = len(self.current_display_name) * 4
                x = (400 - name_width) // 2
                pyxel.text(x, 140, self.current_display_name, 7)
            
            for i in range(5):
                color = (self.animation_frame + i) % 16
                pyxel.rect(50 + i * 60, 200 + (self.animation_frame + i * 10) % 20, 40, 20, color)
            
        elif self.state == "result":
            pyxel.text(150, 80, "Selected Presenter:", 10)
            
            # Draw very large text (30x size) by drawing multiple times with larger offsets
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    if dx == 0 and dy == 0:
                        continue
                    name_width = len(self.selected_name) * 30
                    x = (400 - name_width) // 2
                    pyxel.text(x + dx, 120 + dy, self.selected_name, 1)
            
            # Draw additional layers for even larger appearance
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if dx == 0 and dy == 0:
                        continue
                    name_width = len(self.selected_name) * 30
                    x = (400 - name_width) // 2
                    pyxel.text(x + dx, 120 + dy, self.selected_name, 5)
            
            # Main text
            name_width = len(self.selected_name) * 30
            x = (400 - name_width) // 2
            pyxel.text(x, 120, self.selected_name, 11)
            
            pyxel.text(100, 180, "Press ENTER for next", 6)
            pyxel.text(120, 200, "Press ESC to exit", 6)
            
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.state = "lottery"
                self.lottery_start_time = time.time()
                self.lottery_duration = 3.0
                self.animation_speed = 1
                self.sound_played = False
                pyxel.play(0, 0)
            
            if pyxel.btnp(pyxel.KEY_ESCAPE):
                pyxel.quit()

if __name__ == "__main__":
    LotteryApp()