from akinatorAfunctions import*
import random 
dic = loadcharacters("charactersA.txt")

def questionDecider(filename,dic): #main function for the program, handles the flow by calling functions in akinatorAfunctions.py
    questions = questionReader(filename)
    key = [1,"B"] #initializig the key to the first key
    characters = dic
    
    while True: 
        #depending on the question type, the appropriate path is executed
        if key[1] == "B":
            key,keyword,characters = pathB(key,filename,characters) 
           
        elif key[1] == "A":
            key,keyword,characters = pathA(key,filename,characters)
           
        elif key[1] == "C":
            key,keyword,characters = pathC(key,filename,characters)
            
            
        else:
            flag = False #flag variable to handle special case of 1 guessable character
            guess = [] #variable that stores names of characters program will guess from
            incorrect = 0
            for i in characters: #population guess with character names
                guess.append(i)
            if len(guess) == 0: #in case no character fit the description
                return "Im afraid you've beaten me."
            
            if len(guess) ==  1:
                flag = True
            while len(guess)>0:
                who = random.randint(0,len(guess)-1) #random geneated index to allow random guessing
                print("Were you thinking of " + guess.pop(who) + "?")
                correct = input("\nAnswer with Yes or No: ")
                
                while (correct.lower() != 'yes' and correct.lower() != "no"):
                    correct = input("\nI SAID....answer with Yes or No: ")
                
                if correct.lower() == "yes":
                    
                    print("HAHA! I knew it!")
                    break
                elif correct.lower() == "no":
                    incorrect +=1
                    print("Shoot, let me try again...")
                if incorrect == 2 or flag: #im only giving the program 2 guesses
                    print("Im afraid you've beaten me.")
                    break
            if len(guess)>0: #if there are other characters the program could have chosen from, they are shown to the user
                print("These were the other characters I was thinking about")
                return guess
            return "See you next time!"

print("Hello there, human! My name is AkinatorA, and my creator Malick Sylla has designed me to guess exactly who you are thinking of. To start, think of a public figure or fictional personality. \nThe person or character can be from anywhere (history, sports, media, a novel, television, the big screen etc). I will prompt you with questions, to which you can respond with either 'yes', 'no' or 'maybe' if you are not sure/question is too subjective. \nTo whomever is grading this, if you beat me initially but want to see me guess correctly, then think of someone really famous or just take a peak at my database of characters in characters.txt. Enjoy\n")            
print(questionDecider("questions.txt",dic))


