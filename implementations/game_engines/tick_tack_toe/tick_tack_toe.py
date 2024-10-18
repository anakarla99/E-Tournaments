from src.game.game import Game
from implementations.game_engines.tick_tack_toe.src.utils import Tokens
import implementations.game_engines.tick_tack_toe.src.ttt_game_state as TickTackToeGameState


class TickTackToeGame(Game):
    def __init__(self):
        super().__init__("TickTackToe")
        self._turn = 0
        self._winner = None
        
    def init_game_state(self):
        self._game_state = TickTackToeGameState.TTTGameState(self.players)

    def game_state(self) -> TickTackToeGameState.GameState:
        return self._game_state

    def get_winner(self) -> TickTackToeGameState.Player | None:
        if self._winner is not None:
            return self._winner
        
        board = self._game_state.board

        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] and board[i][0] != TickTackToeGameState.Tokens.EMPTY_TOKEN:
                self._winner = self.players[0 if board[i][0] == Tokens.PLAYER_0_TOKEN else 1]
            if board[0][i] == board[1][i] == board[2][i] and board[0][i] != TickTackToeGameState.Tokens.EMPTY_TOKEN:
                self._winner = self.players[0 if board[0][i] == Tokens.PLAYER_0_TOKEN else 1]

        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != TickTackToeGameState.Tokens.EMPTY_TOKEN:
            self._winner = self.players[0 if board[0][0] == Tokens.PLAYER_0_TOKEN else 1]
        if board[2][0] == board[1][1] == board[0][2] and board[2][0] != TickTackToeGameState.Tokens.EMPTY_TOKEN:
            self._winner = self.players[0 if board[2][0] == Tokens.PLAYER_0_TOKEN else 1]

        return self._winner

    def __next__(self):
        
        if self._game_state is None:
            self.init_game_state()
        if self._game_state.state == TickTackToeGameState.TTTGameState.IDLE:
            self._game_state.state = TickTackToeGameState.TTTGameState.IN_PROGRESS
        
        # Check if there is a winner
        winner = self.get_winner()
        if winner is not None:
            self._game_state.state = TickTackToeGameState.TTTGameState.FINISHED
        if self._turn == 9:
            self._game_state.state = TickTackToeGameState.TTTGameState.FINISHED
        
        if self._game_state.state == TickTackToeGameState.TTTGameState.FINISHED:
            raise StopIteration

        current_player = self._game_state.get_next_player()

        action = current_player.perform_a_move(self._game_state)

        self.perform_a_move(action)

        self._log.append(action)

        self._game_state.set_next_player()

        self._turn+=1
        
        return action

    def perform_a_move(self, action: TickTackToeGameState.Action):
        token = action.action["token"]
        x = action.action["i"]
        y = action.action["j"]

        self._game_state.board[x][y] = token

    def get_all_data_as_string(self):
        text = ""

        for action in self.logs:
            text += str(action) + "\n"

        return text
    
    def copy(self):
        return TickTackToeGame()
