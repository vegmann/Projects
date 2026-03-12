import math
import tkinter as tk
from tkinter import filedialog
import numpy as np
from PIL import Image, ImageTk

WIDTH=700
INTERVALL=100
NORMAL=WIDTH//2
r=150
#konstanter

class image:
   '''Klass som håller koll på bilddatan i form av en array med RGB data med centrum i x=normal, y=normal och funktioner som modifierar dessa'''
   def __init__(self,x0:float,y0:float,r:int):
      self.listafil=[]
      self.x0=x0
      self.y0=y0
      self.r=r
      self.z0=funktion_z(self.r,self.x0,self.y0)
      self.img=self.initialize_img()
       
   def initialize_img(self):
         '''skapar en grundarray'''
         null_bild=np.zeros((WIDTH, WIDTH, 3), dtype=np.uint8)
         null_bild[0:WIDTH,0:WIDTH]=[145, 113, 145]
         return null_bild

   def belysning(self):
        '''delar upp cirkeln i intervall som representeras som små kvadrater och räknar ut belysningen enbart en gång per kvadrat'''
        for y_intervall in range(0,INTERVALL+1):
         y_counter=0
         y1,y2=belysning_uppdelning(y_intervall,self.r)
        
         for row in self.img[(y1):(y2)]:
            #räknare för att hålla koll på var i bilden vi befinner oss
            y_counter=y_counter+1
            for x_intervall in range(0,INTERVALL+1):
         
             x_counter=0
             x1,x2=belysning_uppdelning(x_intervall,self.r)
             z=funktion_z(self.r,(x1-NORMAL),(y1-NORMAL))
             b=funktion_belysning((x1-NORMAL),(y1-NORMAL),z,self.x0,self.y0,self.z0,self.r)
             
             for element in row[(x1):(x2)]:
                 if ((x1+x_counter-NORMAL)**2+(y1+y_counter-NORMAL)**2)<= self.r**2 :
                     self.img[ y1+y_counter, x1+x_counter]=[round(254*b),round(216*b),round(120-((1-b)*60))]
                 #Kollar om pixeln är i cirkeln för varje individuell pixel och sätter ljuset relativt till b
                 
                 x_counter=x_counter+1
                
         
        
   def skugga(self):
      '''Räknar ut en skugga genom projektion och sedan defineras en elips genom dessa'''
     
      length = math.sqrt(self.x0**2 + self.y0**2 + self.z0**2)
      x1, y1, z1 = self.x0 / length, self.y0 / length, self.z0 / length
      #normaliserade vektorer av ljuset
      
      x_skugga_bort,y_skugga_bort,x_skugga_nara,y_skugga_nara=funktion_skugga(self.r,x1,y1,z1)
      #räknar ut extrempunkterna av skuggan
      
      distance_nara=math.sqrt(x_skugga_nara**2+y_skugga_nara**2)
      a=math.sqrt((x_skugga_bort-x_skugga_nara)**2+(y_skugga_bort-y_skugga_nara)**2)/2
      b=self.r
      theta=math.atan2(self.y0,self.x0)
      x_center,y_center=(a//2+distance_nara),0
      #konstanter för elipsen
      
      x_max,x_min,y_max,y_min=optimering_elips(a,b,x_center,theta)
      #räknar ut alla möjliga x och y värden av elipsen
    
      if x_max<-NORMAL:
          x_max=-NORMAL
      if x_max>NORMAL:
          x_max=NORMAL   
      if x_min<-NORMAL:
          x_min=-NORMAL
      if x_min>NORMAL:
          x_min=NORMAL      
      if y_max<-NORMAL:
          y_max=-NORMAL 
      if y_max>NORMAL:
          y_max=NORMAL
      if y_min<-NORMAL:
          y_min=-NORMAL   
      if y_min>NORMAL:
          y_min=NORMAL
          
      #failsafe för konstiga värden och värden utanför bilden för att undervika index error
        
      y_counter=math.floor(y_min+NORMAL)
      #Skapar räknare för att hålla koll på var i bilden den är och går igenom varje pixel elipsen kan vara i
      
      for row in self.img[math.floor(y_min+NORMAL):math.ceil(y_max+NORMAL)]:
         x_counter=math.floor(x_min+NORMAL)
         
         for element in row[math.floor(x_min+NORMAL):math.ceil(x_max+NORMAL)]:
              
             if funktion_elips(x_counter-NORMAL,y_counter-NORMAL,a,b,x_center,y_center,theta)==True:
                 
                 if y_counter<=WIDTH and x_counter<=WIDTH:
                     self.img[y_counter,x_counter]=[29, 29, 66]   
                     
             x_counter=x_counter+1
         y_counter=y_counter+1
      
                    
   def wipe(self):   
     '''nollställer bilden'''
     self.img[0:WIDTH,0:WIDTH]=[145, 113, 145]
   


def funktion_z (r, x, y):
    '''Räknar ut z koordinaten i en punkt givet x och y'''
    if r**2 - x**2 - y**2 >= 0 :
       return math.sqrt(r**2 - x**2 - y**2)
    else: 
        return 0
    
def belysning_uppdelning(xy_intervall,r):
   '''Räknar ut intervallen för belysningen'''
   xy1=math.floor((((xy_intervall)*(2*r))/INTERVALL)-r+NORMAL)
   xy2=math.floor((((xy_intervall+1)*(2*r))/INTERVALL)-r+NORMAL)
   return xy1, xy2

  
def funktion_belysning(x, y, z,x0,y0,z0,r):
     '''Räknar ut belysningen på sfären genom skalärprodukt och ger ett värde mellan 0 och 1 som anger ljusstyrka i punkten'''
     b = ((x * x0) + (y * y0) + (z * z0))/(r**2)
     if b<0:
         return 0
     if b>1:
         return 1
     else:
         return b
     
    
def rotation(x,y,theta):
    '''applicerar en rotationsmatris'''
    x,y=math.cos(theta)*x-y*math.sin(theta),math.sin(theta)*x+math.cos(theta)*y
    return x,y


def optimering_elips(a,b,xcenter,theta):
     '''skapar en rektangel runt elipsen och roterar sedan denna och räknar ut vad högsta möjliga y värde oh x värde av elipsen kan vara'''
    
     theta=theta+math.pi
     #korrekterande differans på pi då extrempunkterna är 180 grader speglade
     x1,y1=rotation(xcenter-a,b,theta)
     x2,y2=rotation(xcenter-a,-b,theta)
     x3,y3=rotation(xcenter+a,b,theta)
     x4,y4=rotation(xcenter+a,-b,theta)
    
     x_max,x_min= max(x1,x2,x3,x4),min(x1,x2,x3,x4)
     y_max,y_min= max(y1,y2,y3,y4),min(y1,y2,y3,y4)
      
     return x_max,x_min,y_max,y_min
    
 
def funktion_elips(x,y,a,b,x_center,y_center,theta):
     '''kollar om punkten x,y roterat med theta fyller elipsens funktion centrerat kring x axeln'''
     theta=-theta+math.pi
     #korrekterande differans på pi då extrempunkterna är 180 grader speglade
     x,y=rotation(x,y,theta)
     if a != 0:
       if (((x-x_center)**2)/(a**2))+(((y-y_center)**2)/(b**2))<1:
          return True   
    

def funktion_skugga(r,x1,y1,z1):
     '''räknar ut extrempunkterna av skuggans elips genom en blanding av projektion och trigonometri givet normaliserade vektorer av infallande ljuset och r'''
     x2,y2,z2=-x1*r,-y1*r,z1*r
     x3,y3,z3= x1*r,y1*r,-z1*r
     #gör en 90 graders lutning i xy planet och multiplicerar med skalären r för att få punkterna som blir skuggans extrempunkter när de projekteras
    
     t2=(z2+r)/z1
     t3=(z3+r)/z1
     #faktor som ger hur "långt" punkterna ska projekteras
   
     x_skugga_bort= x2-x1*t2
     y_skugga_bort= y2-y1*t2
     x_skugga_nara= x3-x1*t3
     y_skugga_nara= y3-y1*t3
     #projektion
   

     return round(x_skugga_bort), round(y_skugga_bort),round(x_skugga_nara), round(y_skugga_nara)



#allt under denna rad är funktioner angående fönster
    

class Interface_manager:
 '''klass som håller i alla grafisk interface grejer och skapar en instance av image som blir bilddatan'''
 def __init__(self):
     self.bilddata=self.initialize()
     
     
 def initialize(self):
     '''initializerar bilddatan'''
     bild=image(0,0,r)
     bild.belysning()
     return bild

  
 def spara_fil(self):
     '''sparar nuvarande bilddata'''
     filhanterare=filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG files", "*.png")])
     if filhanterare:
         bild_fil=self.bilddata.img
         bild_fil=Image.fromarray(bild_fil)
         bild_fil.save(filhanterare)
        

 def on_click(self,event,canvas,bild_pa_canvas):
     '''Tar koordinaterna för ditt klick och ändrar x0 oxh y0 till dessa och gör skugga och belysning enligt dessa koordinater'''
     x, y = event.x-NORMAL, event.y-NORMAL

     if x**2+y**2<r**2:
         self.bilddata.x0 = x
         self.bilddata.y0 = y
         self.bilddata.z0 =funktion_z(r,x,y)
         self.bilddata.wipe()
         self.bilddata.skugga()
         self.bilddata.belysning()
    
   
         updaterad_bild = Image.fromarray(self.bilddata.img)
         updaterad_bild_tk = ImageTk.PhotoImage(updaterad_bild)

         # Updaterar bilden 
         canvas.itemconfig(bild_pa_canvas, image=updaterad_bild_tk)
         canvas.image = updaterad_bild_tk 
     else:
         pass


 def main(self):
     '''mainloopen, håller i alla knappar och klick event'''
     root = tk.Tk()
     root.title("sfär")
     root.config(bg="#918CB4")
 
     image_array = self.bilddata.img  

     # konverterar arrayen till tkinter format
     initial_bild = Image.fromarray(image_array)
     initial_bild_tk = ImageTk.PhotoImage(initial_bild)

     #skapar text för bilden
     label = tk.Label(root, text="Klicka varsomhelst på sfären för att ändra belysning",bg="#918CB4", font=("Comic sans", 18))
     label.pack() 

     # skapar canvas för bilden
     canvas = tk.Canvas(root, width=initial_bild.width-5, height=initial_bild.height-5)
     canvas.pack()
     
     #skapar en spara knapp
     spara_knapp =tk.Button(root,text="Spara bild",bg="purple", font=("Comic sans",30),command=lambda: self.spara_fil()) 
     spara_knapp.pack(side="bottom")
     
      #visar första bilden
     bild_pa_canvas = canvas.create_image(0, 0, anchor=tk.NW, image=initial_bild_tk)
  
     # binder musklick till click event
  
     canvas.bind("<Button-1>", lambda event: self.on_click(event,canvas,bild_pa_canvas))
     # Kör tk inter main loop
     root.mainloop()
 
 
if __name__ == "__main__":
  interface=Interface_manager()
  interface.main()

