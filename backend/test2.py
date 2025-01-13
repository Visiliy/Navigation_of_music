from difflib import SequenceMatcher
 
str1 = "родилась"
str2 = "радилась"
 
matcher = SequenceMatcher(None, str1, str2)
similarity = matcher.ratio()
 
print(f"Сходство между '{str1}' и '{str2}': {similarity:.2f}")
