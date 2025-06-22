import numpy as np
from cube.utils import d_action_turn

def generate_scramble(scramble_moves_count=25):
    '''
    Generate a random scramble of moves.

    NOTE! This current implementation allows for "invalid" scrambles with repeating moves such as R R R...
    '''
    
    np_random_numers = np.random.randint(0, 17, size=scramble_moves_count)

    return [d_action_turn[action] for action in np_random_numers]
