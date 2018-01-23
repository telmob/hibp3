from __future__ import print_function
import requests
import json
import time


class Checkemail:
    """
    Checks an email address for breaches using the haveibeenpwned.com API
    You can pass target email as initialisation param of the object,
    or by setting the ``email`` attribute
    To query HIBP use the ``.fetch()`` method
    Results can be viewed using `bool` attribute pwned,
    or by using method ``status`` to also view breached services
    """
    """
    :param email: Target email
    :param services: List of breached services if target is positive
    :param rate: Throttling rate in seconds
    :param pwned: True is pwned, False if not or unconfirmed
    :type email: str
    :type services: List
    :type rate: float
    :type pwned: bool
    """

    email = ""
    services = []
    rate = 1.3
    ssl = True
    server = "haveibeenpwned.com"
    pwned = False

    """A simple hibp python 3 class test"""

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
