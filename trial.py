
next_location_in_instruction_module=0
next_location_in_data_module=16


table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
    }
for i in range(16):
    
    table["R"+str(i)]=i




class parser:




    def __init__(self,input_file):
        
        with open(input_file,"r") as f:
            self.lines=[l.split("//")[0].strip() for l in f.readlines() if len(l.split("//")[0].strip())]

            self.command_number=-1
            self.current_command=""
    
    def is_there_any_command(self):
        return (self.command_number+1)<len(self.lines)
    
    def next_instruction(self):
         
        if self.is_there_any_command():
            self.command_number+=1
            self.current_command=self.lines[self.command_number]
    
    def command_type(self):
         
        if len(self.current_command) and self.current_command[0]=='@':
            return "A"+self.current_command[1::]
        elif len(self.current_command) and self.current_command[0]=='(':
            return "L"+self.current_command[1:len(self.current_command)-1:]
         
        else:
            return "C"
    
    def symbol(self):

         
        if self.command_type()[0]=='A':
            return self.command_type()[1::]
    
    def dest(self):

        if self.command_type()=="C":
            ok=0
            s=""
            cnt=0
            for ch in self.current_command:
                cnt+=1
                if ch =='=':
                    self.current_command=self.current_command[cnt::]
                    return s.strip()
                
                s+=ch
                
            return "null"
            

    def comp(self):

        if self.command_type()=='C':
            self.current_command+=";"
            s=""
            cnt=0
            for ch in self.current_command:
                cnt+=1
                if ch==';':
                    self.current_command=self.current_command[cnt:len(self.current_command)-1:]
                    return s.strip()
                s+=ch 
    
    def jump(self):

        if self.command_type()=='C':
            return self.current_command.strip() if len(self.current_command) else "null"
        
    
    def detect_lapels(self):
        """detect labels such as (Xxx) and add it to the table 
        and it will point to the next instruction in the instruction memory (used with jmp)"""
        global next_location_in_instruction_module

        for l in self.lines:

            if l[0]=='(':
                table[l[1:-1]]=next_location_in_instruction_module
            
            else:
                next_location_in_instruction_module+=1



class code :
    """111 a cccc ccdd djjj"""


    def __init__(self):

        with open("comp_table.txt","r") as f:
            self.comp_table={l.split()[0]:l.split()[1] for l in f.readlines()}

        with open("dest_table.txt","r") as f:
            self.dest_table={l.split()[0]:l.split()[1] for l in f.readlines()}

        with open("jmp.txt","r") as f:
            self.jmp_table={l.split()[0]:l.split()[1] for l in f.readlines()}

    

    def create_is(self,obj_parser):

        while obj_parser.is_there_any_command():
            obj_parser.next_instruction()

            if obj_parser.command_type()[0]=='A':
                operand=obj_parser.command_type()[1:]
                binary_version=""
                if operand[0].isalpha():

                    """if it symbol so there are 2 options (1-->it was predefined lapel) 
                    (2---> first ocuuerence of variable)
                    """
                    global next_location_in_data_module
                    if table.get(operand,-1)==-1: 
                        """not in the table and it will take the next address from the data module"""
                        table[operand]=next_location_in_data_module
                        binary_version=bin(next_location_in_data_module)[2:].zfill(16)
                        next_location_in_data_module+=1
                    
                    else:
                        """predefined symbol and it map to location of specific instruction"""
                        binary_version=bin(table[operand])[2:].zfill(16)
                
                else:

                    """immediate value"""
                    binary_version=bin(int(operand))[2:].zfill(16)
                with open("out.hack","a") as f:
                    f.write(binary_version+"\n")
                print(binary_version,end="")
                if obj_parser.is_there_any_command():
                   
                    print()


            
            elif obj_parser.command_type()=='C':
                
                
                dest=self.dest_table[obj_parser.dest()]
                comp=self.comp_table[obj_parser.comp()]
                jmp=self.jmp_table[obj_parser.jump()]
                with open("out.hack","a") as f:
                    f.write(f"111{comp}{dest}{jmp}"+"\n")
                print(f"111{comp}{dest}{jmp}",end="")

                if obj_parser.is_there_any_command():
                    print()



parsing=parser("tst.txt")



parsing.detect_lapels()
code=code()

code.create_is(parsing)



