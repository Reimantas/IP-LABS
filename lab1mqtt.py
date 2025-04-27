import json

data = {
 "firstName": "Eimantas",
 "lastName": "Repsys",
 "city": "Vilnius",
 "age": "23",
 "hobby": "sports"
}


y=json.dumps(data)
print(y)