import time, random
from LevPasha.InstagramAPI import InstagramAPI
import os

followers = []
followings = []

api = InstagramAPI(os.getenv('user'), os.getenv('pass'))

print(f"User: {os.getenv('user')}")

min_delay = 5
max_delay = 10

MAXIMO = 200
print(f"Max of the day: {MAXIMO}")


def updated_followed(user_id):
	with open("followed_users_id.txt", "a") as myfile:
		myfile.write(str(user_id)+'\n')


def get_followed():
	with open("followed_users_id.txt", 'r') as arq:
		followed = arq.readlines()

	return [int(x) for x in followed]


def follow_tag(tag):
	tot = 0
	api.getLocationFeed('Brazil')
	api.tagFeed(tag)
	media_id = api.LastJson
	print("\nTAG: "+str(tag)+"\n")
	for i in media_id["items"]:
		time.sleep(float(random.uniform(min_delay*10, max_delay*10) / 10))
		username = i.get("user")["username"]
		user_id = i.get("user")["pk"]
		followed = get_followed()
		if user_id not in followed:
			api.follow(user_id)
			updated_followed(user_id)
			tot += 1
			if tot / 10 in range(1, 11):
				print('ja segui 10, dorme 1 hora')
				time.sleep(3600)
				print("continuando")
			print("Following "+str(username)+" (with id "+str(user_id)+")")
		else:
			print("Ja seguido.")
		if tot >= MAXIMO:
			break
	print("Total in day: "+str(tot)+" for tag "+tag+" (Max val: "+str(MAXIMO)+")\n")


def main():
	api.login()
	target = os.getenv('tag')
	follow_tag(target)


if __name__ == "__main__":
	main()
