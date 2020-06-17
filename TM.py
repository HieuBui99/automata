import sys
import string

class Turing_Machine:
    def __init__(self,state,write_head,tape_list):
        self.state = state
        self.write_head = write_head
        self.tape_list = tape_list

    def getState(self):
        return self.state

    def getHead(self):
        return self.write_head
    
    def getList(self):
        return self.tape_list

    # Table of rules!
    def updateMachine(self):
        # Initial State
        if (self.state == 'q1'):
            if (self.tape_list[self.write_head] != 0):
                ### STATE ### (p)
                char_read = self.tape_list[self.write_head]
                char_index = character_list.index(char_read)
                self.state = ''.join(['p',str(char_index)])
                ### WRITE ### (zero)
                self.tape_list[self.write_head] = 0
                ### MOVE ### (right)
                self.write_head += 1
            else:
                ### STATE ### (qy)
                self.state = 'qy'
                ### WRITE ### (zero, unchanged)
                self.tape_list[self.write_head] = 0
                ### MOVE ### (right) (doesnt matter)
                self.write_head += 1
    
        elif (self.state.startswith('p')):
            if (self.tape_list[self.write_head]!=0):
                ### STATE ### (unchanged)
                self.state = self.state
                ### WRITE ### (unchanged)
                self.tape_list[self.write_head] = self.tape_list[self.write_head]
                ### MOVE ### (right)
                self.write_head += 1
            else:
                ### STATE ### (r)
                self.state = ''.join(['r',self.state[1:]])
                ### WRITE ### (zero, unchanged)
                self.tape_list[self.write_head] = 0
                ### MOVE ### (left)
                self.write_head -= 1
                    
        elif (self.state.startswith('r')):
            char_read = character_list[int(self.state[1:])]
            if (self.tape_list[self.write_head] != char_read and self.tape_list[self.write_head] != 0): # zero is needed for strings of odd length
                ### STATE ### (qn)
                self.state = 'qn'
                ### WRITE ###
                self.tape_list[self.write_head] = self.tape_list[self.write_head]
                ### MOVE ### (left) (doesn't matter)
                self.write_head -= 1
            else:
                ### STATE ###
                self.state = 'q2'
                ### WRITE ### (zero)
                self.tape_list[self.write_head] = 0
                ### MOVE ### (left)
                self.write_head -= 1
                
        elif (self.state == 'q2'):
            if (self.tape_list[self.write_head] != 0):
                ### STATE ### (unchanged)
                self.state = 'q2'
                ### WRITE ### (unchanged)
                self.tape_list[self.write_head] = self.tape_list[self.write_head]
                ### MOVE ### (left)
                self.write_head -= 1
            else:
                ### STATE ### (q1)
                self.state = 'q1'
                ### WRITE ### (zero)
                self.tape_list[self.write_head] = 0
                ### MOVE ### (right)
                self.write_head += 1

# Define Character Set (allowed characters for the palindrome)
character_list = list(string.ascii_lowercase)
character_list.append(' ') # to allow for spaces

# Initial string
initial_string = 'aba'
print('Checking...',initial_string)
print('- - -')
initial_list = list(initial_string)

# Quick check that you only used allow characters
for i in initial_list:
    if i not in character_list:
        print('Error! Initial character >',i,'< not in allowed character list!')
        sys.exit()

# Append list
initial_list.append(0);

# Set up the turing machine
i_write_head = 0
i_state = 'q1' # initial state
i_tape_list = initial_list

# Initiate the class
runMachine = Turing_Machine(i_state,i_write_head,i_tape_list)
print(runMachine.getState(),runMachine.getHead(),runMachine.getList())

# Run the machine
ctr=0
while runMachine.getState() != 'qy' and runMachine.getState() != 'qn' and ctr < 1000:
    runMachine.updateMachine();
    print(runMachine.getState(),runMachine.getHead(),runMachine.getList())
    ctr += 1
print('- - -')

# Printout result
if (runMachine.getState() == 'qy'):
    print(initial_string,'is a palindrome! Steps:',ctr)
else:
    print(initial_string,'is NOT a palindrome! Steps:',ctr)