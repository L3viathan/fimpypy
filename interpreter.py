#!/usr/bin/python3
#FiM++ Interpreter#

import re


#Tokenizer "enum"
ROOT='ROOT' #used during some parsing experimentation
UNPARSED='UNPARSED' #default tag for unparsed text
COMMENT='COMMENT'
ENDLINE='ENDLINE'
ID='ID'
CLASS='CLASS'
STRING='STRING'
CLASSEND='CLASSEND'
METHOD='METHOD'
METHODTYPE='METHODTYPE'
METHODPARAMS='METHODPARAMS'
ENDMETHOD='ENDMETHOD'
RETURN='RETURN'
DECLARATION='DECLARATION'
NOTHING='NOTHING'
PRINT='PRINT'
INPUT='INPUT'
COMP='COMP'
NOT='NOT'
ISNOT='ISNOT'
ISLESS='ISLES'
ISMORE='ISMORE'
IS='IS'
MORE='MORE'
LESS='LESS'
AND='AND'
OR='OR'
WHITESPACE='WS'
NEWLINE='NEWLINE'
YOUR='YOUR'
FAITHFUL='FAITHFUL'
STUDENT='STUDENT'
TODAY='TODAY'
I='I'
LEARNED='LEARNED'
NT='NT'
THAN='THAN'
NO='NO'
THEN='THEN'
YOU='YOU'
GET='GET'
ELSE='ELSE'
SAID='SAID'
WROTE='WROTE'
SANG='SANG'
THOUGHT='THOUGHT'
HEARD='HEARD'
READ='READ'
ASKED='ASKED'
THAT='THAT'
S='S'
ALL='ALL'
ABOUT='ABOUT'
APOSTROPHE='APOSTROPHE'
WHAT='WHAT'
DID='DID'
WOULD='WOULD'
DO='DO'
ENDWHILE='ENDWHILE'
ENDIF='ENDIF'
WHILE='WHILE'
AS='AS'
LONG='LONG'
NUM='NUM'
COMMA='COMMA'
COLON='COLON'

inputtext='''Dear Princess Celestia: Hello World!

Today I learned how to say Hello World!
I said "Hello World"!
That's all about how to say Hello World!

Your faithful student, Kyli Rouge.'''
input2='''Dear Princess Celestia: Letter One.

Today I learned how to sing Applejack's Drinking Song.

Did you know that Applejack likes the number 99?

As long as Applejack had more than 1...
I sang Applejack" jugs of cider on the wall, "Applejack" jugs of cider,".
Applejack got one less. (Jug of cider)

When Applejack had more than 1...
I sang "Take one down and pass it around, "Applejack" jugs of cider on the wall.".

Otherwise: If Applejack had 1...
I sang "Take one down and pass it around, 1 jug of cider on the wall.
1 jug of cider on the wall, 1 jug of cider.
Take one down and pass it around, no more jugs of cider on the wall.".

Otherwise...
I sang "No more jugs of cider on the wall, no more jugs of cider.
Go to the store and buy some more, 99 jugs of cider on the wall.".
That's what I would do.
That's what I did. (End while)

That's all about how to sing Applejack's Drinking Song!

Your faithful student, Twilight Sparkle.'''

class FimCode:
	def __init__(self,inputtext):
		'''Code Object that holds the neccessary methods to tokenize, parse and execute FiM++ code.'''
		self.tokens=[] #List of tuples (type,text)
		self.raw=inputtext #never to be changed
	def tokenize_remove_empty(self):
		'''Remove tuples from the token list self.tokens that have an empty text span.'''
		self.tokens = [(a,b) for (a,b) in self.tokens if b != ""]
	def tokenize(self):
		'''Split text into tokens. Accounts for strings and comments that should not be split.'''
		i=0
		while True:
			if i>=len(self.tokens): #can't use a for loop because the iterable is changed during loop
				break
			if self.tokens[i][0] == COMMENT or self.tokens[i][0] == STRING: #Strings and comments should not be split
				i+=1
				continue
			old = self.tokens[i][1][:]
			splitted = re.findall("(\w+|[-\.\d]+| |\n|.|,|:|!|\?)",old)
			new = []
			for element in splitted:
				new += [(UNPARSED,element)]
			self.tokens = self.tokens[:i] + new + self.tokens[i+1:]
			i += 1
			self.tokenize_remove_empty()
	def lexer_tag(self,what,how):
		'''Tag all instances of 'what' with the tag 'how'.'''
		i=0
		while True:
			if i>=len(self.tokens): #can't use for loop because iterable is changed during loop
				break
			if self.tokens[i][0] != UNPARSED or what != self.tokens[i][1]:
				i+=1
				continue
			old = self.tokens[i][1][:]
			splitted = old.split(what)
			new = []
			for element in splitted:
				new += [(how,what),(UNPARSED,element)]
			new = new[1:]
			self.tokens = self.tokens[:i] + new + self.tokens[i+1:]
			i += 1
			self.tokenize_remove_empty()
	def lexer_nums(self):
		'''Tag numbers with the tag NUM'''
		for i in range(0,len(self.tokens)):
			if self.tokens[i][0] == UNPARSED:
				try:
					self.tokens[i] = (NUM,float(self.tokens[i][1]))
				except:
					continue
	def lexer_unify(self,listofthings,new):
		'''Transform all instances of the sequence defined in 'listofthings' to an unified tag 'new'.'''
		i=0
		while True:
			if i>=len(self.tokens): #can't use for loop because iterable is changed during loop
				break
			if self.tokens[i][0] == listofthings[0]:
				failure=False
				j=i
				for thing in listofthings[1:]:
					j+=1
					if thing !=self.tokens[j][0]:
						failure=True
						break
				if failure:
					i += 1
					continue
				self.tokens = self.tokens[:i] + [(new,"".join([a[1] for a in self.tokens[i:j+1]]))] + self.tokens[j+1:]
			i += 1
	def lexer_IDify(self):
		'''Change everything that is still untagged to an ID. Also collect IDs with spaces between them'''
		i=0
		while True:
			if i>=len(self.tokens): #can't use for loop because iterable is changed during loop
				break
			if self.tokens[i][0] == UNPARSED:
				j=i
				idlist=[self.tokens[i][1]]
				while True:
					j+=1
					if self.tokens[j][0] not in [UNPARSED,WHITESPACE]:
						break
					idlist.append(self.tokens[j][1])
				if idlist[-1] == " ":
					j -= 1
				self.tokens = self.tokens[:i] + [(ID,"".join([a[1] for a in self.tokens[i:j]]))] + self.tokens[j:]
			i += 1
	def run(self):
		'''Main routine of fimpypy'''
		#Find strings and comments first
		pointer=0
		unparsed=self.raw
		while pointer<len(unparsed):
			if unparsed[pointer] == "(":
				if pointer != 0:
					self.tokens.append((UNPARSED,unparsed[:pointer]))
					unparsed = unparsed[pointer:]
					pointer = 0
				while True: #Look for closing paren
					pointer+=1
					if unparsed[pointer] == ")":
						self.tokens.append((COMMENT,unparsed[:pointer+1]))
						unparsed = unparsed[pointer+1:]
						pointer = 0
						break
			elif unparsed[pointer] == '"':
				if pointer != 0:
					self.tokens.append((UNPARSED,unparsed[:pointer]))
					unparsed = unparsed[pointer:]
					pointer = 0
				while True: #Look for closing quote
					pointer+=1
					if unparsed[pointer] == '"':
						self.tokens.append((STRING,unparsed[:pointer+1]))
						unparsed = unparsed[pointer+1:]
						pointer = 0
						break
			pointer += 1
		self.tokens.append((UNPARSED,unparsed))
		#Insert Magic here:
		self.tokenize()
		self.lexer_tag(" ",WHITESPACE)
		self.lexer_tag("\n",NEWLINE)
		self.lexer_tag("Dear",CLASS)
		self.lexer_tag("Your",YOUR)
		self.lexer_tag("faithful",FAITHFUL)
		self.lexer_tag("student",STUDENT)
		self.lexer_tag("Today",TODAY)
		self.lexer_tag("I",I)
		self.lexer_tag("learned",LEARNED)

		self.lexer_tag("with",METHODTYPE)
		self.lexer_tag("using",METHODPARAMS)
		self.lexer_tag("Then",THEN)
		self.lexer_tag("you",YOU)
		self.lexer_tag("get",GET)
		self.lexer_tag("That",THAT)
		self.lexer_tag("s",S)
		self.lexer_tag("all",ALL)
		self.lexer_tag("about",ABOUT)
		self.lexer_tag("'",APOSTROPHE)
		self.lexer_tag("Did you know that ",DECLARATION)
		self.lexer_tag("nothing ",NOTHING)
		self.lexer_tag("said",SAID)
		self.lexer_tag("wrote",WROTE)
		self.lexer_tag("sang",SANG)
		self.lexer_tag("thought",THOUGHT)
		self.lexer_tag("heard",HEARD)
		self.lexer_tag("read",READ)
		self.lexer_tag("asked",ASKED)
		for i in ["is","was","has","had"]:
			self.lexer_tag(i,COMP)
		self.lexer_tag("not",NOT)
		self.lexer_tag("n't",NT)
		self.lexer_tag("no",NO)
		self.lexer_tag("less",LESS)
		self.lexer_tag("greater",MORE)
		self.lexer_tag("more",MORE)
		self.lexer_tag("than",THAN)
		self.lexer_tag("and ",AND)
		self.lexer_tag("or ",OR)
		self.lexer_tag("Otherwise",ELSE)
		self.lexer_tag("did",DID)
		self.lexer_tag("do",DO)
		self.lexer_tag("would",WOULD)
		self.lexer_tag("what",WHAT)
		self.lexer_tag("As",AS)
		self.lexer_tag("as",AS)
		self.lexer_tag("long",LONG)
		self.lexer_tag(",",COMMA)
		self.lexer_tag(":",COLON)
		for i in ".!?‽…":
			self.lexer_tag(i,ENDLINE)
		

		self.lexer_unify([YOUR,WHITESPACE,FAITHFUL,WHITESPACE,STUDENT,COMMA],CLASSEND)
		self.lexer_unify([COMP,NOT],ISNOT)
		self.lexer_unify([TODAY,WHITESPACE,I,WHITESPACE,LEARNED],METHOD)
		self.lexer_unify([I,WHITESPACE,LEARNED],METHOD)
		self.lexer_unify([COMP,NT],ISNOT)
		self.lexer_unify([COMP,WHITESPACE,NOT],ISNOT)
		self.lexer_unify([COMP,WHITESPACE,MORE,WHITESPACE,THAN],ISMORE)
		self.lexer_unify([COMP,WHITESPACE,LESS,WHITESPACE,THAN],ISLESS)
		self.lexer_unify([COMP],IS)
		self.lexer_unify([THEN,WHITESPACE,YOU,WHITESPACE,GET],RETURN)
		self.lexer_unify([I,WHITESPACE,SAID],PRINT)
		self.lexer_unify([I,WHITESPACE,THOUGHT],PRINT)
		self.lexer_unify([I,WHITESPACE,SANG],PRINT)
		self.lexer_unify([I,WHITESPACE,WROTE],PRINT)
		self.lexer_unify([I,WHITESPACE,ASKED],INPUT)
		self.lexer_unify([I,WHITESPACE,HEARD],INPUT)
		self.lexer_unify([I,WHITESPACE,READ],INPUT)
		self.lexer_unify([THAT,APOSTROPHE,S,WHITESPACE,ALL,WHITESPACE,ABOUT],ENDMETHOD)
		self.lexer_unify([THAT,APOSTROPHE,S,WHITESPACE,WHAT,WHITESPACE,I,WHITESPACE,DID],ENDWHILE)
		self.lexer_unify([THAT,APOSTROPHE,S,WHITESPACE,WHAT,WHITESPACE,I,WHITESPACE,WOULD,WHITESPACE,DO],ENDIF)
		self.lexer_unify([AS,WHITESPACE,LONG,WHITESPACE,AS],WHILE)

		self.lexer_nums()
		self.lexer_IDify()
		#In the end
		return self.tokens #just for testing

code=FimCode(inputtext)
print(code.run())
