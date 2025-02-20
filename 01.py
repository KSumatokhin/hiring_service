users = [
    {'first_name': 'Иван', 'last_name': 'Иванов'},
    {'first_name': 'Семен', 'last_name': 'Семенов'},
    {'first_name': 'Петр', 'last_name': 'Петров'},
    {'first_name': 'Алексей', 'last_name': 'Алексеев'},
    {'first_name': 'Дмитрий', 'last_name': 'Дмитриев'},
]

reply_keyboard = [[f"{user['first_name']} {user['last_name']}" for user in users]]

print(reply_keyboard)