
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log
import p3_t3

num_nodes = 1000
explore_faction = 2.

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    bestNode = node
    currentNode = node

    bestScore = 0
    tempScore = 0
    
    while not currentNode.untried_actions and currentNode.child_nodes:
        pointerNode = None
        for currChild in currentNode.child_nodes:
            if currChild.visits != 0:
                if identity == 'red':
                    tempScore = (currChild.wins / currChild.visits) + (explore_faction * sqrt(log(node.visits) / currChild.visits))
                if identity == 'blue':
                    tempScore = (1 - (currChild.wins / currChild.visits)) + (explore_faction * sqrt(log(node.visits) / currChild.visits))
            else:
                tempScore = 0

            if tempScore > bestScore:
                bestScore = tempScore
                bestNode = currChild
                pointerNode = currChild
        currentNode = pointerNode
    
    return bestNode
    # Hint: return leaf_node


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    try:
        action = node.untried_actions.pop() #tries to pop() an action from the list
    except:
        return node #if list is empty, return node
    else:
        state = board.next_state(state, action)
        new_node = MCTSNode(parent=node, parent_action=action,action_list=node.untried_actions) #create new leaf with list of untried actions
        node.child_nodes[action] = new_node #make pointer of child node equal the new_node

    return new_node
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    while not board.is_ended(state):    # while game is not done
        possible_actions = board.legal_actions(state)   #acquire a list of legal actions
        action = choice(possible_actions)   # choose a random action
        state = board.next_state(state, action) # state becomes the next state of chosen action
    return state


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    while node is not None: # while backtracking is true
        node.wins += 1      # -1 if lost, 0 for draw/nothing, 1 for win
        node.visits += 1    # count for visits
        node = node.parent  # traverse to parent node


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        node = root_node
        node = traverse_nodes(node, board, sampled_game, identity_of_bot)

        leaf_node = expand_leaf(node, board, sampled_game)
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return None
