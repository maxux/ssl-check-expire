import socket
import datetime
import ssl

class SSLExpireCheck:
    def __init__(self, target, port=443):
        self.target = target
        self.port = port

    def expiration(self):
        ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

        try:
            context = ssl.create_default_context()

            conn = context.wrap_socket(
                socket.socket(socket.AF_INET),
                server_hostname=self.target,
            )

            conn.connect((self.target, self.port))
            ssl_info = conn.getpeercert()

        except ssl.SSLError as e:
            return None

        return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)

if __name__ == '__main__':
    websites = [
        "arya.maxux.net",
        "clea.maxux.net",
        "cbseraing.be",
        "irc.maxux.net",
        "ssh.maxux.net",
        "www.maxux.net",
        "frites.maxux.net",
        "www.cbseraing.be",
        "www.lapersonnelaplusrichedinternet.eu",
        "www.magickey.be",
        "msgur.maxux.net",
    ]

    services = [
        ("irc.maxux.net", 6697),
    ]

    print("== Websites ==")
    for website in websites:
        site = SSLExpireCheck(website)
        print("%-20s: %s" % (website[0:20], site.expiration()))

    print("")
    print("== Services ==")
    for service in services:
        remote = SSLExpireCheck(service[0], service[1])
        print("%-20s: %s" % (("%s [%s]" % (service[0][0:20], service[1]), site.expiration())))
