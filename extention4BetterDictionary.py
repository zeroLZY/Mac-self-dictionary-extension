#encoding=utf-8
#input : every line of the string context with whitespace and garbage
#output: pure word
def deal_string_line(string_line):
	new_string = string_line.strip() #remove front whitespaces
	#remove <string> or </string> flags
	flag1 = '<string>'
	flag2 = '</string>'
	new_string = new_string.replace(flag1,'')
	new_string = new_string.replace(flag2,'')
	return new_string

def file_filter(aFile):
	count = 0
	back_up = [] # a list of every line string
	#return this back_up list
	for everyline in aFile:
		count +=1
		if count >5:
			dealt_line = deal_string_line(everyline)
			back_up.append(dealt_line)
	#remove the last two item in aList
	length = len(back_up)
	back_up.remove(back_up[length-1])
	back_up.remove(back_up[length-2])
	return back_up

def write_to_file(aList,aFile):
	for every_item in aList:
		aFile.write(every_item)
		aFile.write('\n')

def read_to_List(aFile):
	back_up = []
	for everyline in aFile:
		#remove the '\n' of everyline
		everyline = everyline.replace('\n','')
		back_up.append(everyline)
	return back_up

dictionary_file = open('/Users/zero/Library/Containers/com.apple.Dictionary/Data/Library/Application Support/BetterDictionary/saved-words.plist')
#this path is where Pooria Azimi's BetterDictionary the stores table of words
everyday_words = open('/Users/zero/Desktop/everyday_words.txt','r')
#this path is where I store the table of words which could be edited by the users.
original_context_list = read_to_List(everyday_words)
everyday_words.close()

everyday_words = open('/Users/zero/Desktop/everyday_words.txt','w')
new_context_list      = file_filter(dictionary_file)

merge_context_list = list( set( original_context_list + new_context_list))
print original_context_list
print new_context_list
print merge_context_list
write_to_file(merge_context_list,everyday_words)



#write_to_file(file_filter(dictionary_file),write_dictionary)
everyday_words.close()
dictionary_file.close()	


