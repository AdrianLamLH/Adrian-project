self.block_list = list(self.block_list_temp)
for self.countermoveright in range(4):
    TGrid[((self.block_list[self.countermoveright])[0])][(self.block_list[self.countermoveright])[1]] = 0
for self.countmoveright in range(4):
    (self.block_list[self.countmoveright])[1] = (self.block_list[self.countmoveright])[
                                                   1] + 1  # Update the moved blocks once moved
    TGrid[((self.block_list[self.countmoveright])[0])][(self.block_list[self.countmoveright])[1]] = BlockColour[
        self.block_colour]