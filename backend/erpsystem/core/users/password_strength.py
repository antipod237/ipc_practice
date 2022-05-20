class PasswordPolicy():
    def __init__(self, length, uppercase, numbers, special):
        self.length = length
        self.uppercase = uppercase
        self.numbers = numbers
        self.special = special

    def test(self, password):
        leng = len(password)
        upper = sum(i.isupper() for i in password)
        number = sum(i.isdigit() for i in password)
        spec = leng - number - sum(i.isalpha() for i in password)
        if (leng >= self.length and upper >= self.uppercase and
                number >= self.numbers and spec >= self.special):
            return True
        return False
