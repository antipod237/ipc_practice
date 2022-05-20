class PasswordPolicy():
    def __init__(self, length, uppercase, numbers, special):
        self.length = length
        self.uppercase = uppercase
        self.numbers = numbers
        self.special = special

    def test(self, password):
         l = len(password)
         u = sum(i.isupper() for i in password)
         n = sum(i.isdigit() for i in password)
         s = l - n - sum(i.isalpha () for i in password)
         if (l >= self.length and u >= self.uppercase and n >= self.numbers and s >= self.special): 
            return True
         return False

