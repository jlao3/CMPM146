
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log, inf
import p3_t3

num_nodes = 100
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
    currentNode = node

    while not currentNode.untried_actions and currentNode.child_nodes: #no untried actions left, child nodes available to traverse
        nextNode = None
        highScore = -inf
        for catcher, childNode in currentNode.child_nodes.items(): #catcher contains values we don't care about in node, childNode is what we want to check
            childNode.visits += 1
            if identity == 'red':   # if red then value is equal to 1, thus nothing happens
                tempScore = (childNode.wins / childNode.visits) + (explore_faction * sqrt(log(childNode.parent.visits) / childNode.visits))
            else:   # else identity is blue, thus multiple by -1
                tempScore = ((-1 * childNode.wins) / childNode.visits) + (explore_faction * sqrt(log(childNode.parent.visits) / childNode.visits))
            if tempScore > highScore:   # if temporary score is higher then our best, then make that the next searched node and update highScore
                highScore = tempScore
                nextNode = childNode
        currentNode = nextNode

    return currentNode  # return the best childNode
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
        action = node.untried_actions.pop() # tries to pop() an action from the list
    except:
        return node # if list is empty, return node
    else:
        state = board.next_state(state, action)
        new_node = MCTSNode(parent=node, parent_action=action,action_list=board.legal_actions(state)) # create new leaf with list of legal actions
        node.child_nodes[action] = new_node # make pointer of child node equal the new_node
        return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.
    Args:
        board:  The game setup.
        state:  The state of the game.
    """
    while not board.is_ended(state):    # while game is not done
        possible_actions = board.legal_actions(state)   # acquire a list of legal actions
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
        node.wins += won    # -1 if lost, 0 for draw/nothing, 1 for win
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

    for _ in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        node = traverse_nodes(node, board, sampled_game, identity_of_bot)

        selected_node = node
        select_actions = []

        while selected_node.parent:
            select_actions.append(selected_node.parent_action)
            selected_node = selected_node.parent
        select_actions.reverse()

        for action in select_actions:
            sampled_game = board.next_state(sampled_game, action)

        if not node.untried_actions:
            won = board.points_values(sampled_game)[1]
        else:
            node = expand_leaf(node, board, sampled_game)
            sampled_game = board.next_state(sampled_game, node.parent_action)
            sampled_game = rollout(board, sampled_game)
            won = board.points_values(sampled_game)[1]
        backpropagate(node, won)

    best_winrate = -inf
    if identity_of_bot == 1:
        sign = 1
    else:
        sign = -1
    for action, child in root_node.child_nodes.items():
        child_winrate = (child.wins/child.visits)*sign
        if child_winrate > best_winrate:
            best_action = action
            best_winrate = child_winrate

    return best_action
