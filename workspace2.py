from Maths import Vector
class Dog:
    def __init__(self,name):
        self.name = name
        
    def bark(self):
        print(self.name +str(len(self.name)*"woof"))

class shiba(Dog):
    def __init__(self,name):
        super().__init__(name)
        

        
jack = shiba("joek")
print((getattr(jack,"pos",None)).values())


