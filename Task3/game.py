import hashlib
import hmac
import os
import sys
from typing import List, Tuple, Optional

class CryptoProvider:
    @staticmethod
    def generate_uniform_random(max_value: int) -> int:
        if max_value < 0:
            raise ValueError("max_value must be non-negative")
        return int.from_bytes(os.urandom(4), 'big') % (max_value + 1)

class FairNumberGenerator:
    def __init__(self, crypto_provider: CryptoProvider):
        self.crypto_provider = crypto_provider

    def generate_fair_number(self, max_value: int) -> Tuple[int, bytes, str]:
        key = os.urandom(16)
        number = self.crypto_provider.generate_uniform_random(max_value)
        hmac_value = hmac.new(key, str(number).encode(), hashlib.sha256).hexdigest()
        return number, key, hmac_value

class Die:
    def __init__(self, values: List[int]):
        if not values:
            raise ValueError("Die must have at least one face")
        self.values = values.copy()  # Create a copy to prevent modification

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, index: int) -> int:
        return self.values[index]

    def __repr__(self) -> str:
        return f"Die({self.values})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Die):
            return False
        return self.values == other.values

class TableGenerator:
    @staticmethod
    def generate_table(dice: List[Die]) -> None:
        print("\nProbability Table:")
        print("\t" + "\t".join([f"Die {i}" for i in range(len(dice))]))
        for i, die1 in enumerate(dice):
            row = [f"Die {i}"]
            for j, die2 in enumerate(dice):
                if i == j:
                    row.append("0.50")
                else:
                    row.append(TableGenerator._calculate_probability(die1, die2))
            print("\t".join(row))

    @staticmethod
    def _calculate_probability(die1: Die, die2: Die) -> str:
        wins = sum(1 for x in die1 for y in die2 if x > y)
        total = len(die1) * len(die2)
        return f"{(wins / total):.2f}"

class GameState:
    def __init__(self, dice: List[Die]):
        self.original_dice = dice
        self.available_dice = dice.copy()
        self.player_die = None
        self.computer_die = None

    def select_die(self, die: Die) -> None:
        if die in self.available_dice:
            self.available_dice.remove(die)

    def reset(self) -> None:
        self.available_dice = self.original_dice.copy()
        self.player_die = None
        self.computer_die = None

class GameController:
    def __init__(self, dice_values: List[List[int]]):
        if len(dice_values) < 3:
            raise ValueError("At least three dice must be provided")
        self.crypto_provider = CryptoProvider()
        self.fair_generator = FairNumberGenerator(self.crypto_provider)
        dice = [Die(values) for values in dice_values]
        self.state = GameState(dice)

    def start_game(self) -> None:
        print("Welcome to the Dice Game!")
        TableGenerator.generate_table(self.state.original_dice)

        print("\nLet's determine who will select their die first.")
        player_first = self._determine_first_player()

        if player_first:
            print("You will select your die first.")
            self.state.player_die = self._player_select_die()
            self.state.computer_die = self._computer_select_die()
        else:
            print("Computer will select its die first.")
            self.state.computer_die = self._computer_select_die()
            self.state.player_die = self._player_select_die()

        print(f"\nYou selected: {self.state.player_die}")
        print(f"Computer selected: {self.state.computer_die}")

        print("\nTime to roll the dice!")
        player_score = self._make_throw("Your throw", self.state.player_die)
        computer_score = self._make_throw("Computer's throw", self.state.computer_die)

        print(f"\nYour score: {player_score}")
        print(f"Computer's score: {computer_score}")

        if player_score > computer_score:
            print("Congratulations, you win!")
        elif player_score < computer_score:
            print("Sorry, the computer wins.")
        else:
            print("It's a tie!")

    def _determine_first_player(self) -> bool:
        computer_num, key, hmac_value = self.fair_generator.generate_fair_number(1)
        print(f"I selected a random number (HMAC={hmac_value}).")
        print("Guess the number: 0 or 1")

        while True:
            choice = input("Your guess: ").strip()
            if choice not in ('0', '1'):
                print("Invalid choice. Please enter 0 or 1.")
                continue
            player_guess = int(choice)
            print(f"My number is {computer_num} (KEY={key.hex().upper()}).")
            return player_guess == computer_num

    def _computer_select_die(self) -> Die:
        available = self.state.available_dice
        if not available:
            raise ValueError("No dice available for selection")
        
        computer_choice = self.crypto_provider.generate_uniform_random(len(available) - 1)
        selected_die = available[computer_choice]
        self.state.select_die(selected_die)
        return selected_die

    def _player_select_die(self) -> Die:
        available = self.state.available_dice
        print("Choose your dice:")
        for i, die in enumerate(available):
            print(f"{i} - {die}")

        while True:
            choice = input("Your selection: ").strip()
            if not choice.isdigit() or int(choice) >= len(available):
                print("Invalid selection. Please try again.")
                continue
            selected_die = available[int(choice)]
            self.state.select_die(selected_die)
            return selected_die

    def _make_throw(self, context: str, die: Die) -> int:
        computer_num, key, hmac_value = self.fair_generator.generate_fair_number(len(die) - 1)
        print(f"{context}: I selected a random value in the range 0..{len(die) - 1} (HMAC={hmac_value}).")
        print("Add your number modulo the die size.")

        for i in range(len(die)):
            print(f"{i} - {die[i]}")

        while True:
            choice = input("Your selection: ").strip()
            if not choice.isdigit() or int(choice) >= len(die):
                print("Invalid selection. Please try again.")
                continue
            player_num = int(choice)
            result = (player_num + computer_num) % len(die)
            print(f"My number is {computer_num} (KEY={key.hex().upper()}).")
            print(f"The result is {player_num} + {computer_num} = {result} (mod {len(die)}).")
            return die[result]

def parse_dice_input(args: List[str]) -> List[List[int]]:
    dice_values = []
    for arg in args:
        try:
            values = [int(x) for x in arg.split(',')]
            if not values:
                raise ValueError("Empty dice values")
            dice_values.append(values)
        except ValueError as e:
            print(f"Error parsing dice values '{arg}': {e}")
            sys.exit(1)
    return dice_values

def main() -> None:
    if len(sys.argv) < 4:  # Require at least 3 dice
        print("Usage: python game.py dice1 dice2 dice3 [dice4 ...]")
        print("Example: python game.py 1,2,3,4,5,6 1,1,1,6,6,6 2,2,2,5,5,5")
        sys.exit(1)

    try:
        dice_values = parse_dice_input(sys.argv[1:])
        game = GameController(dice_values)
        game.start_game()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()