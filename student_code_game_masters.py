from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        # find list of all facts that are (on ?disk ?peg) to find all positions
        matches = self.kb.kb_ask(Fact(Statement(['on', Term('?disk'), Term('?peg')]), []))

        # empty lists for each peg
        p1 = []
        p2 = []
        p3 = []

        for b in matches:
            disk = int(str(b.bindings[0].constant)[4])  # disk is its respective int
            peg = str(b.bindings[1].constant)  # peg is 'peg_' with its respective number

            # append disk to correct peg
            if peg == 'peg1':
                p1.append(disk)
            elif peg == 'peg2':
                p2.append(disk)
            elif peg == 'peg3':
                p3.append(disk)

        p1.sort()
        p2.sort()
        p3.sort()

        state = (tuple(p1), tuple(p2), tuple(p3))

        return state

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        info = movable_statement.terms  # disk, start, end (type Term)

        # new/old on, top statements pertaining to moving disk
        initial_on = Fact(Statement(['on', info[0], info[1]]), [])
        initial_top = Fact(Statement(['top', info[0], info[1]]), [])
        final_on = Fact(Statement(['on', info[0], info[2]]), [])
        final_top = Fact(Statement(['top', info[0], info[2]]), [])

        # check for top disk on the receiving peg
        receiving = self.kb.kb_ask(Fact(Statement(['top', Term('?disk'), info[2]]), []))

        if receiving is False:  # if no top disk on receiving peg, it was empty and will soon not be
            self.kb.kb_retract(Fact(Statement(['empty', info[2]]), []))
        else:  # retract the fact for the previous top of the receiving peg
            self.kb.kb_retract(Fact(Statement(['top', receiving[0].bindings[0].constant, info[2]]), []))

        # assert and retract the new facts for moving disk
        self.kb.kb_retract(initial_on)
        self.kb.kb_retract(initial_top)
        self.kb.kb_assert(final_on)
        self.kb.kb_assert(final_top)

        # check for remaining disks on start peg
        remaining = self.kb.kb_ask(Fact(Statement(['on', Term('?disk'), info[1]]), []))

        if remaining is False:  # if no pegs remain, assert that it's empty
            self.kb.kb_assert(Fact(Statement(['empty', info[1]]), []))
        else:  # assert a new top fact for the start peg by finding the smallest disk on it
            disk_num = 10
            new_top = None
            for b in remaining:  # find smallest disk on start pin
                if int(str(b.bindings[0].constant)[4]) < disk_num:
                    disk_num = int(str(b.bindings[0].constant)[4])
                    new_top = b.bindings[0].constant

            # assert new top of start peg
            self.kb.kb_assert(Fact(Statement(['top', new_top, info[1]]), []))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))


class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here

        # find list of all facts that are (position ?piece ?x ?y) to find all positions
        matches = self.kb.kb_ask(Fact(Statement(['position', Term('?piece'), Term('?x'), Term('?y')]), []))

        # lists for each row
        r1 = [0, 0, 0]
        r2 = [0, 0, 0]
        r3 = [0, 0, 0]

        for b in matches:
            piece = int(str(b.bindings[0].constant)[5])  # piece is its respective int

            if piece == 0:  # piece0 is the empty space
                piece = -1

            column = int(str(b.bindings[1].constant)[3])  # column is x
            row = int(str(b.bindings[2].constant)[3])  # row is y

            # append disk to correct peg
            if row == 1:
                r1[column-1] = piece
            elif row == 2:
                r2[column-1] = piece
            elif row == 3:
                r3[column-1] = piece

        state = (tuple(r1), tuple(r2), tuple(r3))

        return state

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        info = movable_statement.terms  # piece, x1, y1, x2, y2 (type Term)

        # new/old position statements pertaining to moving piece, empty space
        piece_new = Fact(Statement(['position', info[0], info[3], info[4]]), [])
        piece_old = Fact(Statement(['position', info[0], info[1], info[2]]), [])
        empty_new = Fact(Statement(['position', Term('piece0'), info[1], info[2]]), [])
        empty_old = Fact(Statement(['position', Term('piece0'), info[3], info[4]]), [])

        self.kb.kb_retract(piece_old)
        self.kb.kb_retract(empty_old)
        self.kb.kb_assert(piece_new)
        self.kb.kb_assert(empty_new)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
