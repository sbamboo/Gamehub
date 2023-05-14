import getpass
import socket
import datetime
import hashlib

def entropyGenerator() -> str:
    user = getpass.getuser()
    host = socket.gethostname()
    date = datetime.date.today().strftime('%y-%m-%d')
    entropy_str = f'{user}-{host}-{date}'
    entropy = hashlib.sha256(entropy_str.encode()).hexdigest()
    return entropy