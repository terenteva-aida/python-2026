class Game:
    def __init__(self):
        word = input("Введите слово из 5 букв: ")
        self.word = word
        self.word_len = len(word)
        self.field = ["x"] * self.word_len
        self.mistakes = 5
    
    def run(self):
        while 'x' in self.field and self.mistakes > 0:
            letter = input("Введите букву: ")
            found = self.check_letter(letter)
            
            if not found:
                self.mistakes -= 1
                print(f"Осталось попыток: {self.mistakes}")
            else:
                print("Угадал!")
            
            print(self.field)
        
        self.show_result()
    
    def check_letter(self, letter):
        found = False
        for key in range(self.word_len):
            if letter == self.word[key]:
                self.field[key] = letter
                found = True
        return found
    
    def show_result(self):
        if 'x' not in self.field:
            print("Поздравляю! Вы отгадали слово!")
        else:
            print("Вы проиграли. Загаданное слово:", self.word)

g = Game()
g.run()