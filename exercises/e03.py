def greet(name):
    if name == 'Andrej':
        return f"Ciao {name}!"
    return f"Hello {name}!"

name = input("What is your name?")
print(greet(name))
