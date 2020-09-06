from os import system, name
from time import sleep
from random import randint
import time, sys, random

#########################################################################
#                                                                       #
#                               CODEBREAKER                             #
#	Version: 0.0.1                                                      #
#	Author:  TJ Dugan                                                   #
#                                                                       #
#	Description: Simple CODEBREAKER Game That Produces a Random         #
#                3-Digit Numerical Code That The Player Must Crack!     #
#                The Following Hints Will Be Provided Per Guess:        #
#                        1. WRONG - None of the 3 Numbers Guessed Are   #
#                                   Correct.                            #
#                        2. CLOSE - Some of the Numbers are Correct,    #
#                                   But are in the Wrong Order.         #
#                        3. MATCH - Some of the Numbers are Correct     #
#                                   AND are in the Correct Order        #
#																		#
#				 Game is Over When All 3 Digits are Guessed Correctly   #
#                AND are in the Correct Order - Or if the User Enters   #
#                'Q'.                                                   #
#																		#
#########################################################################

## GLOBAL VARS ##
TEXT_COLOR = {
	"BLACK"           : "\u001b[30m", 
	"RED"             : "\u001b[31m", 
	"GREEN"           : "\u001b[32m",
	"YELLOW"          : "\u001b[33m", 
	"BLUE"            : "\u001b[34m", 
	"MAGENTA"         : "\u001b[35m", 
	"CYAN"            : "\u001b[36m", 
	"WHITE"           : "\u001b[37m", 
	"BRIGHT_BLACK"    : "\u001b[30;1m", 
	"BRIGHT_RED"      : "\u001b[31;1m", 
	"BRIGHT_GREEN"    : "\u001b[32;1m", 
	"BRIGHT_YELLOW"   : "\u001b[33;1m", 
	"BRIGHT_BLUE"     : "\u001b[34;1m", 
	"BRIGHT_MAGENTA"  : "\u001b[35;1m", 
	"BRIGHT_CYAN"     : "\u001b[36;1m", 
	"BRIGHT_WHITE"    : "\u001b[37;1m"
}
BACKGROUND_COLOR = {
	"BLACK"           : "\u001b[40m",
	"RED"             : "\u001b[41m",
	"GREEN"           : "\u001b[42m",
	"YELLOW"          : "\u001b[43m",
	"BLUE"            : "\u001b[44m",
	"MAGENTA"         : "\u001b[45m",
	"CYAN"            : "\u001b[46m",
	"WHITE"           : "\u001b[47m",
	"BRIGHT_BLACK"    : "\u001b[40;1m",
	"BRIGHT_RED"      : "\u001b[41;1m",
	"BRIGHT_GREEN"    : "\u001b[42;1m",
	"BRIGHT_YELLOW"   : "\u001b[43;1m",
	"BRIGHT_BLUE"     : "\u001b[44;1m",
	"BRIGHT_MAGENTA"  : "\u001b[45;1m",
	"BRIGHT_CYAN"     : "\u001b[46;1m",
	"BRIGHT_WHITE"    : "\u001b[47;1m"
}
RESET_TEXT_AND_BG      = '\u001b[0m'
MOVE_CURSOR_DOWN       = '\u001b[{'
BOLD_TEXT              = '\u001b[1m'
TERM_COLS              = 100
TERM_ROWS              = 40
HIGH_SCORES            = []
game_over = False
user_choice = ""
intro_inst_timeout = 3
guess_counter = 0

#################################################################################
#  ASCII ART LOGO
#################################################################################

AA   = [
	"  ____    ___    ____    _____ ",      
	" / ___|  / _ \  |  _ \  |___ / ",
	"| |     | | | | | | | |   |_ \ ",
	"| |___  | |_| | | |_| |  ___) | ",
	" \____|  \___/  |____/  |____/   _____ ",
	"                                |_____| ",
	" ____      _____   ____  _  _______ ____ ",
	"| __ ) _ _|___ /  / __ \| |/ /___ /|  _ \ ",
	"|  _ \| '__||_ \ / / _` | ' /  |_ \| |_) | ",
	"| |_) | |  ___) | | (_| | . \ ___) |  _ <  ",
	"|____/|_| |____/ \ \__,_|_|\_\____/|_| \_\ ",
	"                  \____/                   "
]
## FUNCTIONS ##

# Resize Terminal Window
def resize_term_window(columns, lines):
	# !!! Note: This Will Not Work On All Terminal Windows!!!!
	# Two Types of Commands Run Here, But Assume That
	# This Function Does Nothing. Just A Perk If It Does Work
	# Code From https://stackoverflow.com/questions/6418678/resize-the-terminal-with-python
	sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=lines, cols=columns))

	# Another method to achieve this
	system("mode con: cols=" + str(columns) + " lines=" + str(lines))

# Set Background Color
def set_background_color(color):
	print(color)

# Clear Screen
def clear_screen():
	# if windows os
	if name == 'nt':
		_ =system('cls')
	# if mac or linux
	else:
		_ = system('clear')

# Animate Text
def animate_text(text_to_animate, time_sleep=0.1):
	t = list(text_to_animate)
	animated = ''
	for i in range(len(t)):
		time.sleep(time_sleep)
		#animated += t[i]
		sys.stdout.write(t[i])
		sys.stdout.flush()
	print
	print(MOVE_CURSOR_DOWN)

# Animante Opening Logo Screen
def animate_logo():
	for i in range(len(AA)):
		animate_text(AA[i], 0.01)

# Animate Code Reveal on Win
def animate_win_reveal(codes, time_sleep=0.5):
	solved_codes=[]
	for x in range(len(codes)):
		if codes[x] < 10:
			solved_codes.append(" "+str(codes[x]))
		else:
			solved_codes.append(str(codes[x]))

	sys.stdout.write("##   ##   ##")

	#Animate 1st Num Reveal
	for i in range(codes[0]+1):
		time.sleep(time_sleep)
		if i < 10:
			sys.stdout.write(u"\u001b[1000D"+" "+str(i)+"   ##   ##")
			sys.stdout.flush()
		else:
			sys.stdout.write(u"\u001b[1000D"+str(i)+"   ##   ##")
	sleep(1)
	print

	#Animate 2nd Num Reveal
	for j in range(codes[1]+1):
		time.sleep(time_sleep)
		if j < 10:
			sys.stdout.write(u"\u001b[1000D"+solved_codes[0]+"   "+" "+str(j)+"   ##")
			sys.stdout.flush()
		else:
			sys.stdout.write(u"\u001b[1000D"+solved_codes[0]+"   "+str(j)+"   ##")
	sleep(1)
	print

	#Animate 3rd Num Reveal
	for k in range(codes[2]+1):
		time.sleep(time_sleep)
		if k < 10:
			sys.stdout.write(u"\u001b[1000D"+solved_codes[0]+"   "+solved_codes[1]+"    "+str(k))
			sys.stdout.flush()
		else:
			sys.stdout.write(u"\u001b[1000D"+solved_codes[0]+"   "+solved_codes[1]+"   "+str(k))
	sleep(1)
	print


# Show Welcome Screen
def welcome_screen():
	print(BOLD_TEXT)
	print(TEXT_COLOR["RED"])
	animate_logo()
	print(TEXT_COLOR["WHITE"])
	sleep(3)
	print("Press 1 to Start")
	print("Press 2 for Instructions")
	print("Press 3 for Fastest Times")
	print("Press Q at at any time to Quit")
	sleep(0.5)

# Parse User Input - Simple Validation
def parse_user_guess(guesses):
	validated_ints = guesses
	try:
		for i in range(len(guesses)):
			validated_ints[i] = int(guesses[i])
			if len(validated_ints) < 3:
				for j in range(len(validated_ints)):
					validated_ints[j] = 11
				for x in range(len(validated_ints), 3):
					validated_ints.append(11)
	except:
		validated_ints = [11, 11, 11]

	#print(validated_ints)
	return validated_ints

# Rules
def display_rules():
	print('')
	print('The rules of the game are simple')
	print('')
	sleep(intro_inst_timeout)
	print('The computer generates a three number code')
	print('')
	sleep(intro_inst_timeout)
	print('Each number is between 0 and 10, with 0 and 10 included')
	print('')
	sleep(intro_inst_timeout)
	print('The numbers do not repeat. Your job is to crack the code.')
	print('')
	sleep(intro_inst_timeout)
	print('You will enter your guess by typing the integer values seperated by a space.')
	print('Example: '+ TEXT_COLOR['BRIGHT_BLACK'] + '3 7 10')
	print('')
	sleep(intro_inst_timeout)
	print(TEXT_COLOR["WHITE"] + "The guess MUST be enterd in this format. No leading zeros and no double spaces")
	print('')
	sleep(intro_inst_timeout)
	print("If none of the numbers are part of the code, the computer will ")
	print("alert you with the word " + TEXT_COLOR["BRIGHT_BLACK"] + "WRONG")
	print('')
	sleep(intro_inst_timeout)
	print(TEXT_COLOR["WHITE"] + "If any of the numbers are right, but none are in the right order, ")
	print("you will be alerted by the word " + TEXT_COLOR["BRIGHT_BLACK"] + "CLOSE")
	print('')
	sleep(intro_inst_timeout)
	print(TEXT_COLOR["WHITE"] + "If you have any numbers right AND in the correct order, ")
	print("you will be alerted by the word " + TEXT_COLOR["BRIGHT_BLACK"] + "MATCH")
	print('')
	sleep(intro_inst_timeout)
	print(TEXT_COLOR["WHITE"] + "The game is over once you guess all the numbers in the right order")
	print("Enter Q at any time to quit the game")

	inp = input("Hit Enter to start the game")
	clear_screen()
	animate_text("Ready?...", 0.35)
	start_game()

# Calculate Skill Level
def calc_skill_level():
	global guess_counter
	sk = ""

	if guess_counter == 1:
		sk = "Lets just chalk this one up to luck"
	elif guess_counter > 1 and guess_counter < 4:
		sk = "Try doing that again 🤔"
	elif guess_counter > 3 and guess_counter < 7:
		sk = "You are a master codebreaker!!"
	elif guess_counter > 6 and guess_counter < 10:
		sk = "Wow! You are a heckuva codebreaker!"
	elif guess_counter > 9 and guess_counter < 16:
		sk = "You've got skills! Keep practicing."
	elif guess_counter > 15 and guess_counter < 21:
		sk = "Not bad for an amateur."
	else:
		sk = "Keep trying, or you'll never make it as a codebreaker 😔"
	return sk


# Display High Scores
def display_high_scores(scores):
	clear_screen()
	print(TEXT_COLOR["BLACK"] + "HIGH SCORES:")
	print("--------------------------------")
	print(TEXT_COLOR["WHITE"])
	if len(scores)>0:
		for i in range(len(scores)):
			num = i + 1
			name = str(scores[i][0])
			scr  = str(scores[i][1])
			print("{:>2}: {:10} - {:>3} Attempts".format(num, name, scr))
			#print(str(num) + ": " + str(scores[i][0]) + "  -  " + str(scores[i][1]) + " Attempts")
	else:
		print("No Scores Yet.")
	print("")
	print("")
	usr_input = input("Press Any Key To Return To Game")
	main_menu()

# Record Time
def write_hs_list_to_file(new_list):
	final_list = []

	#limit list to top 10 scores
	if len(new_list) > 10:
		for i in range(10):
			final_list.append(new_list[i])

	#if less than 10 scores exist record all
	else:
		for j in range(len(new_list)):
			final_list.append(new_list[j])

	#Save to file
	try:
		with open("High_Scores.txt", 'w') as filehandle:
			for listitem in final_list:
				filehandle.write(str(listitem[0]) + " " + str(listitem[1]) + "\n")
	except:
		print("Error Saving File")
	finally:
		filehandle.close()


# Check To See If User's Score is a New High Score
# If it is, Record
def check_for_new_high_score(curr_highs, usr_score):
	new_hs_list = []
	new_score_recorded = False
	is_top_score = False
	usr_name = ""
	
	#if list is not empty ....
	if len(curr_highs) >= 1:
		for i in range(len(curr_highs)):
			if int(usr_score) < int(curr_highs[i][1]) and new_score_recorded == False:
				if i == 0:
					is_top_score = True
				usr_name = get_new_hs_usr_name(is_top_score)
				new_hs_list.append([usr_name, str(usr_score)])
				new_hs_list.append(curr_highs[i])
				new_score_recorded = True
			else:
				new_hs_list.append(curr_highs[i])

		#if user score is not higher than recorded scores
		#check to see if list has 10 scores. If not, add user score to the end
		if len(curr_highs) < 10 and new_score_recorded == False:
			usr_name = get_new_hs_usr_name(is_top_score)
			new_hs_list.append([usr_name, str(usr_score)])
			new_score_recorded = True

	#if list is empty, user has new high score to record
	else:
		is_top_score = True
		usr_name = get_new_hs_usr_name(is_top_score)
		new_hs_list.append([usr_name, str(usr_score)])
		new_score_recorded = True

	if new_score_recorded == True:
		write_hs_list_to_file(new_hs_list)

# New High Score!
def get_new_hs_usr_name(is_top_score):
	usr_name = ""
	if is_top_score == True:
		clear_screen()
		animate_text("NEW TOP SCORE!!!!!!!!!!!!!!!!!")
		print("Congratulations!!!! You Have the New Top Score")
		usr_name = input("Please Enter Your Name For The Leaderboard:  ")
	else:
		print("Congratulations!!!! You Have Made It On To The Leaderboard")
		usr_name = input("Please Enter Your Name For The Leaderboard:  ")

	return usr_name

# File Handler
def file_handler(file_name, mode):
	if mode == "read":
		text_list = []
		x = []
		try:
			text_file = open(file_name, 'r')
			text_list = text_file.readlines()
			text_file.close()
		except:
			text_file = open(file_name, 'w')
			text_file.close()
	if len(text_list) > 0:
		for i in range(len(text_list)):
			x.append(text_list[i].split())
	return x


# User Wins
def user_wins(codes):
	global guess_counter
	skill_level = calc_skill_level()
	#print("congrats....")
	#sleep(2)
	clear_screen()
	animate_win_reveal(codes)

	print(MOVE_CURSOR_DOWN + TEXT_COLOR["WHITE"])
	print("Congratulations - You Cracked the Code!!")
	print("You were able to crack the code in " + str(guess_counter) + " tries")
	print(skill_level)

	check_for_new_high_score(HIGH_SCORES, guess_counter)

	ui = input("Press Enter to Exit")
	quit_game()

# Quick Rules
def quick_rules():
	print('')
	print('Enter your guess by typing the integer values seperated by a space.')
	print('Example: '+ TEXT_COLOR['BRIGHT_BLACK'] + '3 7 10')
	print('')
	sleep(intro_inst_timeout)
	print(TEXT_COLOR["WHITE"] + "The guess MUST be enterd in this format. No leading zeros and no double spaces")
	print('')
	print("Enter Q at any time to quit the game")

	animate_text("Ready?...", 0.65)


# User Quits
def quit_game():
	print("Thanks For Playing. Goodbye.")
	sleep(3)
	print(RESET_TEXT_AND_BG)
	clear_screen()

# Evaluate Guess
def evaluate_guess(codes):
	global game_over
	guesses = []
	user_choice = input(TEXT_COLOR["WHITE"] + "Please enter your guesses seperated by a space: " + TEXT_COLOR["BRIGHT_BLACK"])

	if user_choice == 'Q' or user_choice == 'q':
		game_over = True
		quit_game()
	else:
		guesses = user_choice.split(" ")

	# Convert User Input Into 3 Integers
	guesses = parse_user_guess(guesses)
	if guesses[0] == 11 and guesses[1] == 11 and guesses[2] == 11:
		print("Please enter three integers between 0 & 10 inclusive, seperated by a comma.")
		return False

	#Check For Win
	if guesses[0] == codes[0] and guesses[1] == codes[1] and guesses[2] == codes[2]:
		return True
	#Check For Match
	if guesses[0] == codes[0] or guesses[1] == codes[1] or guesses[2] == codes[2]:
		print(BACKGROUND_COLOR["WHITE"] + TEXT_COLOR["BRIGHT_BLUE"] + "MATCH!"+BACKGROUND_COLOR["CYAN"])
		print(BACKGROUND_COLOR["CYAN"] + TEXT_COLOR["WHITE"])
		return False
	#Check if user has a correct number out or order
	for x in range(len(codes)):
		for j in range(len(guesses)):
			if codes[x] == guesses[j]:
				print(BACKGROUND_COLOR["WHITE"] + TEXT_COLOR["BRIGHT_BLUE"] + "CLOSE!" + BACKGROUND_COLOR["CYAN"])
				print(BACKGROUND_COLOR["CYAN"] + TEXT_COLOR["WHITE"])
				return False
	print(BACKGROUND_COLOR["WHITE"] + TEXT_COLOR["BRIGHT_RED"] + "WRONG!" + BACKGROUND_COLOR["CYAN"])
	print(BACKGROUND_COLOR["CYAN"] + TEXT_COLOR["WHITE"] + "Please Try Again.")
	return False



# Start Game
def start_game():
	global game_over, guess_counter
	
	quick_rules()
	clear_screen()
	
	#print(codes)
	codes = gen_random_code()
	print("The computer has generated the code:")
	print("                           #   #   #")
	#Run the main game loop until user wins
	while not game_over:
		#print(guess_counter)
		game_over = evaluate_guess(codes)
		guess_counter += 1
	#guess_counter += 1
	print(guess_counter)
	user_wins(codes)

# Generate Random Number
def gen_random_code(size=3):
	choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	numbers = []

	print("Generating Code")
	animate_text("###############################", 0.25)

	#Shuffle the numbers in choices
	random.shuffle(choices)

	for i in range(size):
		numbers.append(choices.pop())

	return numbers

# Check Menu Options to Make Sure Entered Value is Valic
def get_valid_menu_option():
	uc = input("Make a selection:  ")
	is_valid_input = False

	while is_valid_input == False:
		if uc != "1" and uc != "2" and uc != "3" and uc != "q" and uc != "Q":
			print("Invalid input.")
			uc = input("Please enter options 1, 2, 3, or q from the above menu: ")
		else:
			is_valid_input = True

	return uc

# MAIN MENU
def main_menu():
	resize_term_window(TERM_COLS, TERM_ROWS)
	set_background_color(BACKGROUND_COLOR["CYAN"])
	valid_input = False
	clear_screen()
	welcome_screen()

	user_choice = get_valid_menu_option()

	if user_choice == "1":
		start_game()
	elif user_choice == "2":
		display_rules()
	elif user_choice == "3":
		display_high_scores(HIGH_SCORES)
	elif user_choice == "Q" or user_choice == "q":
		quit_game()
	else:
		user_choice = "Sorry, invalid input. Please make a selaction: "

## MAIN ##


HIGH_SCORES = file_handler("High_Scores.txt", "read")
main_menu()

