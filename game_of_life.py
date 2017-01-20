from graphics import *
import random

## Written by Sarina Canelake & Kelly Casteel, August 2010
## Revised January 2011
## Final Results by R. Thomas Dixon January 2017

############################################################
# GLOBAL VARIABLES
############################################################
    
BLOCK_SIZE = 20
BLOCK_OUTLINE_WIDTH = 2
BOARD_WIDTH = 40
BOARD_HEIGHT = 40

neighbor_test_blocklist = [(0,0), (1,1)]
toad_blocklist = [(4,4), (3,5), (3,6), (5,7), (6,5), (6,6)]
beacon_blocklist = [(2,3), (2,4), (3,3), (3,4), (4,5), (4,6), (5,5), (5,6)]
glider_blocklist = [(1,2), (2,3), (3,1), (3,2), (3,3)]
pulsar_blocklist = [(2,4), (2,5), (2,6), (4,2), (4,7), (5,2), (5,7),
                    (6,2), (6,7), (7,4), (7,5), (7,6), ]
# for diehard, make board at least 25x25, might need to change block size
diehard_blocklist = [(15,17), (16,17), (16,18), (20,18), (21,18), (22,18), (21,16)]

############################################################
# TEST CODE (don't worry about understanding this section)
############################################################

def test_neighbors(board):
    '''
    Code to test the board.get_block_neighbor function
    '''
    for block in board.block_list.values():
        neighbors = board.get_block_neighbors(block)
        ncoords = [neighbor.get_coords() for neighbor in neighbors]
        if block.get_coords() == (0,0):
            zeroneighs = [(0,1), (1,1), (1,0)]
            for n in ncoords:
                if n not in zeroneighs:
                    print "Testing block at (0,0)"
                    print "Got", ncoords
                    print "Expected", zeroneighs
                    return False

            for neighbor in neighbors:
                if neighbor.get_coords() == (1, 1):
                    if neighbor.is_live() == False:
                        print "Testing block at (0, 0)..."
                        print "My neighbor at (1, 1) should be live; it is not."
                        print "Did you return my actual neighbors, or create new copies of them?"
                        print "FAIL: get_block_neighbors() should NOT return new Blocks!"
                        return False

        elif block.get_coords() == (1,1):
            oneneighs = [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1),(2,2)]
            for n in ncoords:
                if n not in oneneighs:
                    print "Testing block at (1,1)"
                    print "Got", ncoords
                    print "Expected", oneneighs
                    return False
            for n in oneneighs:
                if n not in ncoords:
                    print "Testing block at (1,1)"
                    print "Got", ncoords
                    print "Expected", oneneighs
                    return False
    print "Passed neighbor test"
    return True


############################################################
# BLOCK CLASS (Read through and understand this part!)
############################################################

class Block(Rectangle):
    ''' Block class:
        Implement a block for a tetris piece
        Attributes: x - type: int
                    y - type: int
        specify the position on the board
        in terms of the square grid
    '''

    def __init__(self, pos, color):
        '''
        pos: a Point object specifing the (x, y) square of the Block (NOT in pixels!)
        color: a string specifing the color of the block (eg 'blue' or 'purple')
        '''
        self.x = pos.x
        self.y = pos.y
        
        p1 = Point(pos.x*BLOCK_SIZE,
                   pos.y*BLOCK_SIZE)
        p2 = Point(p1.x + BLOCK_SIZE, p1.y + BLOCK_SIZE)

        Rectangle.__init__(self, p1, p2)
        self.setWidth(BLOCK_OUTLINE_WIDTH)
        self.setFill(color)
        self.status = 'dead'
        self.new_status = 'None'
        
    def get_coords(self):
        return (self.x, self.y)

    def set_live(self, canvas):
        '''
        Sets the block status to 'live' and draws it on the grid.
        Be sure to do this on the canvas!
        '''
        if self.status=='dead':
          self.status = 'live'
          self.draw(canvas)

    def set_dead(self):
        '''
        Sets the block status to 'dead' and undraws it from the grid.
        '''
        if self.status=='live':
          self.status = 'dead'
          self.undraw()

    def is_live(self):
        '''
        Returns True if the block is currently 'live'. Returns False otherwise.
        '''
        if self.status == 'live':
            return True
        return False

    def reset_status(self, canvas):
        '''
        Sets the new_status to be the current status
        '''
        if self.new_status=='dead':
            self.set_dead()
        elif self.new_status=='live':
            self.set_live(canvas)
        

###########################################################
# BOARD CLASS (Read through and understand this part!)
# Print out and turn in this section.
# Name:
# Recitation:
###########################################################

class Board(object):
    ''' Board class: it represents the Game of Life board

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:CanvasFrame - where the blocks will be drawn
                    block_list - type:Dictionary - stores the blocks for a given position
    '''
    
    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.win = win
        # self.delay is the number of ms between each simulation. Change to be
        # shorter or longer if you wish!
        self.delay = 100

        # create a canvas to draw the blocks on
        self.canvas = CanvasFrame(win, self.width * BLOCK_SIZE,
                                       self.height * BLOCK_SIZE)
        self.canvas.setBackground('black')

        # initialize grid lines
        for x in range(1,self.width):
            self.draw_gridline(Point(x, 0), Point(x, self.height))

        for y in range(1,self.height):
            self.draw_gridline(Point(0, y), Point(self.width, y))

        # For each square on the board, we need to initialize
        # a block and store that block in a data structure. A
        # dictionary (self.block_list) that has key:value pairs of
        # (x,y):Block will be useful here.
        self.block_list = {}
        i=0
        j=0
        for x in range (0,self.width):
            for y in range (0,self.height):
                pt=Point(i,j)
                block = Block(pt, "yellow")
                block_loc = (x,y)
                self.block_list.update({block_loc : block})
                j=j+1
            j = 0
            i=i+1

        ####### YOUR CODE HERE ######
        #raise Exception("__init__ not implemented")


    def draw_gridline(self, startp, endp):
        ''' Parameters: startp - a Point of where to start the gridline
                        endp - a Point of where to end the gridline
            Draws two straight 1 pixel lines next to each other, to create
            a nice looking grid on the canvas.
        '''
        line = Line(Point(startp.x*BLOCK_SIZE, startp.y*BLOCK_SIZE), \
                    Point(endp.x*BLOCK_SIZE, endp.y*BLOCK_SIZE))
        line.setFill("white")
        line.draw(self.canvas)
        
        line = Line(Point(startp.x*BLOCK_SIZE-1, startp.y*BLOCK_SIZE-1), \
                    Point(endp.x*BLOCK_SIZE-1, endp.y*BLOCK_SIZE-1))
        line.draw(self.canvas)


    def random_seed(self, percentage):
        ''' Parameters: percentage - a number between 0 and 1 representing the
                                     percentage of the board to be filled with
                                     blocks
            This method activates the specified percentage of blocks randomly.
        '''
        for block in self.block_list.values():
            if random.random() < percentage:
                block.set_live(self.canvas)
                print "("+str(block.x)+", "+str(block.y)+")"

    def seed(self, block_coords):
        '''
        Seeds the board with a certain configuration.
        Takes in a list of (x, y) tuples representing block coordinates,
        and activates the blocks corresponding to those coordinates.
        '''
        for val in block_coords:
            x = val[0]
            y= val[1]
            #print "("+str(x)+", "+str(y)+")"
            for pt in self.block_list.values():
                #print "("+str(pt.x)+", "+str(pt.y)+")"
                if pt.x == x and pt.y ==y:
                    #print "Match!"
                    pt.set_live(self.canvas)
    


    def get_block_neighbors(self, block):
        '''
        Given a Block object, returns a list of neighboring blocks.
        Should not return itself in the list.
        |1|2|3|
        -------
        |4|5|6|
        -------
        |7|8|9|
        self.block_list['value']
        '''
        block1 = (block.x-1,block.y-1)
        block2 = (block.x,block.y-1)
        block3 = (block.x+1,block.y-1)
        block4 = (block.x-1,block.y)
        block6 = (block.x+1,block.y)
        block7 = (block.x-1,block.y+1)
        block8 = (block.x, block.y+1)
        block9 = (block.x+1, block.y+1)
        
        if(block.x==0):
            if(block.y==0):
                #check 6,8,9
                blk_list = (self.block_list[block6],self.block_list[block8],self.block_list[block9])
            elif(block.y==BOARD_HEIGHT-1):
                #check 2,3,6
                blk_list=(self.block_list[block2], self.block_list[block3], self.block_list[block6])
            else:
                #check 2,3,6,8,9
                blk_list=(self.block_list[block2], self.block_list[block3], self.block_list[block6], self.block_list[block8], self.block_list[block9])
        elif(block.x==BOARD_WIDTH-1):
            if(block.y==0):
                #check 4,7,8
                blk_list=(self.block_list[block4], self.block_list[block7], self.block_list[block8])
            elif(block.y==BOARD_HEIGHT-1):
                #check 1,2,4
                blk_list=(self.block_list[block1], self.block_list[block2], self.block_list[block4])
            else:
                #check 1,2,4,7,8
                blk_list=(self.block_list[block1], self.block_list[block2], self.block_list[block4], self.block_list[block7], self.block_list[block8])
        elif(block.y==BOARD_HEIGHT-1):
            #check 1,2,3,4,6
            blk_list=(self.block_list[block1], self.block_list[block2], self.block_list[block3], self.block_list[block4], self.block_list[block6])
        elif(block.y==0):
            #check 4,6,7,8,9
            blk_list=(self.block_list[block4], self.block_list[block6], self.block_list[block7], self.block_list[block8], self.block_list[block9])
        else:
            #check 1,2,3,4,6,7,8,9
            blk_list=(self.block_list[block1], self.block_list[block2], self.block_list[block3], self.block_list[block4], self.block_list[block6], self.block_list[block7], self.block_list[block8], self.block_list[block9])
        return blk_list
        
    def simulate(self):
        '''
        Executes one turn of Conways Game of Life using the rules
        listed in the handout. Best approached in a two-step strategy:
        
        1. Calculate the new_status of each block by looking at the
           status of its neighbors.

        2. Set blocks to 'live' if their new_status is 'live' and their
           status is 'dead'. Similarly, set blocks to 'dead' if their
           new_status is 'dead' and their status is 'live'. Then, remember
           to call reset_status(self.canvas) on each block.
        '''
        copy_dict=self.block_list
        count = 0
        for block in copy_dict.values():
            live_n=0            
            for blk in self.get_block_neighbors(block):
                if(blk.is_live()):
                    live_n=live_n+1
            if(live_n<2 and block.is_live()):
                block.new_status = 'dead'
            elif(live_n>3 and block.is_live()):
                block.new_status = 'dead'
            elif(block.is_live() and live_n==2 or live_n==3):
                block.new_status = 'live'
            elif(not block.is_live() and live_n==3):
                block.new_status = 'live'
            else:
                block.new_status = block.status
                count = count+1
                #print count
            block_loc=(block.x,block.y)
            self.block_list.update({block_loc: block})
        for b  in self.block_list.values():
            b.reset_status(self.canvas)
            

        #### YOUR CODE HERE #####
        #raise Exception("simulate not implemented")

        

    def animate(self):
        '''
        Animates the Game of Life, calling "simulate"
        once every second
        '''
        self.simulate()
        self.win.after(self.delay, self.animate)



################################################################
# RUNNING THE SIMULATION
################################################################

if __name__ == '__main__':    
    # Initalize board
    win = Window("Conway's Game of Life")
    board = Board(win, BOARD_WIDTH, BOARD_HEIGHT)

    ## PART 1: Make sure that the board __init__ method works    
    #board.random_seed(.15)

    ## PART 2: Make sure board.seed works. Comment random_seed above and uncomment
    ##  one of the seed methods below
    #board.seed(toad_blocklist)

    ## PART 3: Test that neighbors work by commenting the above and uncommenting
    ## the following two lines:
    #board.seed(neighbor_test_blocklist)
    #test_neighbors(board)


    ## PART 4: Test that simulate() works by uncommenting the next two lines:
    #board.seed(toad_blocklist)
    #board.seed(beacon_blocklist)
    #board.seed(glider_blocklist)
    #board.seed(pulsar_blocklist)
    board.seed(diehard_blocklist)
    #win.after(2000, board.simulate)

    ## PART 5: Try animating! Comment out win.after(2000, board.simulate) above, and
    ## uncomment win.after below.
    win.after(2000, board.animate)

    ## Yay, you're done! Try seeding with different blocklists (a few are provided at the top of this file!)
    
    win.mainloop()
                
