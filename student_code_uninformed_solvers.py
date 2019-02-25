
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        movables = self.gm.getMovables()
        moves_left = True

        if movables:
            for m in movables:  # create a GameState for each movable, put it in children

                # store the tuples of the child GameState
                self.gm.makeMove(m)
                new_state = self.gm.getGameState()
                self.gm.reverseMove(m)

                # defining the new child, and its parent (current state)
                child = GameState(new_state, (self.currentState.depth+1), m)
                child.parent = self.currentState

                print('child:' + str(child.state))

                # append child state to the list inside current state
                self.currentState.children.append(child)

            while self.currentState.children[self.currentState.nextChildToVisit] in self.visited:  # check if queued up child has already been visited
                if self.currentState.nextChildToVisit == (len(self.currentState.children)-1):  # just reached last child, and it was already visited
                    moves_left = False
                    break
                self.currentState.nextChildToVisit += 1  # if it has, increment to the next one, until it is new, then exits

        elif not movables:  # there are no movable disks/pieces (probably shouldn't happen but in case)
            moves_left = False


        if moves_left:
            # we will not increment nextChildToVisit so it stays on the same element, in case it's the last one
            # if we return to it, it will enter while loop, find True in dict, find itself as the last element, and moves_left -> False
            self.gm.makeMove(self.currentState.children[self.currentState.nextChildToVisit].requiredMovable)
            self.currentState = self.currentState.children[self.currentState.nextChildToVisit]
            self.visited[self.currentState] = True

            print(self.currentState.state)

            # DID WE WIN OR NAH
            return self.gm.isWon()
        elif not moves_left:
            # YIKES HERE WE GO
            new_moves = False
            index = 0

            while new_moves is False:  # keep moving up the tree until we find a GameState with undiscovered children
                self.gm.reverseMove(self.currentState.requiredMovable)  # move up to parent
                self.currentState = self.currentState.parent

                for i in range(len(self.currentState.children)):
                    # if a GameState has not been visited, remember its index in its parent's children list and exit
                    if self.currentState.children[i] not in self.visited:
                        index = i
                        new_moves = True
                        break

            # assign the index found to nexChildtoVisit
            self.currentState.nextChildToVisit = index

            self.gm.makeMove(self.currentState.children[self.currentState.nextChildToVisit].requiredMovable)
            self.currentState = self.currentState.children[self.currentState.nextChildToVisit]
            self.visited[self.currentState] = True

            print(self.currentState.state)

            # DID WE WIN OR NAH
            return self.gm.isWon()


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        return True
