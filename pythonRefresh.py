'''
print("\n=========== Variables and Printing  =================\n")

# Variables and Printing
age = 62
name = "Patty"

print(age)
print(name)

print("My name is {} and I'm {} years old".format(name, age))

# Exercise: assign the above string to a variable named "sentence"
sentence = "My name is {} and I'm {} years old".format(name, age)
print("Exercise results: {}".format(sentence))

print("\n=========== if/else and bools  =================\n")

# If/else statements
# Note the indentation signifies the statements for the if/else - wierd
if age > 18:
    print("You are older than 18")
    print("Your age is {}".format(age))
else:
    print("You are younger than 18")

todayIsCold = False
if todayIsCold:
    print("Today is cold!")
else:
    print("Today is hot!")

# Exercise: Check is a year is between 2000 and 2100, print a message
# accordingly.

year = 2017
if year > 2000 and year < 2100:
    print("Welcome to the 21st century!")
else:
    print("You are before or after the 21st century")

print("\n========== Functions ==============\n")


def hello():
    print("Hello world!")


hello()

# Function here has parameters with default values and a return.
# For some reason, 2 blank lines are needed here....


def helloWithParams(name="James", age=25):
    return "My name is {} and I am {} years old".format(name, age)


sentence = helloWithParams("Patty", 62)
print(sentence)
sentence = helloWithParams()
print(sentence)

# Exercise: Create a function that takes a string and prints it 3 times
# (no spaces)


def trippleprint(inputString):
    print("{}{}{}".format(inputString, inputString, inputString))


print("Exercise results: ")
trippleprint("hello")

print("\n========== Lists ==============\n")

dogNames = ["Fido", "Sean", "Sally",  "Mark"]
print(dogNames)

dogNames.insert(0, "Buddy")
print(dogNames)

del(dogNames[2])
print(dogNames)

print(len(dogNames))

dogNames[2] = "Jane"
print(dogNames)

# Exercise: Create the following shoes Lists
shoes = ["Spizikes", "Air Force 1", "Curry 2", "Melo 5"]
print("Exercise results: ")
print(shoes)

print("\n========== Loops ==============\n")

print("Dog names are ")
for dog in dogNames:
    print("{}".format(dog))

for x in range(5, 10):
    print(x)

print("While loop")
age = 10
while age < 16:
    print(age)
    age += 1

# Exercise: From the given array, print every number greater than 90
numbers = [76, 83, 16, 69, 52, 78, 10, 77, 45, 52, 32, 17, 58, 54, 79, 72, 55, 50, 81, 74, 45, 33, 38, 10, 40, 44, 70, 81, 79, 28, 83, 41, 14, 16, 27, 38, 20, 84, 24, 50, 59, 71, 1, 13, 56, 91, 29, 54, 65, 23, 60, 57, 13, 39, 58, 94, 94, 42, 46, 58, 59, 29, 69, 60, 83, 9, 83, 5, 64, 70, 55, 89, 67, 89, 70, 8, 90, 17, 48, 17, 94, 18, 98, 72, 96, 26, 13, 7, 58, 67, 38, 48, 43, 98, 65, 8, 74, 44, 92]
print("Exercise results: ")
for number in numbers:
    if number > 90:
        print(number)

print("\n========== Dictionaries ==============\n")

dogs = {"Fido": 7, "Sally": 3, "Buddy": 10}
print(dogs)

sentence = "Sally's age is {}".format(dogs["Sally"])
print(sentence)

del(dogs["Fido"])
print(dogs)

dogs["Edith"] = 8
print(dogs)

# Exercise, create a dictionary with the given keys and values
words = ["PoGo", "Spange", "Lie-Fi"]
definitions = ["Slang for Pokemon Go", "To collect spare change, either from couches, passerbys on the street or any numerous other ways and means", "When your phone or tablet indicates that you are connected to a wireless network, however you are still unable to load webpages or use any internet services with your device"]


cooldictionary = {}
for index in range(len(words)):
    key = words[index]
    cooldictionary[key] = definitions[index]


print(cooldictionary)

print("\n========== Classes ==============\n")


class Dog:
    # Class instance variables - see access below
    dogInfo = "Dogs are cool."

    # Using init to setup the instance variables - if you provide default
    # values, you can then instantiate the class as new Dog().  Note
    # there are NO spaces when using default values.
    def __init__(self, name="", age=0, furColor=""):
        self.name = name
        self.age = age
        self.furColor = furColor

    # Some oddity here about class methods - you need to explicity supply self
    # as the first parameter.
    def bark(self):
        print("BARK!")


newDog = Dog("Buddy", 10, "gray")
newDog.bark()

print("My dog {} is {} years old. and has {} fur.".format(newDog.name, newDog.age, newDog.furColor))

# Instance variables added on the fly
newDog.anotherName = "Fido"
newDog.anotherAge = 6

print("My dog {} is {} years old.".format(newDog.anotherName, newDog.anotherAge))
print(Dog.dogInfo)

# Exercise: Add a method to the class that returns how old the car is


class Car:
    def __init__(self, year, make, model):
        self.year = year
        self.make = make
        self.model = model

    def age(self):
        return 2017 - self.year


car = Car(2015, "VW", "Jetta")
print("The car is {} years old".format(car.age()))

'''

# From the pig latin translator tutorial - my test for creating a
# pig latin version of the given string - more accurate according to
# wikipedia.


def pigLatinTest(originalText):
        translation = ""

        for word in originalText.split():
            if word[0] in ['a', 'e', 'i', 'o', 'u']:
                # The first letter is a vowel
                translation += word
                translation += "yay "
            else:
                # Handle consonants - here you're supposed to place all letters
                # before the initial vowel to the end of the word sequence
                # followed by 'ay' - Nick uses the first letter only.
                lastBit = word[0]
                newWord = word[1:]

                newWordIndex = 0
                while newWordIndex < len(newWord):

                    if newWord[newWordIndex] in ['a', 'e', 'i', 'o', 'u']:
                        # Take the rest of the word beginning at index and add it
                        translation += newWord[newWordIndex:]

                        # Add on the constonants string
                        translation += lastBit

                        # Add on "ay"
                        translation += "ay "
                        break
                    else:
                        lastBit += newWord[newWordIndex]
                        newWordIndex += 1

        return translation


translation = pigLatinTest("one two three")
print("Result: {}".format(translation))
