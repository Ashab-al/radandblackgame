import random
import time
from exceptions import NotCorrectColorIndex

class RedBlack:
    def __init__(self, user_color_index, bet):
        self.red_numbers = [number for number in range(1, 51)]
        self.black_numbers = [number for number in range(51, 101)]
        self.green_numbers = [0 for number in range(15)]

        self.game_box = self.red_numbers + self.black_numbers + self.green_numbers

        self.bet = bet
        self.user_number = self.__from_color_index_to_number(user_color_index)

    def start_game(self):
        self.__shuffle_game_box()
        self.game_number = self.__generate_number()

    def get_prize_color_bet(self):
        if (self.game_number in self.red_numbers and \
            self.user_number in self.red_numbers or \
            self.game_number in self.black_numbers and \
            self.user_number in self.black_numbers):
            return self.bet * 2
        
        elif self.game_number in self.green_numbers and \
            self.user_number in self.green_numbers:
            return self.bet * 14
        
        return -self.bet

    def check_correct_index_color(function):
        def wrapper(self, user_color_index, *args, **kwargs):
            if user_color_index not in range(0, 3):
                raise NotCorrectColorIndex("Введите корректный индекс цвета")
            return function(self, user_color_index, *args, **kwargs)
        return wrapper

    def __shuffle_game_box(self):
        return random.shuffle(self.game_box)

    def __generate_number(self):
        return random.sample(self.game_box, 1)[0]

    @check_correct_index_color
    def __from_color_index_to_number(self, user_color_index):
        if user_color_index == 1:
            return random.sample(self.red_numbers, 1)[0]
        if user_color_index == 2:
            return random.sample(self.black_numbers, 1)[0]
        return 0


class GameInterface:
    def __init__(self, game):
        self.game = game

    def drop_effect(function):
        def wrapper(self, *args, **kwargs):
            game_number_index = self.game.game_box.index(self.game.game_number)
            print_time = 20 + random.randint(0, 20)
            
            if game_number_index >= print_time:
                numbers = self.game.game_box[game_number_index - 20:game_number_index]
            else:
                numbers = self.game.game_box[game_number_index: game_number_index + 20]

            for index, number in enumerate(numbers, 1):
                print(f"{number}\n", end='')
                time.sleep(.1 + index/25)
            return function(self, *args, **kwargs)
        return wrapper

    @drop_effect
    def game_result_information(self):
        if self.game.game_number in self.game.red_numbers:
            print(f"Выпало красное -- {self.game.game_number}")
        
        elif self.game.game_number in self.game.black_numbers:
            print(f"Выпало чёрное -- {self.game.game_number}")
            
        else:
            print(f"Выпало зелёное -- {self.game.game_number}")
    
    def checking_winning(self):
        game_result = self.game.get_prize_color_bet()
        if game_result < 0:
            print("К сожалениею, вы проиграли")
        else:
            print("Поздравляем с победой!")

class User:
    def __init__(self, user_hash):
        self.username = user_hash["username"]
        self.bank = user_hash["bank"]

    def print_bank(self):
        print(f"Ваш банк -- {self.bank}")

    def update_user_bank(self, bet):
        return self.bank + bet


username = input("Введите ваш ник: ")
user_bank = int(input("Ваш банк: "))
user = User({"username": username, "bank": user_bank})

user_bet = int(input("Введите вашу ставку: "))
print("0. Зеленое\n1. Красное\n2. Чёрное")
user_color_choice = int(input("Цвет (выберите цифрой): "))

user.bank -= user_bet

game = RedBlack(user_color_choice, user_bet)
game.start_game()
prize = game.get_prize_color_bet()

console = GameInterface(game)

console.game_result_information()
console.checking_winning()

user.bank += prize
print(f"Ваш банк -- {user.bank}")
