import requests
import json


def print_help():
	print('COMMANDS:')
	print('\thelp -> show help')
	print('\texit -> exit')
	print('\tupdate -> fetch new messages')
	print('\tsend <username> <msg> -> send message to contact')
	print('\tcontact add <username> <id> -> adds user for given id')
	print('\tcontact rem <username> -> removes user')
	print('\tcontact show -> shows users')

def contact_lookup(username):
	with open('contacts.txt', 'r') as f:
			data = json.load(f)
			if username not in data:
				print('\t> Kontakt ' + str(username) + ' nicht gefunden')
				return None
			else:
				return data[username]

def manipulate_to_contacts(action, username=None, user_id=None):
	in_data = False
	data = None
	with open('contacts.txt', 'r') as f:
			data = json.load(f)
			if username in data:
				in_data = True

	if (data is not None):
		if action == 'add':
			if not in_data:
				with open('contacts.txt', 'w') as outfile:
					data[username] = user_id
					json.dump(data, outfile)
					print('\t> Kontakt ' + str(username) + ' mit der ID ' + str(user_id) + ' hinzugefügt!')
			else:
				print('\t> Kontakt ' + str(username) + ' ist bereits in deinen Kontakten!')
		elif action == 'rem':
			if in_data:
				with open('contacts.txt', 'w') as outfile:
					id_copy = data[username]
					del data[username]
					json.dump(data, outfile)
					print('\t> Kontakt ' + str(username) + ' mit der ID ' + str(id_copy) + ' gelöscht!')
			else:
				print('\t> Kontakt ' + str(username) + ' ist NICHT in deinen Kontakten!')
		else:
			if len(data) == 0:
				print('\tKontaktliste leer!')
			else:
				for i, (user_entry, id_entry) in enumerate(data.items(), 1):
					print('\t--- KONTAKTE ---\n')
					print('\t> Kontakt ' + str(i) + ":")
					print('\t\tName: ' + str(user_entry))
					print('\t\tID: ' + str(id_entry) + '\n')
	else:
		print("!! FEHLER: contacts.txt fehlt oder fehlerhaft")

token = ''

with open('token.txt', 'r') as file:
	token = file.read()

print("---------SendYourLink---------")
# link = str(input("Enter your Link now: \n--> "))
stay = True

while stay:
	choice = input('-> ')

	args = choice.split(' ')
	keyword = args[0]

	if keyword.lower() == 'exit':
		stay = False
		print("...Thanks for using SendYourLink...")

	elif keyword.lower() == 'update':

		# token = '1726566416:AAEOvLbbSh1Ld_UyilcYG-hQzqwNvqxQ2jg'

		answer = requests.get(f'https://api.telegram.org/bot{token}/getUpdates')

		content = answer.content
		data = json.loads(content)

		if data['ok'] == True:
			results = data['result']
			if len(results) > 3:
				results = results[-3:]
			for i, result in enumerate(results):
				msg = result['message']
				chat_id = msg['chat']['id']
				print("\t--- Eintag " + str(i) + " ---")
				print("\t> Absender: " + str(msg['chat']['first_name']) + ", ID: " + str(chat_id))
				print("\t> Nachricht: " + str(msg['text']))

	elif keyword.lower() == 'send':
		if len(args) >= 3:
			msg = " ".join(args[2:])
			addr = args[1]

			chat_id = contact_lookup(addr)

			if chat_id is not None:
				params = {"chat_id":chat_id, "text":msg}
				url = f'https://api.telegram.org/bot{token}/sendMessage'
				answer = requests.post(url, params=params)

				content = answer.content
				data = json.loads(content)

				if data['ok'] == True:
					print("\t> Nachricht an " + str(addr) + " gesendet!")
				else:
					print("\t> Nachricht konnte nicht gesendet werden (falsche ID hinterlegt?)!")

			
		else:
			print('Usage:')
			print_help()

	elif keyword.lower() == 'contact':
		if len(args) < 2:
			print_help()
		else:
			to_do = args[1]
			if to_do.lower() == 'add':
				if len(args) != 4:
					print_help()
				else:
					username = args[2]
					user_id = args[3]
					manipulate_to_contacts(to_do, username=username, user_id=user_id)
			elif to_do.lower() == 'show':
				if len(args) != 2:
					print_help()
				else:
					manipulate_to_contacts(to_do)
			elif to_do.lower() == 'rem':
				if len(args) != 3:
					print_help()
				else:
					username = args[2]
					manipulate_to_contacts(to_do, username=username)
			else:
				print_help()


	elif keyword.lower() == 'help':
		print_help()
	else:
		print_help()



