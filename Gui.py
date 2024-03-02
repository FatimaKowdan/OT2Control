import customtkinter
from customtkinter import IntVar, CHECKBUTTON
import subprocess
import os
import pickle

def run():
   """ Executes python script deckPositionsGui.py with the 
   directory path where the script is located.

   Parameters: none
   Returns: none
   """
   os.chdir
   os.chdir("/home/gabepm100/OT2Control")

   # Executes file with the user's login number (ex: CNH_002)
   execute_python_file('deckPositionsGui.py',mynumber.get()) 


def input1(sim,auto,combobox):
    """ Handles input parameters and executes the python script
   controller.py

   Parameters:
      sim (int): Integer representing simulation mode (0 or 1).
      auto (bool): Boolean indicating whether to run in automatic mode.
      combobox (object): Object representing the combobox widget from customtkinter

   Returns:
      int: -1 if there is a validation error, otherwise returns None
    """
    global mynumber # Name input from GUI (ex: CHN_002)
    update_pickle(mynumber.get(),combobox) # Updates pickle file (caching) with mynumber and combobox values
    ent=" -n " +mynumber.get() # Constructs argument string with 'mynumber'
    
    # Check to see if 'mynumber' is empty
    if len(ent)==4:
        # Displays warning message in text widget
        T.delete("1.0",customtkinter.END)
        T.insert(customtkinter.END, "Need Name Input", 'warning')
        return -1
        
    os.chdir("/home/gabepm100/OT2Control")

    # Appends either auto or sim flag
    if sim.get()==1:
        ent=ent + " --no-sim"
    if auto.get():
        ent = ent+ " -m auto"
    
    command="controller.py"
    
    # Executes python script with constructed string argument
    output=execute_python_file(command,ent)

    # Clears the text widget
    T.delete("1.0",customtkinter.END)

    # Pipelines output into the text widget
    T.insert(customtkinter.END,output) 

def execute_python_file(file_Name, argument):
   try:
      completed_process = subprocess.run(['python3', file_Name, argument], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      if completed_process.returncode == 0:
         print("Execution successful.")
         return completed_process.stdout
      else:
         print(f"Error: Failed to execute.")
         return completed_process.stderr
   except FileNotFoundError:
      print(f"Error: The file does not exist.")
      
def execute_command(command):
   # executes the given command and returns the process
   process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
   return process

def read_stdout(process):
   # reads stdout of the given process line by line and update the output
   while True:
      output = process.stdout.readline().decode('utf-8')
      if not output:
         break
      update_output(output)

def read_stderr(process):
   # reads stderr of the provided process line by line and the output
   while True:
      error = process.stderr.readline().decode('utf-8')
      if not error:
         break
      update_output(error)

def update_output(text):
   # updates the output text
   T.insert(customtkinter.END, text)
   T.see(customtkinter.END)
   
def update_pickle(val,combobox):
   global comboboxlist
   vals=list(comboboxlist)
   try:
      if isinstance(val,str) and val!='':
         filename='pickle.pk'
         if os.path.isfile(filename):

            vals.append(val)
            with open(filename, 'wb') as g:
               vals=list(dict.fromkeys(vals))
               if len(vals)>10:
                  vals=vals[1:]
               pickle.dump(vals,g)
               g.close()
      else:
         print("Sheetname is not string")
      combobox.configure(values=vals)
   except:
      print("updating pickle didnt work. Please try doing something different")
      

def read_pickle():
   try:
      with open('pickle.pk', 'rb') as fi:
         loadedval=pickle.load(fi)
         loadedval=[x for x in list(loadedval) if x]
         fi.close()
         return list(dict.fromkeys(loadedval))
   except:
      print("couldnt read pickle")
      return []

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme('dark-blue')
#Create an instance of Tkinter frame
win= customtkinter.CTk()
win.title("OT2Control")
#Set the geometry of Tkinter frame

win.geometry("750x450")
win.configure(fg_color= '#252526')
win.title("OT2Control")

# Name Label
l = customtkinter.CTkLabel(master= win, text = "What is the name?")
l.configure(font =("Inter", 16), text_color="white")
l = customtkinter.CTkLabel(master= win, text = "What is the name?")
l.configure(font =("Inter", 16), text_color="white")
l.pack()

#Create an Entry widget to accept User Input
mynumber = customtkinter.StringVar()
combobox = customtkinter.CTkComboBox(win, width = 400 , variable = mynumber,fg_color='#3e3e42')
v=read_pickle()
combobox.configure(values = v)
comboboxlist=v
combobox.pack()

#Sim checkbox

sim = IntVar()
c2 = customtkinter.CTkCheckBox(master= win, text='Sim?',variable=sim, onvalue=1, offvalue=0, fg_color= "303030", text_color= "white", border_color = "#A7A6A6")
c2.configure(border_width= 2, font= ("Inter", 12))
c2.pack(padx=20, pady= (15, 10))


#Sim checkbox
auto = IntVar()
c2 = customtkinter.CTkCheckBox(master= win, text='Auto?',variable=auto, onvalue=1, offvalue=0, text_color= "white", border_color = "#A7A6A6")
c2.configure(border_width= 2, font= ("Inter", 12))
c2.pack()
output="hello"
#Create a Button to validate Entry Widget
customtkinter.CTkButton(win, text= "Execute",width= 20,fg_color='#007acc', font= ("Inter", 12) ,command= lambda : [input1(sim,auto,combobox)]).pack(pady=(20, 13))
# Bind the <Return> event to the execute_button's command
win.bind('<Return>', lambda event: [input1(sim, auto,combobox)])

#show deck positions
customtkinter.CTkButton(win, text= "Check Deck Positions",fg_color='#007acc', font= ("Inter", 12), command=run, width=30).pack(pady= (0, 17))
# Create text widget and specify size.
T = customtkinter.CTkTextbox(win, height = 5, width = 52)
# Create label
l = customtkinter.CTkLabel(win, text = "Output", text_color= "white")
l.configure(font =("Inter", 14))
l = customtkinter.CTkLabel(win, text = "Output", text_color= "white")
l.configure(font =("Inter", 14))
l.pack()

v=customtkinter.CTkScrollbar(win,orientation='vertical') 
v.pack(side="right", fill='y')  


# Create text widget and specify size.
T = customtkinter.CTkTextbox(win, height = 50, width = 400)
T.configure(fg_color= "#3e3e42", text_color= "white")
T.focus_set()
T.pack(side='left',expand=True,fill='both')




win.mainloop()