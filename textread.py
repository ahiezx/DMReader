import requests, json, os, time, colorama
from colorama import Fore, Style, Back
from datetime import timedelta

colorama.init()
print(Style.BRIGHT, end='\r')

sessionid = input("[I] Enter Sessionid : ")
limit = input("[I] Enter Inbox Limit : ")

headers = {
    "Host": "i.instagram.com",
    "Accept": "*/*",
    "User-Agent": "Instagram 118.0.0.25.121 (iPhone11,8; iOS 13_1_3; en_US; en-US; scale=2.00; 828x1792; 180988914)",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": f"sessionid={sessionid}"
}

def getInbox():
    inbox = requests.get(f"https://i.instagram.com/api/v1/direct_v2/inbox/?limit={limit}&thread_message_limit=1", headers=headers)
    return inbox.json()['inbox']['threads']

def showMessages(thread_id, msglimit=5):
    messages = requests.get(f"https://i.instagram.com/api/v1/direct_v2/threads/{thread_id}/?limit={int(msglimit)+1}", headers=headers)
    user = messages.json()['thread']['users'][0]['username']
    
    return list(reversed(messages.json()['thread']['items'])), user

count = 1
for thread in getInbox():
    thread_id = thread['thread_id']
    print()
    msglimit = input(f"[I] Enter Message Limit For User {count}: ")
    messages, user = showMessages(thread_id, msglimit)
    count += 1
    print(f"Messages from {Back.GREEN} {user} {Back.RESET}")
    msgcount = 1
    for msg in messages:

        delta = time.time() - int(msg['timestamp'] /1000000)

        if delta < 60:
            delta = f"{int(delta)} seconds ago"
        elif delta < 3600:
            delta = f"{int(delta/60)} minutes ago"
        elif delta < 86400:
            delta = f"{int(delta/3600)} hours ago"
        elif delta < 604800:
            delta = f"{int(delta/86400)} days ago"
        elif delta < 2592000:
            delta = f"{int(delta/604800)} weeks ago"
        elif delta < 31536000:
            delta = f"{int(delta/2592000)} months ago"
        else:
            delta = f"{int(delta/31536000)} years ago"

        print(f"""
    {Fore.CYAN} Message {msgcount}: {Fore.RESET} - {Fore.RED} {msg['item_type']} {Fore.RESET} - {Fore.YELLOW} {msg['text'] if 'text' in msg else 'N/A'} {Fore.RESET}
    {Fore.GREEN} {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(msg['timestamp'] /1000000)))} ({delta}) {Fore.RESET}
        """)
        msgcount += 1