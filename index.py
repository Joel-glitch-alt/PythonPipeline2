def greet(name):
    return f"Hello, {name}! Welcome."

def farewell(name):
    return f"Goodbye, {name}! Have a great day."

def ask_how_are_you():
    response = input("How are you today? (good/bad) ").strip().lower()
    if response == "good":
        return "That's awesome to hear! Keep it up!"
    elif response == "bad":
        return "I'm sorry to hear that. Hope things get better soon."
    else:
        return "Thanks for sharing!"

if __name__ == "__main__":
    name = "Joel"
    print(greet(name))
    
    print(ask_how_are_you())
    
    while True:
        answer = input("Would you like another greeting? (yes/no) ").strip().lower()
        if answer == "yes":
            print(greet(name))
        elif answer == "no":
            print(farewell(name))
            break
        else:
            print("Please answer 'yes' or 'no'.")

