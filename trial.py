from tkinter import*
from random import randint

root = Tk()

c = Canvas(root)
c.pack()



global var
var = 0

AButtonOutline = c.create_oval(100,20,20,100,width=5,)

FaceTimeByte = [15,254,254,12,14,188,1,69,204,254,99]
FaceInputByte = [1,0,0,0,0,0,0,0,0,1,0,0]

print(len(FaceInputByte))
print(len(FaceTimeByte))
AButtonFiller = 0
def first():
    global AButtonFiller
    c.delete(AButtonFiller)
    AButtonFiller = c.create_oval(90,30,30,90, fill="black",)

def second():
    AButtonFiller = c.create_oval(90,30,30,90, fill="black",)


c.delete(AButtonFiller)
while var != 10:
    if FaceInputByte[var] == 1:
        if FaceTimeByte[var] < 255:
            root.after(0,first)
            root.after(FaceTimeByte[var],lambda: c.delete(AButtonFiller))
        else:
            root.after(0,second)
    else:
        root.after(0,lambda: c.delete(AButtonFiller))
        root.after(FaceTimeByte[var],lambda: c.delete(AButtonFiller))
    var = var + 1


root.mainloop()