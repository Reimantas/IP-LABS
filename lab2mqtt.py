import json
import sys

# Nustatome UTF-8 konsolei
sys.stdout.reconfigure(encoding='utf-8')

try:
    # 1. Nuskaitome users1.json
    with open('users1.json', 'r', encoding='utf-8') as file:
        users1_data = json.load(file)

    # 2. Nuskaitome users2.json
    with open('users2.json', 'r', encoding='utf-8') as file:
        users2_data = json.load(file)

    # 3. Sujungiame users1.json ir users2.json duomenis
    users1_data['table']['users'].update(users2_data['table']['users'])

    # 4. Issaugome rezultata i users.json
    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(users1_data, file, indent=4, ensure_ascii=False)

    print("Data successfully merged and saved to users.json")

except FileNotFoundError as e:
    print(f"Error: File not found - {e}")
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON structure - {e}")
except Exception as e:
    print(f"Unexpected error: {e}")