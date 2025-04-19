class Parent:

    def __init__(self, txt):
        self.message = txt
        self.age = len(txt)
  


class Child(Parent):
    def __init__(self, txt):
        super().__init__(txt)
        self.message = txt + str(self.age)
    

x = Child("Hello, and welcome!")

print(x.message)