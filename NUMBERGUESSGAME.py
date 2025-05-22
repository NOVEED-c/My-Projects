#required modules
import mysql.connector as mysql#Backend
import pickle#Used to fetch dares
import random#Used in Game
mydb=mysql.connect(host='localhost',user='root',password='123')#You may enter your specs
mycursor=mydb.cursor()
try:#Logic to create database in mysql
    mycursor.execute('use game')
except:
    mycursor.execute('create database game')#to create required database
    mycursor.execute('use game')
try:#Logic to create table 
    mycursor.execute('desc winner')
    data=mycursor.fetchall()#To avoid unread result error//an important concept of cursor object to understand
except:
    mycursor.execute('create table winner(ID int,Name varchar(30),Score int,Chances int,Ratio decimal(10,5))')#to create required table
print('******************************************NUMBER GUESSING GAME**********************************************')
def intro():
    print('\t\t\t\t********NUMBER GUESSING GAME*********')#General Instruction kindly follow
    print('GENERAL INSTRUCTIONS BEFORE YOU PLAY:')
    print('->It is a fun Number Guessing game where you have to guess the right number between 1-100 in 5 attempts')
    print('->If you guessed correct you scored else...')
    print('->You will get prior hints based on our guesses')
    print('->If you didnot guessed right you will get a dare when all attempts are lost')
    print('->If you gave any other entry except natural numbers between 1-100 you will lose an attempt')
    print('->Each time you will Guess right your score will increase by 1')
    print('->Your final score will display when you terminate the game')
    print('->The person having score to chance ratio>=0.4 for Chances>=4 will win the game')
    print('Lets get started\nALL THE BEST!!\n','-'*100,'\n')
    
def Numguess():#Main Game
    n=random.randint(1,100)#logic behind the number guessed by computer
    print('Now your turn to guess what number computer has taken between 1-100')
    score=0
    i=0
    attempt=5
    win=0
    while i<attempt:#game body
        print('**Guess the number**')
        ch=int(input("What's your Guess :"))
        if ch==n:
            win=1
            score=score+1
            break
        elif ch not in range(1,101):
            print('Entry Valid between 1-100 only\n')
            print('Remaining Attempts:',4-i)
            print()
        else:
            diff=n-ch
            if diff>0:
                if diff>=20:
                    if i!=4:
                        print('Wrong Guess! Try Again...But.\n')
                        print('-->You Guessed Too Low')
                        print('-->Guess quite a large number...\n')
                    else:
                        print('\n----------GAME OVER----------')
                elif diff<20 and diff>=10:
                    if i!=4:
                        print('Wrong Guess! Try Again...But.\n')
                        print('-->You are little close....\n')
                    else:
                        print('----------GAME OVER----------')
                elif diff<10 and diff>=6:
                    if i!=4:
                        print('Wrong Guess! Try Again...But.\n')
                        print('-->Your are really close!!!')
                    else:
                        print('\n----------GAME OVER----------')
                elif diff<6:
                    if i!=4:
                        print('Wrong Guess! Try Again...But.\n')
                        print('-->You are very very close!!!!')
                        print('-->Think a little higher!!!\n')
                    else:
                        print('\n----------GAME OVER----------')
            elif diff<0:
                diff=ch-n
                if diff>=20:
                    if i!=4:
                        print('Wrong Guess! Try Again...But.\n')
                        print('-->You Guessed Too High')
                        print('-->Guess quite a smaller number...\n')
                    else:
                        print('\n----------GAME OVER----------')
                elif diff<20 and diff>=10:
                    if i!=4:
                        print('Wrong Guess! Try Again...But.\n')
                        print('-->You are little close....\n')
                    else:
                        print('\n----------GAME OVER----------')
                elif diff<10 and diff>=6:
                    if i!=4:
                        print('-->Wrong Guess! Try Again...But.\n')
                        print('-->Your are really close!!!\n')
                    else:
                        print('\n----------GAME OVER----------')
                elif diff<6:
                    if i!=4:
                        print('Wrong Guess! Try Again...But.\n')
                        print('-->You are very very close!!!!')
                        print('-->Think little lower!!!\n')
                    else:
                        print('\n----------GAME OVER----------')
            print('Remaining attempts:',4-i)
            print()
        i+=1
    l=[]
    try:
        f=open('Dare.dat','rb')
        while True:
            dare=pickle.load(f)#To get dares from dare.dat
            l.append(dare)
    except EOFError:
        f.close()
    d=random.randrange(0,len(l))
    if win==0:
        print()
        print('You lost the game')
        print('The required number was:',n)
        print()
        print('You lost..Get ready for the dare')
        print('And your dare is---->\n')
        print(l[d].upper())
        print('********************************************************************************************\n')
    elif win==1:
        print('Congratulations!!!!!!!')
        print('You Guessed it Right! now take 10 rupees from your brother......LOL')#Reward
        print()
    return(score)

def newgame():#For a new player to create a new id
    print()
    scre=0
    chance=0
    Id=random.randint(1,1000)
    print('Your Player ID is:',Id)
    name=input('Enter your name:')
    print('Hello',name,'Welcome to our Number Guessing Game')
    print("To Start the game TYPE: 'S'\nTo Exit the game TYPE: 'E'\n")
    s=input('TYPE YOUR RESPONSE:')
    if s.upper()=='S':
        print()
        intro()
        choice='yes'
        while choice.upper()=='YES':
            chance+=1
            scre+=Numguess()#To sum up your scores
            choice=input('Type Yes to Play Again\nType No to terminate\nWant To Play Again?\nTYPE YOUR RESPONSE HERE:')
            print()
            if choice.upper()=='NO':
                print('Total Chances Played:',chance)
                print('Your Score is:',scre)
                ratio=scre/chance
                print('TERMINATED')
                mycursor.execute("insert into winner values({},'{}',{},{},{})".format(Id,name,scre,chance,ratio))
                mydb.commit()#To Save player progress
                break
            elif choice.upper()!='YES':
                print('INVALID RESPONSE')
                print('YOUR DATA CANNOT BE SAVED')
    elif s.upper()=='E':
        print('You chose to Exit')
    else:
        print('Invalid response')

def Continue():#For Pre-existing player to continue his/her progress, requires player id
    print()
    ID=int(input('Enter your Player ID:'))
    mycursor.execute('select * from winner')
    data=mycursor.fetchall()
    Chance=0
    Score=0
    found=0
    for i in data:
        if i[0]==ID:
            found=1
            print('Hello',i[1],'!!! Welcome back to our Number Guessing Game........')
            print("To Start the game TYPE: 'S'\nTo Exit the game TYPE: 'E'\n")
            s=input('TYPE YOUR RESPONSE:')
            if s.upper()=='S':
                print()
                intro()
                choice='yes'
                while choice.upper()=='YES':
                    Chance+=1
                    Score+=Numguess()
                    choice=input('Type Yes to Play Again\nType No to terminate\nWant To Play Again?\nTYPE YOUR RESPONSE HERE:')
                    print()
                    if choice.upper()=='NO':
                        print('Total Chances Played:',Chance)
                        print('Your Score is:',Score)
                        Ratio=Score/Chance
                        print('TERMINATED')
                        mycursor.execute("update winner set score=score+{},chances=chances+{},ratio=ratio+{} where id={}".format(Score,Chance,Ratio,ID))
                        mydb.commit()
                        break
            elif s.upper()=='E':
                 print('You chose to Exit')
            else:
                 print('Invalid response')
        else:
            continue
    if found==0:
        print('PLAYER NOT FOUND')

def stats():#check your/all players stats in game
    mycursor.execute('select * from winner')
    Data=mycursor.fetchall()
    if Data!=[]:#To implement handling situation when no records present in winner table
        print('TYPE (MY) TO CHECK YOUR STATS')
        print('TYPE (ALL) TO CHECK OVERALL STATS')
        re=input('Enter your response:')
        if re.upper()=='MY':
            myid=int(input('Enter your Player ID:'))
            search=0
            mycursor.execute('select * from winner')
            data=mycursor.fetchall()
            for i in data:
                if i[0]==myid:
                    search=1
                    break
            if search==0:#linear search method
                print('PLAYER RECORD WITH GIVEN ID DOESNOT EXIST')
            elif search==1:
                mycursor.execute('select * from winner where id={}'.format(myid))#Extract required data
                for i in mycursor:
                    print()
                    print('**************************YOUR STATS***************************')
                    print('PlayerID:',i[0],'\nPlayer Name:',i[1],'\nScore:',i[2],'\nChances Played:',i[3],'\nS/C Ratio:',i[4])
        elif re.upper()=='ALL':
            mycursor.execute('select * from winner order by score desc')
            data=mycursor.fetchall()
            print('PlayerID     ','Player Name   ','Score    ','Chances     ','Score:Chances')
            for i in data:
                print(i[0],'           ',i[1],'         ',i[2],'\t',i[3],'\t\t',i[4])
    else:
        print('***********NO DATA PRESENT CURRENTLY***********')#Message displayed for empty table
def delitem():
    mycursor.execute('select * from winner')
    Data=mycursor.fetchall()
    if Data!=[]:
        print()
        print('DO YOU WANT TO DELETE YOUR DATA')
        y=input('->TYPE YES TO CONFIRM\n->TYPE NO TO EXIT\nTYPE YOUR RESONSE:')
        print()
        if y.upper()=='YES':
            delid=int(input('Enter your Player ID:'))
            found=0
            mycursor.execute('select * from winner where id={}'.format(delid))
            data=mycursor.fetchone()
            if data!=None:
                mycursor.execute('delete from winner where id={}'.format(delid))
                mydb.commit()
                print('***********PLAYER DATA HAS BEEN DELETED SUCCESSFULLY***********')
            else:
                print('********PLAYER NOT FOUND********')
        elif y.upper()=='NO':
            print('REVERTED')
        else:
            print('-----INVALID RESPONSE-----')
    else:
        print('***********NO DATA PRESENT CURRENTLY***********')

def winner():#Declares winner
    print()
    mycursor.execute('select * from winner')
    Data=mycursor.fetchall()
    winner=[]
    cont=[]
    if Data!=[] and len(Data)<=1:
        print('*************************Minimum two players required to declare winner***********************')
    elif Data!=[] and len(Data)>1:
        mycursor.execute('select * from winner')
        data=mycursor.fetchall()
        #win=0
        for i in data:
            ratio=i[2]/i[3]
            if ratio>=0.4 and i[3]>=4:
                winner.append([i[1],ratio])
            elif ratio>=0.4 and i[3]<4:
                cont.append([i[1],ratio])
        for blank in winner:
            if blank==[]:
                winner.remove(blank)
        for blank in cont:
            if blank==[]:
                cont.remove(blank)
        while True:
            if len(winner)==0 and len(cont)==0:
                print('-----------Nobody has won the game still! Play more and enjoy-----------')
                break
            elif len(winner)!=0 and len(winner)==1:
                print('The Grand Winner of the Game is:',winner[0][0],'with Score:Chances ratio:',winner[0][1])
                print()
                break
            elif len(winner)>1:
                mycursor.execute('Select name,ratio from winner where ratio=(select max(ratio) from winner)')
                win_data=mycursor.fetchall()
                if len(win_data)==1:
                    print('The Grand Winner of the Game is:',win_data[0][0],'with Score:Chances ratio:',win_data[0][1])
                    break
                else:
                    print('Following players have same ratio>=0.4:')
                    print('Name\t\t','Ratio')
                    for i in win_data:
                        print(i[0],'\t\t',i[1])
                    print('Either Toss, Rock paper Scissors or play more to compete and win!!!!!')    
                    break
            elif len(cont)==0:
                continue
            elif len(cont)>0:
                print('Winner cannot be declared! But player with ratio>=0.4 but chances<4')
                print()
                print('Name\t\t','Ratio')
                for pname in cont:
                    print(pname[0],'\t\t',pname[1])
                print('\n----------Hang On and play more! One may win soon!!!!!-----------')
                break
    else:
        print('***********NO DATA PRESENT CURRENTLY***********')                
while True:
    print()
    print()
    print('An IMPORTANT NOTE: Kindly enter your choices as mentioned')
    print('*********************************************MAIN MENU*********************************************')
    print('->TYPE 1: NEW GAME')
    print('->TYPE 2: CONTINUE')
    print('->TYPE 3: STATS')
    print('->TYPE 4: DELETE MY ID')
    print('->TYPE 5: DECLARE WINNER')
    print('->TYPE 6: EXIT')
    resp=int(input('Enter your response:'))
    print()
    if resp==1:
        newgame()
    elif resp==2:
        Continue()
    elif resp==3:
        stats()
    elif resp==4:
        delitem()
    elif resp==5:
        winner()
    elif resp==6:
        print('THANKS FOR PLAYING!!!!\nYOU CHOSE TO EXIT.....')
        break
    else:
        print('Invalid Response')
#Changes as per convenience are allowed but make sure to understand sequence of code execution or Algorithm to avoid exceptions
        
        
            
