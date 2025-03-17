import re

txt = "1231242342B234234"

#Search for a sequence that starts with "he", followed by 1 or more  (any) characters, and an "o":

x = re.search("[A-Z]+", txt)

if x:
	print("found")
else:
	print("not found")