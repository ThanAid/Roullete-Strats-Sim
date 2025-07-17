import random
# from pyroullete.constants import MULTIPLIERS

class PyRoullete:
    def __init__(self, credits: float):
        self.credits = credits

    def get_balance(self) -> float:
        """
        Returns the current balance of the player.
        """
        return self.credits
    
    def spin(self):
        """
        Spins the roulette wheel and returns the result.
        """
        result = random.randint(0, 36)
        return result
    
    @staticmethod
    def get_bet_amount(bet_info: dict) -> float:
        """
        Calculates the total bet amount by summing all the values in the bet_info dictionary.
        """
        return sum(bet_info.values())
    
    def play(self, bet_info: dict):
        """
        Plays a round of roulette with the given bet information.
        """
        win = False
        bet_amount = self.get_bet_amount(bet_info=bet_info)

        if bet_amount > self.credits:
            raise ValueError("Bet amount exceeds current credits.")
        
        self.credits -= bet_amount
        result = self.spin()
        
        if str(result) in bet_info.keys():
            win = True
            self.credits += bet_info[str(result)] * 35 # TODO: as of now it only works when you play straight bets

        return {
            'result': result,
            'balance': self.get_balance(),
            'win': win,
            'bet_amount': bet_amount
        }