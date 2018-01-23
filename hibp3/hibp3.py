from __future__ import print_function
import requests
import json
import time


class Checkemail:
    """
    :attribute email: Target email
    :attribute services: List of breached services if target is positive
    :attribute rate: Throttling rate in seconds
    :attribute pwned: True is pwned, False if not or unconfirmed
    :type email: str
    :type services: List
    :type rate: float
    :type pwned: bool

    Checks an email address for breaches using the haveibeenpwned.com API
    You can pass target email as initialisation param of the object,
    or by setting the ``email`` attribute
    To query HIBP use the ``.fetch()`` method
    Results can be viewed using `bool` attribute pwned,
    or by using method ``status`` to also view breached services
    Example::
            >>> import hibp3
            >>> t = hibp3.Checkemail("test@example.com")
            >>> t.fetch()
            True
            >>> t.pwned
            True
            >>> t.status()
            test@example.com pwned in 54 breaches
            ['000webhost', '7k7k', 'Adobe', 'Anti Public Combo List', 'Bitcoin Talk', 'Bitly', 'Bolt', 'BTC-E', 'Coupon Mom / Armor Games', 'Dailymotion', 'diet.com', 'Disqus', 'Dodonew.com', 'Dropbox', 'Elance', 'Evony', 'Exploit.In', 'Funimation', 'Gawker', 'GeekedIn', 'GFAN', 'Heroes of Newerth', 'iMesh', 'Last.fm', 'Lifeboat', 'LinkedIn', 'Little Monsters', 'mail.ru Dump', 'MCBans', 'MPGH', 'mSpy', 'MySpace', 'NetEase', 'Nihonomaru', 'Onliner Spambot', 'OwnedCore', 'Patreon', 'PayAsUGym', 'QIP', 'QuinStreet', 'R2Games', 'River City Media Spam List', 'Staminus', 'Stratfor', 'Trillian', 'tumblr', 'vBulletin', 'VK', 'We Heart It', 'WHMCS', 'Wishbone', 'XSplit', 'Yahoo', 'Zomato']



    """

    email = ""
    services = []
    rate = 1.3
    ssl = True
    server = "haveibeenpwned.com"
    pwned = False

    def __init__(self, *args):
        """
    Target email to query for HIBP can be set as init param or ``email``
    attribute
        Args:
        :param email: target email
        :type email: type str
        """

        self.email = args[0]
        self.check = None

    def _clean(self):
        """
    Internal function to parse API result
        """
        self.check = json.loads(self.check.text)
        self.breaches = len(self.check)
        for i in self.check:
            self.services += [i["Title"]]

    def fetch(self):
        """
    Queries the HIBP API
    Handles recommended throttling
        Returns:
          :return: True or False depending on breached or not
          :rtype: bool

        """
        self.check = requests.get(
            "https://" + self.server + "/api/v2/breachedaccount/" +
            self.email + "?includeUnverified=true",
            verify=self.ssl)
        if str(self.check.status_code) == "404":
            self.check = "Not pwned"
            self.pwned = "False"
            time.sleep(self.rate)
            return False
        elif str(self.check.status_code) == "200":
            self.pwned = True
            self._clean()
            time.sleep(self.rate)
            return True
        elif str(self.check.status_code) == "429":
            time.sleep(self.rate)
            self.fetch()
        else:
            time.sleep(self.rate)
            return True

    def status(self):
        """
        Prints the result of the query, also shows breached services
        Requires having run the ``fetch`` method successfully

        """

        if self.check == "Not pwned":
            print("%s is not pwned" % self.email)
        elif (self.check is None) & (self.pwned is False):
            print("Did you run fetch method correctly?")
        elif (self.check is not None) & (self.pwned is True):
            print("{} pwned in {} breaches".format(self.email, self.breaches))
            print(self.services)
        else:
            print("Something is wrong")
