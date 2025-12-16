# oop_practice.py - Learning OOP basics

# Define a class (blueprint for a dog)
class Dog:
    # __init__ is a special method that runs when creating a new dog
    def __init__(self, name, age):
        self.name = name  # self.name is an attribute
        self.age = age
        self.energy = 100
    
    # Methods are functions that belong to the class
    def bark(self):
        print(f"{self.name} says: Woof!")
        self.energy -= 5
    
    def sleep(self):
        print(f"{self.name} is sleeping... zzz")
        self.energy = 100
    
    def play(self):
        if self.energy > 20:
            print(f"{self.name} is playing! So fun!")
            self.energy -= 20
        else:
            print(f"{self.name} is too tired to play.")
    
    def status(self):
        print(f"{self.name} - Age: {self.age}, Energy: {self.energy}")


# Now let's CREATE objects (actual dogs) from our class
print("=== Creating Dogs ===")
dog1 = Dog("Buddy", 5)
dog2 = Dog("Max", 3)

print("\n=== Dog 1 Actions ===")
dog1.status()
dog1.bark()
dog1.play()
dog1.status()

print("\n=== Dog 2 Actions ===")
dog2.status()
dog2.bark()
dog2.bark()
dog2.bark()
dog2.status()
dog2.sleep()
dog2.status()

print("\n=== Both Dogs Together ===")
print(f"{dog1.name} and {dog2.name} are different dogs!")
print(f"{dog1.name}'s energy: {dog1.energy}")
print(f"{dog2.name}'s energy: {dog2.energy}")
