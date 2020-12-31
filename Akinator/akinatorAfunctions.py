"""
This file stores the main functions of the Akinator.  It is imported by the akinator in order to execute the game.
"""
def questionReader(filename): #this function loads the questions stored a given question database into a dictionary
    file = open(filename, "r") # opening the file
    line = "tango"
    questions = {} # dictionary storing key as the key, and the questions as the value
    
    while line != "":
        key = ""
        cluster = []
        while line!= "/" and line != "": #while loop that runs in between question clusters
            if line[0].isdigit(): #checking to see if the line is a key
                key = line
            else:
                cluster.append(line) #adding the questions to a list, in order to form the cluster
            line = file.readline().strip()
        if key != "":
            questions[key] = cluster # adding the cluster of questions to the key dictionary
        line = file.readline().strip()
    return questions

def keyMaker(lis):#this function receives a list representing a key, and converts its content to a string version of the key
    key = str(lis[0])
    if len(lis) ==1:
        return str(lis[0])
    return key + keyMaker(lis[1:])
            
            
def keyCheck(key, filename): #this function receives a key, as well as a filename in order to find the key's type
    questions = questionReader(filename) 
    for keyword in questions: #iterating over every key(from now on, keyword) in the question bank
        counter = 0 #counter variable storing amount of matching digits
        i = 0
        for letter in range(0,len(keyword)): #going over every character in the keyword
            if str(key[i]) == keyword[letter]: #checking to see if the key given looks like the keyword
                counter +=1
                if i == 1: #I do not want to count a match that is the type; I am trying to update the type
                    counter -=1
            if counter == len(key)-1: #when counter is the length of the key, that means the key matches every single character in the keyword minus the type
                return keyword[1] #returning the type of the matching keyword
            
            i+=1
            if i == len(key): #out of range stoppage
                break
    
   #default return is None 

def keyBuilderA(key,filename): #this function updates the key given , with the assumption that the user entered "yes"
    key[0] = key[0]+1 #incrementing the level
    key.append(1) #adding a 1 to the path to represent a "yes" answer
    typeQ = keyCheck(key,filename)
    key[1] = typeQ
    keyword = keyMaker(key)
    return key,keyword

def pathB(key,filename, charactersList): #function that handles the program flow if the key is of type B
    keyword = keyMaker(key)
    questions = questionReader(filename)
    dic = charactersList
    for i in range(len(questions[keyword])): #iterating over the cluster
        choice = input("Does this tag fit your character?: " + questions[keyword][i]+ "- ")
        
        while choice.lower() == "" or (choice.lower() != 'yes' and choice.lower() != "no" and choice.lower() != "maybe"): #ensuring appropriate input is inputted
            choice = input("I SAID...does this tag fit your character?: " + questions[keyword][i]+ "- ")
        
        dic = check(questions[keyword][i], choice, dic) #updating the character dictionary
    key,keyword = keyBuilderA(key,filename) #updating the key
    return key,keyword, dic
 
def pathA (key,filename,charactersList): #function that handles the program flow if the key is of type A
    questions = questionReader(filename)
    keyword = keyMaker(key)
    header = keyword #since the key changes after each question, a header saving the key is required
    dic = charactersList
    for i in range(len(questions[header])):
        flag = True #variable to be aware of special case when there is only 1 question
        
        if len(questions[header]) == 1:
            flag = False
        choice = input("Does this tag fit your character?:" + questions[header][i]+ "- ")
        
        while choice.lower() == "" or (choice.lower() != 'yes' and choice.lower() != "no"):
            choice = input("I SAID...does this tag fit your character?: " + questions[header][i]+ "- ")
        
        if choice.lower().strip() == "yes":
            key,keyword = keyBuilderA(key,filename) #updating key 
            dic = check(questions[header][i], choice, dic) #updating character dictionary
            break
        
        elif choice.lower().strip() == "no":
            if flag == False: #updating key in special case
                dic = check(questions[header][i], choice, dic)
                key[0] = key[0] + 1
                key.append(0)
                key[1] = keyCheck(key,filename)
                keyword = keyMaker(key)
                
            else:
                dic = check(questions[header][i], choice, dic) #updating character dictionary
                #code below updates key with a 0 instead of a 1, and does not move levels
                key.append(0)
                key[1] = keyCheck(key,filename)
                keyword = keyMaker(key)
    return key,keyword,dic
    
def keyBuilderC(key,filename): #function to update the key in a type C cluster
    key[0] = key[0] + 1
    key[1] = keyCheck(key,filename)
    keyword = keyMaker(key)
    return key,keyword
    
def pathC(key,filename,charactersList): #function that handles the program flow if the key is of type A
    keyword = keyMaker(key)
    questions = questionReader(filename)
    dic = {}
    
    for i in range(len(questions[keyword])): 
        choice = input("Does this tag fit your character?: " + questions[keyword][i] + "- ")
        
        while choice.lower() == "" or (choice.lower() != 'yes' and choice.lower() != "no"):
            choice = input("I SAID...does this tag fit your character?: " + questions[keyword][i]+ "- ")
        
        if choice.lower().strip() == "yes":
            dic = check(questions[keyword][i], choice, charactersList) #updating the dictionary 
            key,keyword = keyBuilderC(key,filename) #updating the key and moving to the next cluster below
            return key,keyword,dic
        
        elif choice.lower().strip() == "no":
            dic = check(questions[keyword][i], choice, charactersList) #updating the dictionary
     
    key,keyword = keyBuilderC(key,filename) #if yes was never entered and the function has reached the end of the questions, key is updated accordingly
    return key,keyword,dic
        
def charcounter(filename): #function that counts the amount of characters in the database
    counter = 0
    file = open(filename, "r")
    for i in file:
        if i.strip() == "/": 
            counter +=1
    return counter
    
def loadcharacters(filename): #function that loads all the characters from a database into a dictionary
    people = open(filename, "r")
    line = "b"
    counter = charcounter(filename)
    person = {} #person dictionary will store the name of a character as the key, and the dictionary of tags as the value
    
    for i in range(counter): 
        characters = {} #creating a new dictionary to save a character's tag
        line = people.readline().strip()
        name = line
        
        while line != "/":
            line = people.readline().strip()
            
            if line == '/':
                break
            
            characters[line] = True #adding a tag 
            
        person[name] = characters #adding a character
    
    people.close()
    return person

    
def check(ques, choice, characters): #function that updates the dictionary according to the response to an asked question
   if choice.lower().strip() == "yes":
        for p in list(characters):  #converting the character dictionary as a list to iterate over it
            if ques not in characters[p]: #if the question is not present in a character's tags, delete that character
                del characters[p]
        return characters
   
   elif choice.lower().strip() == "no":
        for p in list(characters):
            if ques in characters[p]: #if the question is present in a character's tags, delete that character
                del characters[p]
   return characters
