from collections import Counter
z = [
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
'blue', 'red', 'blue', 'yellow', 'blue', 'red',
]
print Counter(z)