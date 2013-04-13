from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
from collections import Counter,UserDict
from collections import OrderedDict as od
import re

# sites I looked at for applicable calculations
#http://stackoverflow.com/questions/3387691/python-how-to-perfectly-override-a-dict
#http://www.decoz.com/numerology-Course-21a.htm

CONSONANTS=re.compile("[bcdfghjklmnpqrstvwxyz]",re.I)
VOWELS=re.compile("[aeiou]",re.I)

MASTER_NUMS=frozenset([11,22,33])
PROBLM_NUMS=frozenset([13,14,16,19]) # http://www.decoz.com/Karmic_Debt.htm
ALLSPECIAL=MASTER_NUMS.union(PROBLM_NUMS)
#active=[1,4,8]
#thinking=[2,5,7]
#feeling=[3,6,9]

class TransformedDict(UserDict):
	"""A dictionary which applies an arbitrary key-altering function before accessing the keys"""
	def __init__(self, *args, **kwargs):
		self.data = dict()
		self.update(dict(*args, **kwargs)) # use the free update to set keys
	def __getitem__(self, key):
		return self.data[self.__keytransform__(key)]
	def __setitem__(self, key, value):
		self.data[self.__keytransform__(key)] = value
	def __delitem__(self, key):
		del self.data[self.__keytransform__(key)]
	def __iter__(self):
		return iter(self.store)
	def __len__(self):
		return len(self.store)
	def __keytransform__(self, key):
		return key

class LowerTransformedDict(TransformedDict):
	def __keytransform__(self, key):
		if isinstance(key, str):
			return key.lower()
		return key

planes_of_expression=LowerTransformedDict({
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
})

onlyvwls=lambda x: VOWELS.match(x)
onlycnsts=lambda x: CONSONANTS.match(x)
onlyltrs=lambda x: onlyvwls(x) or onlycnsts(x)


#key is life path number
PERIOD_CYCLES={
		1:[[26,27],[53,54],[float('inf'),float('inf')]],
		2:[[25,26],[52,53],[float('inf'),float('inf')]],
		3:[[33,34],[60,61],[float('inf'),float('inf')]],
		4:[[32,33],[59,60],[float('inf'),float('inf')]],
		5:[[31,32],[58,59],[float('inf'),float('inf')]],
		6:[[30,31],[57,58],[float('inf'),float('inf')]],
		7:[[29,30],[56,57],[float('inf'),float('inf')]],
		8:[[28,29],[55,56],[float('inf'),float('inf')]],
		9:[[27,28],[54,55],[float('inf'),float('inf')]],
}
PERIOD_CYCLES[11]=PERIOD_CYCLES[2]
PERIOD_CYCLES[22]=PERIOD_CYCLES[4]
PERIOD_CYCLES[33]=PERIOD_CYCLES[6]

def daterange(start_date, end_date):
	for n in range(int((end_date - start_date).days)):
		yield start_date + timedelta(n)

sumdcache={}
def sum_digits(number, special=frozenset()):
	if sumdcache.get((number,special)) is not None:
		return sumdcache.get((number,special))
	if number > 9 and not number in special:
		new_num=sum((int(i) for i in str(number)))
		return sum_digits(new_num, special=special)
	else:
		return number

class LetterMapping(LowerTransformedDict):
	def __init__(self, fname):
		super().__init__()
		self.valid_nums=set()
		with open(fname) as f:
			total=1
			for line in f:
				self.valid_nums.add(total)
				for c in line:
					self.data[c]=total
				total+=1
			else:
				self.max_num=total

class NumerologyReport:
	def __init__(self, first_name, last_name, birth_date, 
				l2nmap, middle_name=''):
		#properties for calculations
		self.fname=first_name
		self.mname=middle_name
		self.lname=last_name
		self.bdate=birth_date
		self.l2nmap=l2nmap
		self.nicknames=[]

		#properties that are cached
		self._pdate_nums_cache={}
		self._pinnacle_ends=None
		self._pinnacle_nums=None
		self._challenge_nums=None
		self._eplane=None
		self._eplane2=None
		self._eplane3=None
		self._eplane4=None
		self._hidden_passion=None
		self._weaknesses=None
		self._subconscious=None
		self._pcycle=None
		self._scycle=None
		self._mcycle=None

	def export(self, fname, sdate, edate, mapname):
		title=("Report for {}, born on {} and using"
			" the {} letter to number mapping.").format(self.full_name,self.bdate,mapname)
		with open(fname,'w') as f:
			lines=[title]
			lines.append("Basics:")
			lines.append("\tLife Path: {:d}".format(self.life_path_num))
			lines.append("\tBirthday: {:d}".format(self.birth_day_num))
			lines.append("\tCharacter: {:d}".format(self.character_num))
			lines.append("\tSocial: {:d}".format(self.social_num))
			lines.append("\tHeart's Desire: {:d}".format(self.heart_num))
			lines.append("\tRational Thought: {:d}".format(self.rational_thought_num))
			lines.append("\tBalance: {:d}".format(self.balance_num))
			lines.append("\tUnderlying Goal: {:d}".format(self.underlying_goal_num))
			lines.append("\tFirst Vowel: {}".format(self.first_vowel_num))
			lines.append("\tCapstone: {}".format(self.capstone_num))
			lines.append("\tCornerstone: {}".format(self.cornerstone_num))

			lines.append("Strengths and Weaknesses:")
			lines.append("\tHidden Passion: {:d}".format(self.hidden_passion))
			lines.append("\tSubconscious Self: {:d}".format(self.subconscious_self))
			lines.append("\tPossible weaknesses: {}".format(self.possible_weaknesses))
			area,area2,totals,totals2=self.planes_of_expression
			lines.append("\tMost prominent planes of expression: {}, {}".format(area,area2))
			lines.append("\tNumbers for planes of expression:")
			lines.append("\tPlane      |Number")
			lines.append("\t-----------|------")
			for n in totals.keys():
				if n == self._eplane:
					lines.append("\t{:11}|{:6}".format(n,"*{:d}".format(totals[n])))
				else:
					lines.append("\t{:11}|{:6d}".format(n,totals[n]))
			for n in totals2.keys():
				if n == self._eplane2:
					lines.append("\t{:11}|{:6}".format(n,"*{:d}".format(totals2[n])))
				else:
					lines.append("\t{:11}|{:6d}".format(n,totals2[n]))

			lines.append("Life Overview:")
			lines.append("\tChallenges: {}".format(self.challenge_nums))
			lines.append("\tPinnacles:")
			lines.append("\tEnd Age|Number")
			lines.append("\t-------|------")
			for endage,pinnum in zip(*self.pinnacles):
				lines.append("\t{:7.0f}|{:6d}".format(endage,pinnum))
			lines.append("\tLife Cycles:")
			lines.append("\t(The first cycle's effects are based on your month.")
			lines.append("\tThe second cycle's effects are based on your day of birth.")
			lines.append("\tThe third cycle's effects are based on your year of birth.)")
			lines.append("\tEnd Age|Transition Age")
			lines.append("\t-------|--------------")
			for endage,transage in self.life_cycles:
				lines.append("\t{:7.0f}|{:14.0f}".format(endage,transage))
			if None not in (sdate,edate):
				lines.append("Life Snapshot for {} to {}:".format(sdate,edate))
				lines.append(("\tDate      |Physical|Mental|Spiritual|Essence"
							  "|Personal Year|Personal Month|Personal Day"))
				lines.append(("\t----------|--------|------|---------|-------"
							  "|-------------|--------------|------------"))
				for d in daterange(sdate,edate+timedelta(1)):
					transits=self.transit_cycle_num(d)
					pdatenums=self.personal_date_nums(d)
					stats=[d.strftime("%Y-%m-%d")]
					stats.extend(transits)
					stats.extend(pdatenums.values())
					lines.append("\t{:10}|{:8}|{:6}|{:9}|{:7d}|{:13d}|{:14d}|{:12d}".format(*stats))
			f.write('\n'.join(lines))

	def transit_cycle_num(self, date):
		if self._pcycle is None:
			self._pcycle=[]
			self._scycle=[]
			for c in filter(onlyltrs, self.fname):
				for i in range(self.l2nmap[c]):
					self._pcycle.append(c)
			for c in filter(onlyltrs, self.lname):
				for i in range(self.l2nmap[c]):
					self._scycle.append(c)
			if self.mname == "":
				self._mcycle=self._scycle
			else:
				self._mcycle=[]
				for c in filter(onlyltrs, self.mname):
					for i in range(self.l2nmap[c]):
						self._mcycle.append(c)
		diffyears=relativedelta(date,self.bdate).years
		pc=self._pcycle[diffyears%len(self._pcycle)]
		mc=self._mcycle[diffyears%len(self._mcycle)]
		sc=self._scycle[diffyears%len(self._scycle)]
		essence=self.l2nmap[pc]+self.l2nmap[mc]+self.l2nmap[sc]
		return pc,mc,sc,essence

	def personal_date_nums(self, date):
		if date not in self._pdate_nums_cache.keys():
			self._pdate_nums_cache[date]={}
			self._pdate_nums_cache[date]['year']=sum_digits(date.year+self.bdate.day+self.bdate.month,special=MASTER_NUMS)
			self._pdate_nums_cache[date]['month']=sum_digits(date.month+self._pdate_nums_cache[date]['year'],special=MASTER_NUMS)
			self._pdate_nums_cache[date]['day']=sum_digits(date.day+self._pdate_nums_cache[date]['month'],special=MASTER_NUMS)
		return self._pdate_nums_cache[date]

	@property
	def life_cycles(self):
		return PERIOD_CYCLES[sum_digits(self.life_path_num)]

	@property
	def birth_day_num(self):
		return sum_digits(self.bdate.day,special=ALLSPECIAL)

	@property
	def life_path_num(self):
		return sum_digits(self.bdate.month+self.bdate.year+self.bdate.day,special=ALLSPECIAL)

	@property
	def planes_of_expression(self):
		if self._eplane is None:
			c1=Counter([planes_of_expression[c][0] for c in self.full_name if onlyltrs(c)])
			c2=Counter([planes_of_expression[c][1] for c in self.full_name if onlyltrs(c)])
			self._eplane3=od([("physical",0),("emotional",0),("mental",0),("intuitive",0)])
			self._eplane4=od([("creative",0),("vacillating",0),("grounded",0)])
			for c in filter(onlyltrs,self.full_name): 
				k,k2=planes_of_expression[c]
				self._eplane3[k]=sum_digits(self.l2nmap[c]+self._eplane3[k])
				self._eplane4[k2]=sum_digits(self.l2nmap[c]+self._eplane4[k2])
			self._eplane,self._eplane2=c1.most_common()[0][0],c2.most_common()[0][0]
		return self._eplane,self._eplane2,self._eplane3,self._eplane4
	@property
	def full_name(self):
		return "{fname} {mname} {lname}".format(**vars(self))
	@property
	def pinnacles(self):
		#gets the end of the first pinnacle, 
		#	second pinnacle, and third pinnacle
		#	and also the number associated with each pinnacle
		if self._pinnacle_ends is None:
			first=36-self.life_path_num
			second=first+9
			third=second+9
			firstn=sum_digits(self.bdate.month+self.bdate.day)
			secondn=sum_digits(self.bdate.year+self.bdate.day)
			thirdn=sum_digits(firstn+secondn)
			fourthn=sum_digits(self.bdate.year+self.bdate.month)
			self._pinnacle_ends=(first,second,third,float('inf'))
			self._pinnacle_nums=(firstn,secondn,thirdn,fourthn)
		return self._pinnacle_ends,self._pinnacle_nums
	@property
	def challenge_nums(self):
		if self._challenge_nums is None:
			first=sum_digits(abs(self.bdate.month-self.bdate.day),special=MASTER_NUMS)
			second=sum_digits(abs(self.bdate.year-self.bdate.day),special=MASTER_NUMS)
			third=abs(first-second)
			fourth=sum_digits(abs(self.bdate.year-self.bdate.month),special=MASTER_NUMS)
			self._challenge_nums=(first,second,third,fourth)
		return self._challenge_nums

	@property
	def hidden_passion(self):
		if self._hidden_passion is None:
			self._hidden_passion=Counter([self.l2nmap[c] for c in self.full_name if onlyltrs(c)]).most_common(1)[0][0]
		return self._hidden_passion
	@property
	def subconscious_self(self):
		if self._subconscious is None:
			nums=set()
			for c in filter(onlyltrs,self.full_name): nums.add(self.l2nmap[c])
			self._subconscious=len(nums)
		return self._subconscious
	@property
	def possible_weaknesses(self):
			nums=set((self.l2nmap[c] for c in filter(onlyltrs, self.full_name)))
			return set(self.l2nmap.valid_nums)-nums
	@property
	def name_sum(self):
		return sum((self.l2nmap[c] for c in filter(onlyltrs, self.full_name)))
	@property
	def character_num(self):
		#expression
		return sum_digits(self.name_sum,special=ALLSPECIAL)
	@property
	def social_num(self):
		#personality
		total=sum(self.l2nmap[c] for c in filter(lambda x: onlycnsts(x), self.full_name))
		return sum_digits(total,special=ALLSPECIAL)
	@property
	def heart_num(self):
		#heart's desire
		total=sum(self.l2nmap[c] for c in filter(lambda x: onlyvwls(x), self.full_name))
		return sum_digits(total,special=ALLSPECIAL)
	@property
	def rational_thought_num(self):
		total=sum((self.l2nmap[c] for c in filter(onlyltrs, self.fname)))
		other_num=sum_digits(total)
		return sum_digits(self.birth_day_num+other_num)
	@property
	def balance_num(self):
		n1=self.l2nmap[self.fname[0]]
		n2=self.l2nmap[self.mname[0]] if self.mname != "" else 0
		n3=self.l2nmap[self.lname[0]]
		total=n1+n2+n3
		return sum_digits(total)
	@property
	def underlying_goal_num(self):
		#also known as the maturity number, where master numbers
		#aren't included
		return sum_digits(self.life_path_num+self.character_num,special=MASTER_NUMS)
	@property
	def capstone_num(self):
		#just ltr?
		return self.fname[0]
	@property
	def cornerstone_num(self):
		return self.fname[-1]
	@property
	def first_vowel_num(self):
		#first vowel of first name is for hint at hearts desire
		return list(filter(lambda x:onlyvwls(x), self.fname))[0]
'''
if __name__ == "__main__":
	import sys
	if len(sys.argv[1:]) < 2:
		print("Need a mapping file to process names", file=sys.stderr)
		exit(1)
	mappy=LetterMapping(sys.argv[1])
	for string in sys.argv[2:]:
		print(string)
		#minor versions of these are derived from name one is
		#	addressed by currently
		print("Character number:",character_num(string,mappy))
		print("Heart number:",heart_num(string,mappy))
		print("Social number:",social_num(string,mappy))
		print("---")
'''
