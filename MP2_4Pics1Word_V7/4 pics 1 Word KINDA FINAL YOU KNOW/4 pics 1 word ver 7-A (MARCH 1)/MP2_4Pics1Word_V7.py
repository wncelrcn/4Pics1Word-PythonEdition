from tkinter import *
import json
import random
import string
import os
import winsound #SOUND



class game(Tk):
    
    picNum = None
    ansList = []
    picfiles = []
    
    #FUNCTION FOR CHECKING IF THERE IS SAVED PROGRESS AND LOAD IT
    def progressLoad(self):
        try:
            with open("game_progress.json","r") as f:
                data = json.load(f)
                self.picNum = data["pic_num"]
                self.correct = data["ans"]
                self.coin_count = data["coins"]
        except FileNotFoundError:
            self.picNum = 0
            self.correct = ""
            self.coin_count = 100

    def __init__(self):
        #FOR SOUND EFFECTS
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.correct_sound_file = os.path.join(self.script_dir, "sounds", "correct_sound.wav")
        self.wrong_sound_file = os.path.join(self.script_dir, "sounds", "wrong_sound.wav")
        self.hint_sound_file = os.path.join(self.script_dir, "sounds", "hint_sound.wav")
        self.skip_sound_file = os.path.join(self.script_dir, "sounds", "skip_sound.wav")
        self.bg_music_file = os.path.join(self.script_dir,"sounds","bg_music.wav")
        self.end_music_file = os.path.join(self.script_dir,"sounds","ending_sound.wav")
        
        
        #winsound.PlaySound(self.bg_music_file, winsound.SND_LOOP + winsound.SND_ASYNC)
    

        #FUNCTION CALL FOR LOADING OF PROGRESS
        self.progressLoad()

        #READING PICLIST.TXT AND APPENDING TO LISTS
        if os.path.exists("game_progress.json"):
            with open("data\\picList.txt","r") as f:               
                x = f.readlines()
            for p in x:
                fn = p.strip().split(';')
                self.picfiles.append(fn[1])
                self.ansList.append(fn[1])
        else:
            with open("data\\picList.txt","r") as f:
                lines = [line.strip().split(";") for line in f.readlines()]
            names = [pic[1] for pic in lines]
            random.shuffle(names)
            with open("data\\picList.txt","w") as f:
                for i,name in enumerate(names):
                    f.write(f"{i+1};{name}\n")
                    self.picfiles.append(name)
                    self.ansList.append(name)
        #SETTING OF PICNUM SO THAT IT WILL NOT BE OVERWRITTEN
        if self.picNum is None:
            self.picNum = 0
        else:
            self.picNum = self.picNum

        #ASSIGNING THE CORRECT ANSWER IN ONE VARIABLE (EASIER TO CALL IF WE NEED TO GET THE CORRECT ANSWER IN THE SPECIFIC LEVEL)
        self.correct = self.ansList[self.picNum] 

        #WINDOW TITLE AND DIMENSIONS
        super().__init__()
        self.title("4 Pics 1 Word")
        self.iconbitmap("pictures/icon.ico")
        self.geometry("500x700")

        #CREATING MAIN FRAME
        self.bg_frame = Frame(self,name="bg_frame",bg="#152238",width=500,height=700)
        self.bg_frame.place(x=0,y=0)
        #CREATING THE STATUS BAR (FOR LEVEL DISPLAY AND COIN COUNT DISPLAY)
        self.status_bar = Frame(self.bg_frame,name="status_bar",bg="#4682B4",width=500,height=70)
        self.status_bar.place(x=0,y=0)

        #CREATING THE COIN PICTURE
        self.coin = PhotoImage(file=r"pictures\coin.png")
        self.coin_disp = Label(self.status_bar,name="coin_disp",image=self.coin,bg="#4682B4")
        self.coin_disp.pack()
        self.coin_disp.place(x=402,y=14)

        #DISPLAYING THE CURRENT LEVEL
        title_level = "Level:" + str(self.picNum+1)
        self.level_disp = Label(self.status_bar,name="level_disp",text= title_level,font="Courier 27 bold",bg="#4682B4",fg="#F0FFFF")
        self.level_disp.pack()
        self.level_disp.place(x=7,y=15)

        #DISPLAYING THE COIN COUNTER
        self.coin_counter = Label(self.status_bar,name="coin_counter",text=self.coin_count,font="Courier 17 bold",bg="#4682B4",fg="#F0FFFF")
        self.coin_counter.pack()
        self.coin_counter.place(x=448,y=23)
        
        #CREATING FRAME FOR 4 PICS
        self.pic_frame = Frame(self,name="pic_frame",width=300,height=300,bg="#152238")
        self.pic_frame.place(x=100,y=150)

        #DISPLAYING THE 4 PICS
        self.pics = PhotoImage(file=r"pictures/{}.png".format(self.picfiles[self.picNum]))
        self.lblpic = Label(self.pic_frame,image=self.pics,width=300,height=300,bg="#152238")
        self.lblpic.pack()
        self.lblpic.place(x=-4,y=0)

        #CREATING THE SKIP BUTTON
        self.image_skip_button = PhotoImage(file='pictures/skip.png')
        self.nextPic = Button(self,image=self.image_skip_button,command= self.skipLvl,borderwidth=0, bg = '#152238',relief=RAISED,activebackground="#152238")
        self.nextPic.pack(pady=20)
        self.nextPic.place(x=418,y=580)

        #CREATING THE HINT BUTTON
        self.image_hint_button = PhotoImage(file='pictures/hint.png')
        self.hint_button = Button(self,image=self.image_hint_button,command=self.hint,borderwidth=0,bg="#152238",activebackground="#152238")
        self.hint_button.pack(pady=20)
        self.hint_button.place(x=418,y=514)

        #CREATING THE KEYBOARD FRAME, AND CALLING THE CREATE KEYBOARD FUNCTION
        self.keyboard_frame = Frame(self, bg = "#3CD184", width = 300, height = 130)
        self.keyboard_frame.place(x=249,y=580, anchor = CENTER)
        self.Keyboard(self.correct)

        #CREATING THE ANSWER BOXES (ANSWER LABELS)
        self.ansLabels = []
        self.createAnsLabel()

        #CREATING THE CHECK BUTTON
        self.check_button = Button(self,text = "SUBMIT",command = self.checkAns, font = "MSSansSerif 14 bold",bg = '#3EB489', fg = 'White')
        self.check_button.pack()
        self.check_button.place(x = 205, y = 650)

    #FUNCTION USED TO CHECK IF THE USER-INPUTTED ANSWER IS CORRECT
    def checkAns(self):
        answer = "".join(i.cget("text") for i in self.ansLabels)
        if answer == self.correct.upper():
            winsound.PlaySound(self.correct_sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC) #SOUND
            self.coin_count += 10
            self.coin_counter.config(text = self.coin_count)
            self.updateLvl()
        elif not all(i.cget("text") for i in self.ansLabels): #UPDATESOUND
            pass  
        else: #SOUND
            winsound.PlaySound(self.wrong_sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
                
    #TO UPDATE THE PICTURES (IF LEVEL SKIPPED OR LEVEL PASSED)
    def updateLvl(self):
        self.picNum += 1
        if self.picNum == 50:
            self.congratsScreen()
        else:
            self.pics = PhotoImage(file=r"pictures/{}.png".format(self.picfiles[self.picNum]))
            self.lblpic.config(image = self.pics)
            self.correct = self.ansList[self.picNum]
            self.pics.config(file=r"pictures\\{}.png".format(self.picfiles[self.picNum]))
            self.level_disp.config(text = "Level:" + str(self.picNum+1))

            # SAVING THE GAME PROGRESS BEFORE MOVING ONTO THE NEXT LEVEL 
            with open("game_progress.json","w") as score_file:
                data = {"pic_num":self.picNum,"ans":self.correct,"coins":self.coin_count}
                json.dump(data,score_file)
            self.ResetKey()
            self.ResetLabels()

    #FUNCTION FOR SKIPPING LEVEL (MINUS 10 COINS EVERY SKIP)
    def skipLvl(self):
        if 0 >= self.coin_count <= 2:
            return
        
        if self.coin_count >= 10:
            self.coin_count -= 10 
            self.coin_counter.config(text=self.coin_count)
            winsound.PlaySound(self.skip_sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.updateLvl()
            

    #FUNCTION FOR REVEALING A LETTER USING HINT BUTTON
    def hint(self):
        ansLetters = list(self.correct.upper())
        
        if 0 >= self.coin_count <= 2:
            return
        
        empty_indices = [i for i, label in enumerate(self.ansLabels) if label["text"] == ""]
        if len(empty_indices) == 0:
            return  # Exit if all labels are filled up
        
        hint_index = random.choice(empty_indices)
        hint_random = self.correct[hint_index]
        self.ansLabels[hint_index].config(text=hint_random.upper(),fg = "Green")

        self.coin_count -= 2  # Decrement count only if there are empty labels
        self.coin_counter.config(text=self.coin_count)
        winsound.PlaySound(self.hint_sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
            
    #FUNCTION FOR CREATING THE KEYBOARD BUTTONS 
    def Keyboard(self, ans):
        ansLetters = list(ans.upper())
        addLetters = max(12 - len(ansLetters),0)
        extra = random.choices(string.ascii_uppercase,k=addLetters)
        allLetters = ansLetters + extra

        random.shuffle(allLetters)

        for i in range(len(allLetters)):
            letter = allLetters[i]
            self.letter_button = Button(self.keyboard_frame, text=letter, width = 4, height=2, font = 'Helvetica 12 bold',relief=RAISED,fg = 'Black', bg = '#e5e5e5')
            self.letter_button.configure(command = lambda c=letter, b = self.letter_button: (self.BlockPress(c), self.disableBtn(b)))
            self.letter_button.grid(row = i//6, column = i%6)
        return allLetters

    def disableBtn(self,b):
        b.config(state=DISABLED)

    #FUNCTION FOR CREATING THE ANSWER BOXES 
    def createAnsLabel(self):
        total_width = len(self.correct) * 55
        x = (505 - total_width) // 2

        for i in range(len(self.correct)):
            self.ansLabel = Label(self, text="", font = 'Helvetica 12 bold', bg = "#00000d",width=4,height=2,fg = 'White',relief=FLAT)
            self.ansLabel.place(x=x + i * 55, y=470)
            self.ansLabels.append(self.ansLabel)
            self.ansLabels[i].bind("<Button-1>", lambda event, index=i: self.removeAnsLabel(index))
        
        
    def removeAnsLabel(self, index):
        self.ansLabels[index].config(text="")
        for i in self.keyboard_frame.winfo_children():
            i.configure(state=NORMAL)

    #FUNCTION SO THAT THE KEY PRESSED IN THE KEYBOARD WILL APPEAR IN THE ANSWER BOXES 
    def BlockPress(self,c):
        if all(str(label.cget("text")) != "" for label in self.ansLabels):
            self.ansLabels[0].config(text=c)
            for label in self.ansLabels[1:]:
                label.config(text="")
        else:
            for label in self.ansLabels:
                if str(label.cget("text")) == "":
                    label.config(text=c)
                    break

    #FUNCTION USED TO CLEAR THE KEYS ON THE KEYBOARD & GENERATE A NEW SET OF LETTERS
    def ResetKey(self):
        ansLetters = list(self.correct.upper())
        addLetters = max(12 - len(ansLetters),0)
        extra = random.choices(string.ascii_uppercase,k=addLetters)
        allLetters = ansLetters + extra

        random.shuffle(allLetters)

        #REMOVING THE LETTERS IN THE KEYBOARD
        for label in self.keyboard_frame.winfo_children():
            label.destroy()

        random.shuffle(allLetters)

        for i in range(len(allLetters)):
            letter = allLetters[i]
            self.letter_button = Button(self.keyboard_frame, text=letter, width = 4, height=2, font = 'Helvetica 12 bold',relief=RAISED,fg = 'Black', bg = '#e5e5e5')
            self.letter_button.configure(command = lambda c=letter, b = self.letter_button: (self.BlockPress(c), self.disableBtn(b)))
            self.letter_button.grid(row = i//6, column = i%6)
        return allLetters

    #FUNCTION USED TO RESET THE ANSWER BOXES
    def ResetLabels(self):
        for label in self.ansLabels:
            label.destroy()

        self.ansLabels = []

        label_width = 55
        total_width = len(self.correct) * label_width
        x = (505 - total_width) // 2

        for i in range(len(self.correct)):
            self.ansLabel = Label(self, text="", font='Helvetica 12 bold', bg="#00000d", width=4, height=2,fg = 'White')
            self.ansLabel.place(x=x + i * 55, y=470)
            self.ansLabels.append(self.ansLabel)
            self.ansLabels[i].bind("<Button-1>", lambda event, index=i: self.removeAnsLabel(index))
    
    #FUNCTION FOR CREATING THE END SCREEN + GIGACHAD MUSIC
    def congratsScreen(self):
        winsound.PlaySound(self.end_music_file,winsound.SND_FILENAME | winsound.SND_ASYNC)    
        self.congratsFrame = Frame(self, name= "congratsFrame",bg="#152238",width=500,height=700)
        self.congratsFrame.place(x=0,y=0)

        congrats_label = Label(self.congratsFrame, name="congrats_label",text="Congratulations!",font="System 28 bold",bg="#152238",fg = 'White').place(x=250,y=90,anchor=CENTER)
        congrats_label2 = Label(self.congratsFrame, name="congrats_label2",text="You have finished 4 Pics 1 Word!",font="System 20 bold",bg="#152238",fg = 'White').place(x=250,y=160,anchor=CENTER)
        

        self.trophy = PhotoImage(file=r"pictures\\trophy.png")
        self.trophy_disp = Label(self.congratsFrame,name="trophy_disp",image=self.trophy)
        self.trophy_disp.pack()
        self.trophy_disp.place(x=100,y=240)

        level_text = f"Levels Passed: {self.picNum}"
        level_label = Label(self.congratsFrame, name="level_label",text=level_text,font="System 18 bold",bg="#152238",fg = 'White').place(x=250,y=515,anchor=CENTER)

        coins_text = f"Coins Earned: {self.coin_count}"
        coins_earned = Label(self.congratsFrame, name="coins_earned",text=coins_text,font="System 18 bold",bg="#152238",fg = 'White').place(x=250,y=550,anchor=CENTER)
        
        quit_button = Button(self.congratsFrame,name="quit_button",command=self.quit,text="QUIT",font="MSSansSerif 24 bold", bg="red",fg="white").place(x=250,y=650,anchor=CENTER)

        os.remove("game_progress.json")

#NEW CLASS FOR THE START SCREEN WINDOW
class StartScreen(Tk):
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.start_music_file = os.path.join(self.script_dir,"sounds","start_sound.wav")
        super().__init__()
        # Create the start screen
        self.title("Welcome to 4 Pics 1 Word!")
        self.iconbitmap("pictures/icon.ico")
        self.geometry("500x700")
        self.resizable(False,False)
        
        #CREATING A BG FRAME FOR START SCREEN
        self.bg_frame = Frame(self,name="bg_frame",bg="#152238",width=500,height=700)
        self.bg_frame.place(x=0,y=0)
        
        #CREATING A 4PICS 1 WORD LOGO
        self.logo = PhotoImage(file=r"pictures\\4pics.png")
        self.logo_disp = Label(self.bg_frame,name="logo_disp",image=self.logo,bg="#152238")
        self.logo_disp.pack()
        self.logo_disp.place(x=125,y=80)

        #WELCOME TEXT
        welcome = Label(self, text = "Welcome to 4 Pics 1 Word!",font = "MSSansSerif 20 bold",fg = 'White',bg="#152238")
        welcome.place(x=75,y= 350)
        
        #MADE BY TEXT
        madeBy = Label(self.bg_frame,text="Made by: Arbutante, Dampil, Desembrana, Rivano",fg="white",font = "MSSansSerif 8 bold",bg="#152238")
        madeBy.place(x=114,y=669)

        #GAME MECHANICS TEXT
        mechanics = f"""Game Mechanics:
1. Start with 100 coins - Begin with 100 coins and try to solve all puzzles without running out.
2. Solve puzzles - Guess the word linking four pictures together.
3. Hint button - Reveal one letter of the answer for 2 coins.
4. Remove letters - Click on any answer letter to remove it.
5. Pass button - Skip to the next level for 10 coins.
6. Correct answers - Earn 10 coins as a reward for each correct answer.
7. Running out of coins - Avoid running out of coins to keep using the hint and pass buttons."""

        mechanics_label = Label(self,text=mechanics,fg="white",font = "Helvetica 8",bg="#152238",justify=LEFT)
        mechanics_label.place(x=15,y=420)
        #CREATE A START/CONTINUE BUTTON
        self.image_start_button = PhotoImage(file='pictures/start.png')
        button = Button(self, image=self.image_start_button, text="Start/Continue Game", font = "Helvetica 24 bold italic",command=self.start_application,bg = '#3EB489', fg = 'White',activebackground="#152238")
        button.place(x = 50, y = 550)
    #FUNCTION THAT WILL RUN WHEN THE START BUTTON IS PRESSED
    def start_application(self):
        winsound.PlaySound(self.start_music_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
        #DESTROY THE START SCREEN
        self.destroy()
        #CREATE AN INSTANCE OF THE MAIN GAME WINDOW
        app = game()


if __name__ == "__main__":
    start_screen = StartScreen()
    start_screen.mainloop()
