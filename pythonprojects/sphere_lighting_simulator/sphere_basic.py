import math
import sys

WIDTH=70
INTERVALL=50
#Konstanter

class Pixel:
    '''pixelklass som håller koll på varje pixels x,y och belysningsvärde b'''
    def __init__(self, x:int, y:int, b:str):
     
     self.x=x
     self.y=y
     self.b=b

class image:
   '''klass som håller koll på bilddatan i form av en nestad lista pixlar och funktioner som modifierar dessa'''
   def __init__(self,x0:int,y0:int,r:int):
      self.listafil=[]
      self.x0=x0
      self.y0=y0
      self.r=r
      self.z0=z_funktion(self.r,self.x0,self.y0)
      self.img= [
      [Pixel(x, y, "W") for x in range(-WIDTH, WIDTH+1)] 
      for y in range(-WIDTH, WIDTH+1)
      ]
       
  

   def belysning(self):
        '''delar upp cirkeln i intervall som representeras som små kvadrater och räknar ut belysningen enbart en gång per kvadrat'''
        for y_intervall in range(0,INTERVALL):
        
         y1,y2=belysning_uppdelning(y_intervall,self.r)
         
         for row in self.img[(WIDTH+y1):(WIDTH+y2)]:
            
            for x_intervall in range(0,INTERVALL):
                  
             x1,x2=belysning_uppdelning(x_intervall,self.r)
    
             z=z_funktion(self.r,x1,y1)
             b=belysning_funktion(x1,y1,z,self.x0,self.y0,self.z0,self.r)
             
             
             for pixel in row[(WIDTH+x1):(WIDTH+x2)]:
                 if (pixel.x**2+pixel.y**2)<= self.r**2:
                     #kollar om pixeln ligger i cirkeln och om den gör det sätter den uträknade belysningen
                     pixel.b=b
    
               
     
   def skugga(self):
      '''Räknar ut en skugga genom projektion och sedan definera en elips genom dessa'''
     
      length = math.sqrt(self.x0**2 + self.y0**2 + self.z0**2)
      x1, y1, z1 = self.x0 / length, self.y0 / length, self.z0 / length
      #normaliserade vektorer av ljuset
      
      x_skugga_bort,y_skugga_bort,x_skugga_nara,y_skugga_nara=skugga_funktion(self.r,x1,y1,z1)
      #räknar ut extrempunkterna av skuggan
      
      distance3=math.sqrt(x_skugga_nara**2+y_skugga_nara**2)
      a=math.sqrt((x_skugga_bort-x_skugga_nara)**2+(y_skugga_bort-y_skugga_nara)**2)/2
      b=self.r
      theta=math.atan2(self.y0,self.x0)
      centerx,centery=(a//2+distance3),0
      #Olika konstanter för elipsen
      
      x_max,x_min,y_max,y_min=optimering_elips(a,b,centerx,theta)
      
      if x_max<-WIDTH:
          x_max=-WIDTH
      if x_max>WIDTH:
          x_max=WIDTH   
      if x_min<-WIDTH:
          x_min=-WIDTH
      if x_min>WIDTH:
          x_min=WIDTH      
      if y_max<-WIDTH:
          y_max=-WIDTH 
      if y_max>WIDTH:
          y_max=WIDTH
      if y_min<-WIDTH:
          y_min=-WIDTH   
      if y_min>WIDTH:
          y_min=WIDTH
          
      #failsafe om optimeringen ger konstiga värden eller värden out of range 
    
      for row in self.img[math.floor(y_min+WIDTH):math.ceil(y_max+WIDTH)]:
         
         for pixel in row[math.floor(x_min+WIDTH):math.ceil(x_max+WIDTH)]:
             
             if elips_funktion(pixel.x,pixel.y,a,b,centerx,centery,theta)==True:
                 if -WIDTH<=pixel.x<=WIDTH and -WIDTH<=pixel.y<=WIDTH:
                     self.img[pixel.y+WIDTH][pixel.x+WIDTH].b="Q"   
            
               

     
   def printa(self):
     '''gör alla b värden till en lista och printar och sparar på en separat lista till senare potentiell filsparning''' 
     for row in self.img:
         lista=[]
         for pixel in row:   
             b=pixel.b
             lista.append(b)
         print("".join(lista))
         lista.append("\n")
         self.listafil.append("".join(lista))
    
    
   
   def create_file(self,filnamn):
     '''skapar en fil'''
     listafil="".join(self.listafil)
     filnamn=f"{filnamn}.txt"
    
     with open(filnamn, "a") as file:
      file.write(listafil)
      file.close()
    
    

def z_funktion (r, x, y):
    '''räknar ut z koordinaten på cirkeln i punkt x,y givet r x och y'''
    if r**2 - x**2 - y**2 >= 0 :
     return math.sqrt(r**2 - x**2 - y**2)
    else: 
     return 0

 
def belysning_funktion (x, y, z,x0,y0,z0,r):
     '''räknar ut belysningen genom skalärprodukt'''
     b = ((x * x0) + (y * y0) + (z * z0))/(r**2)
     if b <= 0:
        return "M"
     if 0 < b <= 0.3:
        return "*"
     if 0.3 < b <= 0.5:
        return "+"
     if 0.5 < b <= 0.7:
        return "-"
     if 0.7 < b <= 0.9:
        return "."
     if 0.9 < b <= 1:
        return " "
     else:
        return "W"
 
def belysning_uppdelning(xy_intervall,r):
   '''Räknar ut intervallen för belysningen'''
   xy1=math.floor((((xy_intervall)*(2*r))/INTERVALL)-r)
   xy2=math.floor((((xy_intervall+1)*(2*r))/INTERVALL)-r)
   return xy1, xy2
#funktioner angående elipsen
 
def skugga_funktion(r,x1,y1,z1):
   '''räknar ut extrempunkterna av skuggans elips genom en blanding av projektion och trigonometri givet normaliserade vektorer av infallande ljuset'''
   x2,y2,z2=-x1*r,-y1*r,z1*r
   x3,y3,z3= x1*r,y1*r,-z1*r
   #gör en 90 graders lutning i xy planet och multiplicerar med skalären för att få punkterna som blir skuggans extrempunkter när de projekteras
   
   t2=(z2+r)/z1
   t3=(z3+r)/z1
   #faktor som ger hur "långt" punkterna ska projekteras
   
   x_skugga_bort= x2-x1*t2
   y_skugga_bort= y2-y1*t2
   x_skugga_nara= x3-x1*t3
   y_skugga_nara= y3-y1*t3
   #projektion

   return round(x_skugga_bort), round(y_skugga_bort),round(x_skugga_nara), round(y_skugga_nara)
   
def elips_funktion(x,y,a,b,centerx,centery,theta):
   '''kollar om punkterna xy roterat till x axeln fyller elipsens funktion med en korrekterande differans på pi då skuggans extrempunkter är 18+ grader speglat'''
   theta=-theta+math.pi
   x,y=rotation(x,y,theta)
   if a != 0:
       if (((x-centerx)**2)/(a**2))+(((y-centery)**2)/(b**2))<1:
          return True   
 
def rotation(x,y,theta):
    '''applicerar ett rotationsmatrix på en punkt'''
    x,y=math.cos(theta)*x-y*math.sin(theta),math.sin(theta)*x+math.cos(theta)*y
    return x,y

def optimering_elips(a,b,xcenter,theta):
    '''skapar en rektangel runt elipsen och roterar sedan denna och räknar ut vad högsta möjliga y värde och x värde av elipsen kan vara'''
    theta=theta+math.pi
    #korrekterande differans på pi då uträkningarna på normalvektorerna skedde 180 grader speglat
    x1,y1=rotation(xcenter-a,b,theta)
    x2,y2=rotation(xcenter-a,-b,theta)
    x3,y3=rotation(xcenter+a,b,theta)
    x4,y4=rotation(xcenter+a,-b,theta)
    
    x_max,x_min= max(x1,x2,x3,x4),min(x1,x2,x3,x4)
    y_max,y_min= max(y1,y2,y3,y4),min(y1,y2,y3,y4)
    return x_max,x_min,y_max,y_min
    
    
    
    
def meny():
  '''meny som loopar om ej avslutas'''
  print(f"Hej välkommen till programmet, här kan du simulera belysningen av en sfär. Bredden och höjden av bilden är {WIDTH*2}")
  try:
     r=int(input("vad är radiens längd? "))
     x0=int(input("vad är x koordinaten där ljuset infaller? "))
     y0=int(input("vad är y koordinaten där ljuset infaller? "))
     if r>=1 and r<WIDTH:
        if x0**2+y0**2<r**2:       
         bild=image(x0,-y0,r)
         #korrekterande faktor på -1 då koordinatsystemets y axel är speglad
         bild.skugga()
         bild.belysning()
         bild.printa()
         val=input("vill du ha den på en fil? skriv 1 ")
         
         if val == "1":
             filnamn=input("vad ska filen heta? Om givet namn redan finns kommer den skrivas längst ner i samma textfil. ")
             bild.create_file(filnamn)
             print(f"bild sparad som {filnamn}.txt ")
             
         val2=input("Vill du avsluta programmet? skriv 1 annars kommer programmet köra igen" )
         if val2 == "1":
                 sys.exit()
        else:
            print("x0 och y0 ligger ej i cirkeln vänligen pröva igen ")
     else: 
         print(f"Ej giltiga värden på radien, vänligen ange ett positivt värde mellan 1 och {WIDTH}" )
  except ValueError:
         print("felaktig input vänligen pröva igen och ange ett heltal")
      
      
      
      
while True == True:
    meny()