from state import PacbotState

gameState = PacbotState('192.168.0.101')

# Wait until game starts
while(gameState.state == gameState.STOPPED):
    gameState.poll()

# Game has started
while(gameState.state != gameState.STOPPED):
    gameState.poll()
