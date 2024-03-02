import customtkinter
from customtkinter import IntVar, CHECKBUTTON
import subprocess
import os
import pickle

def run():
   """ 
   Executes python script deckPositionsGui.py with the 
   directory path where the script is located.

   Parameters: none
   Returns: none
   """
   os.chdir
   os.chdir("/home/gabepm100/OT2Control")

   # Executes file with the user's login number (ex: CNH_002)
   execute_python_file('deckPositionsGui.py',mynumber.get()) 


def input1(sim,auto,combobox):
    """ 
    Executes the Python script 'controller.py' with specified arguments based on user inputs.
    Updates the GUI text widget with the output of the script

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
   """ Executes a Python script with the given file using subprocess to run the file.
   Takes either a file name if it is in the same directory or a file path if it is not. Runs said file
   simultaneously to the current process. Determines if the file ran successfully or failed to execute.

   Called for both input1 and deck position.

   Parameters:
      file_Name (str): Name of the python script to execute
      argument (str): String of different arguments
   
   Returns: Standard output of the executed script if successful.
               Standard error output if the execution fails.

   
   """
   try:
      # Executes specified python script
      completed_process = subprocess.run(['python3', file_Name, argument], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      
      # Checks the return code of subprocess and returns standard output if successful or not
      if completed_process.returncode == 0:
         print("Execution successful.")
         return completed_process.stdout
      else:
         print(f"Error: Failed to execute.")
         return completed_process.stderr
   except FileNotFoundError:
      print(f"Error: The file does not exist.")
      
def execute_command(command):
   """
   Executes the given command and returns the process using subprocess.

   Parameter:
      command (str): Contains the valid shell command you want to execute.
   
   Returns:
      process (obj):The subprocess.Popen object that allows you to interact with 
                     the executed command and obtain information about its execution
   """
   process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
   return process

def read_stdout(process):
   """
   Reads stdout of the given process line by line and updates the output by calling
   the function update_output.

   Parameter:
      process (obj): a subprocess.Popen object that allows the function to 
                     read the standard output of the executed command and update the output accordingly
   
   Returns: 
      None
   """   
   while True:
      output = process.stdout.readline().decode('utf-8')
      if not output:
         break
      update_output(output)

def read_stderr(process):
   """
   Reads stderr of the provided process line by line and the output.

   Parameter:
      process (obj): a subprocess.Popen object that allows the function to 
                     read the standard output of the executed command and update the output accordingly
   
   Returns: 
      None
   """
   while True:
      error = process.stderr.readline().decode('utf-8')
      if not error:
         break
      update_output(error)

def update_output(text):
   """
   Updates the output text in the custom tkinter text widget

   Parameter: 
      text (str): The text to be inserted into the text widget
   """
   T.insert(customtkinter.END, text)
   T.see(customtkinter.END)
   
def update_pickle(val,combobox):
   """
   Updates the pickle file for caching with the provided value 

   Parameters:
      val (str): The value to be added to pickle file
      combobox (obj): Object representing the combobox widget from customtkinter
   """
   # Keep track of values displayed in combobox widget
   global comboboxlist
   vals=list(comboboxlist)
   try:

      # Check if provided value is a non-empty string
      if isinstance(val,str) and val!='':
         filename='pickle.pk'
         if os.path.isfile(filename):

            # Appends the value to the list of cached values
            vals.append(val)
            with open(filename, 'wb') as g:

               # Removes duplicates by converting to dictionary then to list
               vals=list(dict.fromkeys(vals))

               # Limits list size to 10
               if len(vals)>10:

                  # Removes first element (oldest value) from 'vals' list
                  vals=vals[1:]
               
               # Serializes 'vals' data to file object
               pickle.dump(vals,g)
               g.close()
      else:
         print("Sheetname is not string")

      # Configure the combobox widget with the updated list of values
      combobox.configure(values=vals)
   except:
      print("updating pickle didnt work. Please try doing something different")
      

def read_pickle():
   """
   Reads and returns the values stored in pickle caching file

   Returns:
      list: A list cotianing the values stored in the pickle file. 
      If reading the file fails, an empty list is returned
   """
   try:
      with open('pickle.pk', 'rb') as fi:

         # Reads data stored in pickle file and converts into a Pyton object
         loadedval=pickle.load(fi)

         # Filters out 'None' values 
         loadedval=[x for x in list(loadedval) if x]
         fi.close()

         # Removes duplicates from list 'loadedval' by converting to dictionary then back to list to preserve order of elements
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