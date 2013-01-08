from datetime import date
from collections import Counter

CONSONANTS="bcdfghjklmnpqrstvwxyz"
VOWELS="aeiou"

all_nums={1,2,3,4,5,6,7,8,9,11,22,33}
#active=[1,4,8]
#thinking=[2,5,7]
#feeling=[3,6,9]

planes_of_expression={
	'e':['physical','creative'],
	'w':['physical','vacillating'],
	'd':['physical','grounded'],
	'm':['physical','grounded'],
	'a':['mental','creative'],
	'h':['mental','vacillating'],
	'j':['mental','vacillating'],
	'n':['mental','vacillating'],
	'p':['mental','vacillating'],
	'g':['mental','grounded'],
	'l':['mental','grounded'],
	'i':['emotional','creative'],
	'o':['emotional','creative'],
	'r':['emotional','creative'],
	'z':['emotional','creative'],
	'b':['emotional','vacillating'],
	's':['emotional','vacillating'],
	't':['emotional','vacillating'],
	'x':['emotional','vacillating'],
	'k':['intuitive','creative'],
	'f':['intuitive','vacillating'],
	'q':['intuitive','vacillating'],
	'u':['intuitive','vacillating'],
	'y':['intuitive','vacillating'],
	'c':['intuitive','grounded'],
	'v':['intuitive','grounded'],
}

onlyltrs=lambda x: x in CONSONANTS or x in VOWELS

#key is life path number
period_cycles={
		1:[[26,27],[53,54]],
		2:[[25,26],[52,53]],
		3:[[33,34],[60,61]],
		4:[[32,33],[59,60]],
		5:[[31,32],[58,59]],
		6:[[30,31],[57,58]],
		7:[[29,30],[56,57]],
		8:[[28,29],[55,56]],
		9:[[27,28],[54,55]],
}
period_cycles[11]=period_cycles[2]
period_cycles[22]=period_cycles[4]
period_cycles[33]=period_cycles[6]

def personal_date_nums(bdate,date):
	sum_digits(date.year+bdate.day+bdate.month)

def pinnacles(date):
	#gets the end of the first pinnacle, 
	#	second pinnacle, and third pinnacle
	#	and also the number associated with each pinnacle
	first=36-life_path_num(date)
	second=first+9
	third=second+9
	firstn=sum_digits(date.month+date.day)
	secondn=sum_digits(date.year+date.day)
	thirdn=sum_digits(firstn+secondn)
	fourthn=sum_digits(date.year+date.month)
	return (first,second,third),(firstn,secondn,thirdn,fourthn)

def challenges(date):
	first=sum_digits(abs(date.month-date.day),nomaster=True)
	second=sum_digits(abs(date.year-date.day),nomaster=True)
	third=abs(first-second)
	fourth=sum_digits(abs(date.year-date.month),nomaster=True)
	return first,second,third,fourth

def planes_of_expression(string):
	c1=Counter([planes_of_expression[c][0] for c in string if onlyltrs(c)])
	c2=Counter([planes_of_expression[c][1] for c in string if onlyltrs(c)])
	return c1.most_common()[0],c2.most_common()[0]

def hidden_passion(string,letter2value):
	c=Counter([letter2value[c] for c in string if onlyltrs(c)])
	return c.most_common()[0]

def subconscious_self(string,letter2value):
	nums=set()
	for c in string:
		nums.add(letter2value[c])
	return len(nums)

def possible_weaknesses(string,letter2value):
	nums=set()
	max_num=0
	for c in string:
		nums.add(letter2value[c])
		if letter2value[c] > max_num: max_num=letter2value[c]
	return set(range(1,max_num+1))-nums

def sum_digits(number,nomaster=False):
	if (nomaster and number//10 > 0) or (number not in all_nums):
		new_num=sum((int(i) for i in str(number)))
		return sum_digits(new_num)
	else:
		return number

def birth_day_num(date):
	return sum_digits(date.day)

def life_path_num(date):
	return sum_digits(date.month+date.year+date.day)

def character_num(string, letter2value):
	total=sum((letter2value[c] for c in filter(onlyltrs, string.lower())))
	return sum_digits(total)

def social_num(string, letter2value):
	chars=''.join(filter(lambda x: x in CONSONANTS, string.lower()))
	return character_num(chars, letter2value)

def heart_num(string, letter2value):
	chars=''.join(filter(lambda x:x in VOWELS, string.lower()))
	return character_num(chars, letter2value)

def parse_letter_value_map(fname):
	valdict={}
	with open(fname) as f:
		total=1
		for line in f:
			for c in line:
				valdict[c]=total
			total+=1
	return valdict

if __name__ == "__main__":
	import sys
	if len(sys.argv[1:]) < 2:
		print("Need a mapping file to process names", file=sys.stderr)
		exit(1)
	mappy=parse_letter_value_map(sys.argv[1])
	for string in sys.argv[2:]:
		print(string)
		#import pdb;pdb.set_trace()
		#minor versions of these are derived from name one is
		#	addressed by currently
		#rational thought num is day of birth+name
		#balance number uses one letter from each part of birth name
		#maturity number is life path num+character num
		#capstone is for first letter of first name
		#last letter of first name is for cornerstone
		#first vowel of first name is for heart's desire
		print("Character number:",character_num(string,mappy))
		print("Heart number:",heart_num(string,mappy))
		print("Social number:",social_num(string,mappy))
		print("---")
