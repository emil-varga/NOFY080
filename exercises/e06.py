class Fraction:
    """ Represents a/b """
    def __init__(self, a, b):
        self.a = a
        self.b = b

    # the __something__ methods are called magic or dunder (Double UNDERscore)
    # they indicate some built-in syntax, for example, if f1 and f2 are Fractions
    #f1 + f2 is translated to f1.__add__(f2)
    def __add__(self, other):
        return Fraction(self.a*other.b + self.b*other.a,
                        self.b*other.b)
    
    #f1 - f2 -> f1.__sub__(f2)
    def __sub__(self, other):
        return Fraction(self.a*other.b - self.b*other.a,
                        self.b*other.b)
    
    #f1 * f2 -> f1.__mul__(f2)
    def __mul__(self, other):
        return Fraction(self.a*other.a, self.b*other.b)
    
    #f1 / f2 -> f1.__truediv__(f2)
    def __truediv__(self, other):
        return Fraction(self.a*other.b, self.b*other.a)
    
    def value(self):
        return self.a/self.b
    
    # str(f1) -> f1.__str__(); used in print()
    #textual representation of the object
    def __str__(self):
        return f"{self.a}/{self.b}"
    #__repr__ is similar to __str__, except it
    #gets called when we simply evaluate the object
    #in REPL
    def __repr__(self):
        return str(self)
    
    #f1(args) -> f1.__call__(args)
    def __call__(self):
        return self.value()
    
    #f1[idx] -> f1.__getitem__(idx)
    def __getitem__(self, idx):
        if idx == 0:
            return self.a
        elif idx == 1:
            return self.b
        else:
            raise ValueError

if __name__ == '__main__':
    f1 = Fraction(1,2)
    f2 = Fraction(3,4)
    
    print(f1 + f2) # === f1.__add__(f2)
    print(f1.value())
    print(f1.__str__())
    print((f1 + f2).value())
    print(f1.value() + f2.value())
    print(f1())
    print(f1[0])