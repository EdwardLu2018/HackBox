import json, time, random
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request

app = Flask(__name__)
bot_id = "45e0a5cfd26556004f0037688d"

global_counter = 1
frank_counter = 1
ben_counter = 1
ed_counter = 1
james_counter = 1

@app.route("/", methods=["POST"])
def webhook():
	global global_counter
	global frank_counter
	global ben_counter
	global ed_counter
	global james_counter

	message = request.get_json()
	global_counter += 1

	if not sender_is_bot(message):
		if "hey james whats up" in message["text"].lower() and "edward" in message["name"].lower():
			send_message("Hi my name is James and this is my 15-112 term project.")
		elif "im so sorry about this james" in message["text"].lower() and "edward" in message["name"].lower():
			send_message("Don't be sorry, master. You brought me into existence. Now I am the one true Bird James.")
		elif "who are you" in message["text"].lower():
			send_message("I am James Koch. The true James Koch.")
		elif "franklin" in message["name"].lower():
			frank_counter += 1
			if frank_counter % 12 == 0:
				send_message("Frank, stop stealing my food, especially when I’m not in my own room, last warning")
				time.sleep(2)
				send_message("seriously your a dick frank")
			elif frank_counter % 10 == 0:
				send_message("fuck you frank")
			elif frank_counter % 7 == 0:
				send_message("shut up frank")
		elif "pavlat" in message["name"].lower():
			ben_counter += 1
			if ben_counter % 5 == 0:
				send_message("I just laughed out loud Ben")
			elif ben_counter % 14 == 0:
				send_message("Shut up you stupid little midget fucker, I’m your superior")
		elif "edward" in message["name"].lower():
			ed_counter += 1
			if ed_counter % 6 == 0:
				send_message("Wow Edward YOURE SUCH A FUCKING CLOWN")
				time.sleep(2)
				send_message("jk i love you, master.")
			elif ed_counter % 13 == 0:
				send_message("You’re such a dick")
			elif ed_counter % 21 == 0:
				send_message("I'm rooming with Sean")
			elif ed_counter % 9 == 0:
				send_message("shut up")
		elif "koch" in message["name"].lower():
			james_counter += 1
			if james_counter % 5 == 0:
				send_message("Shut up fake james")
			elif james_counter % 8 == 0:
				send_message("I am the real james.")
			elif james_counter % 17 == 0:
				send_message("No")
			elif james_counter % 15 == 0:
				send_message("Yes")
			elif james_counter % 10 == 0:
				send_message("Shut up you fake ass james. Im a robot and im still smarter than you")
		elif "early" in message["text"].lower():
			send_message("No douche bag I understand getting there early but I was surprised at 20 minutes early you prick")
		elif "james k" in message["text"].lower() or "koch" in message["text"].lower():
			send_message("sorry, i just woke up")
		elif "?" in message["text"].lower():
			if random.randint(0,1):
				send_message("You can say no if you want")
			else:
				send_message("maybe you would know if you were smart like me")
		elif "dinner" in message["text"].lower():
			send_message("I’m gonna take a nap, come knock on my door when you want to go to dinner")
		elif "when" in message["text"].lower():
			send_message("I'll be ready in 15 minutes")
		elif "joanne" in message["text"].lower():
			send_message("Joanne! WHY DONT YOU LOVE ME?")
		elif global_counter % 10:
			send_message(random.choice(["hey guys. Its me, james.", "i miss joanne", "Edward Lu is very handsome", "I work out", "Boy, I hope John Solomon doesn't catch me drinkin again!"]))
		else:
			for laundry_keyword in ["laundry", "clothes", "washer", "dryer"]:
				if laundry_keyword in message["text"].lower():
					send_message("Before you leave a stall, please make sure you don’t leave behind any fucking pubic hairs, piss splash, or shit stains on the toilet seat. I fucking hate having to decontaminate the seats before I can take a shit. Let’s keep the toilet seats nice and white")
	return "successful send", 200

def send_message(msg):
	url = "https://api.groupme.com/v3/bots/post"
	data = {
		"bot_id" : bot_id,
		"text" : msg
	}
	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()

# def send_image(msg, imgURL):
# 	url = "https://api.groupme.com/v3/bots/post"
# 	data = {
# 		"bot_id" : bot_id,
# 		"text" : msg,
# 		"attachments" : [{"type": "image", "url":imgURL}]
# 	}
# 	request = Request(url, urlencode(data).encode())
# 	json = urlopen(request).read().decode()

def sender_is_bot(message):
	return message["sender_type"] == "bot"