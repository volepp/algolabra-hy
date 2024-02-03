import numpy as np

class Move:

    file_mapping_int_to_str = {
        0: "a",
        1: "b",
        2: "c",
        3: "d",
        4: "e",
        5: "f",
        6: "g",
        7: "h"
    }
    file_mapping_str_to_int = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7
    }

    def __init__(self, from_square: np.array, to_square: np.array):
        """ Rank is given as an integer so that
        a=1, b=2, c=3, ..., h=8. file is the number of the file.
        """
        self.from_square = from_square
        self.to_square = to_square

    def to_uci(self) -> str:
        """ Converts the given move (np.array([file, rank])) to UCI string format.
        """

        from_sqr = f"{self.file_mapping_int_to_str[self.from_square[1]]}{self.from_square[0]+1}"
        to_sqr = f"{self.file_mapping_int_to_str[self.to_square[1]]}{self.to_square[0]+1}"
        return f"{from_sqr}{to_sqr}"
    
    @staticmethod
    def parse_uci(uci: str):
        """ Parses a move from the given UCI string and returns it.
        """
        if len(uci) != 4:
            raise ValueError(f"Wrongly formatted UCI: {uci}")
        
        from_sqr_str = uci[:2]
        to_sqr_str = uci[2:]
        from_sqr = np.array([
            int(from_sqr_str[1])-1,
            Move.file_mapping_str_to_int[from_sqr_str[0]],
            ])
        to_sqr = np.array([
            int(to_sqr_str[1])-1,
            Move.file_mapping_str_to_int[to_sqr_str[0]],
            ])
        
        return Move(from_sqr, to_sqr)
    
    def __repr__(self):
        return self.to_uci()
    
    def __str__(self):
        return self.to_uci()
    
    def __eq__(self, other):
        if not np.array_equal(self.from_square, other.from_square):
            return False
        elif not np.array_equal(self.to_square, other.to_square):
            return False
        return True