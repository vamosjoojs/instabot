import datetime

import aux_funcs, time, random
from LevPasha.InstagramAPI import InstagramAPI
import os

followers = []
followings = []
api = InstagramAPI(os.getenv('user'), os.getenv('pass'))

print(f"User: {os.getenv('user')}")

### Delay in seconds ###
min_delay = 5
max_delay = 10

## The daily limit is 200 a day. 10 follows and unfollows per hour would keep your account safe and saves your account from being suspended.

MAXIMO = 200
print(f"Max of the day: {MAXIMO}")


def info():
	print("I follow them but they dont follow me:\n")
	tot = 0
	for i in followings:
		if i not in followers:
			tot=tot+1
			print(str(tot)+" "+i)
	print("\nTotal: "+str(tot))

	print("\nThey follow me but i dont follow them:\n")
	tot = 0
	for i in followers:
		if i not in followings:
			tot=tot+1
			print(str(tot)+" "+i)
	print("\nTotal: "+str(tot))

	print("\nPeople following me:\n")
	tot = 0
	for i in followers:
		tot=tot+1
		print(str(tot)+" "+i)
	print("\nTotal: "+str(tot))

	print("\nPeople I follow:\n")
	tot = 0
	for i in followings:
		tot=tot+1
		print(str(tot)+" "+i)
	print("\nTotal: "+str(tot))


def updated_followed(user_id):
	with open("followed_users_id.txt", "a") as myfile:
		myfile.write(str(user_id)+'\n')


def get_followed():
	with open("followed_users_id.txt", 'r') as arq:
		followed = arq.readlines()

	return [int(x) for x in followed]


def follow_tag(tag, tot):
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
			print("Following "+str(username)+" (with id "+str(user_id)+")")
		else:
			print("Ja seguido.")
		if tot >= MAXIMO:
			break
	print("Total in day: "+str(tot)+" for tag "+tag+" (Max val: "+str(MAXIMO)+")\n")


def follow_location(target):
	api.getLocationFeed(target)
	media_id = api.LastJson
	tot = 0
	for i in media_id.get("items"):
		time.sleep(float( random.uniform(min_delay*10,max_delay*10) / 10 ))
		username = i.get("user").get("username")
		user_id = aux_funcs.get_id(username)
		api.follow(user_id)
		tot += 1
		print("Following "+str(username)+" (with id "+str(user_id)+")")
		if(tot>=MAXIMO):
			break
	print("Total: "+str(tot)+" for location "+str(target)+" (Max val: "+str(MAXIMO)+")\n")


def follow_list(target):
	user_list = open(target).read().splitlines()
	tot = 0
	for username in user_list:
		time.sleep(float( random.uniform(min_delay*10,max_delay*10) / 10 ))
		user_id = aux_funcs.get_id(username)
		api.follow(user_id)
		tot += 1
		print("Following "+str(username)+" (with id "+str(user_id)+")")
		if(tot>=MAXIMO):
			break
	print("Total: "+str(tot)+" users followed from "+str(target)+" (Max val: "+str(MAXIMO)+")\n")


def super_followback(count):
	for i in followers:
		if i not in followings:
			time.sleep(float(random.uniform(min_delay*10,max_delay*10) / 10))
			print(str(count)+") Following back "+i)
			user_id = aux_funcs.get_id(i)
			api.follow(user_id)
			count+=1
	return count


def super_unfollow():
	whitelist = open("whitelist.txt").read().splitlines()
	count = 0
	for i in followings:
		if (i not in followers) and (i not in whitelist):
			count+=1
			time.sleep(float( random.uniform(min_delay*10,max_delay*10) / 10 ))
			print(str(count)+") Unfollowing "+i)
			user_id = aux_funcs.get_id(i)
			api.unfollow(user_id)


def unfollowall():
	whitelist = open("whitelist.txt").read().splitlines()
	count = 0
	for i in followings:
		if i not in whitelist:
			count +=1
			time.sleep(float( random.uniform(min_delay*10,max_delay*10) / 10 ))
			print(str(count)+") Unfollowing "+i)
			user_id = aux_funcs.get_id(i)
			api.unfollow(user_id)


def main():
	api.login()
	while True:
		tot = 0
		target = os.getenv('tag')
		follow_tag(target, tot)


if __name__ == "__main__":
	main()
