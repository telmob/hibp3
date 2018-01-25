from __future__ import print_function
import requests
import json
import time


class Checkemail:
    """
    :ivar services: List of breached services if target is positive
    :ivar rate: Throttling rate in seconds,
        default is HIBP friendly (1.3s)

    :ivar pwned: True is pwned, False if not or unconfirmed
    :type email: str
    :type services: List
    :type rate: float
    :type pwned: bool

    :param email: target email
    :type email: type str

    * Checks an email address for breaches using the haveibeenpwned.com API
    * You can pass target email as initialisation param
        of the object or by setting the ``email`` attribute

    * Results can be viewed using:
        * `bool` attribute ``pwned``
        * by using method :func:`status` to also view breached services

    * Example:
            >>> import hibp3
            >>> t = hibp3.Checkemail("test@example.com")
            >>> t.pwned
            True
            >>> t.status()
            test@example.com pwned in 54 breaches
            ['000webhost', '7k7k', 'Adobe', ...]

    .. note:: If email is not set during object creation,
        you must set email and call the :func:`fetch()` method

    """

    def __init__(self, *args):
        """
    Target email to query for HIBP can be set as init param or ``email``
    attribute

        """
        self.email = args[0]
        self.check = None
        self.services = []
        self.rate = 1.3
        self.ssl = True
        self.server = "haveibeenpwned.com"
        self.pwned = False
        if self.email:
            self.fetch()

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
    * Queries the HIBP API
    * Handles recommended throttling
        Returns:
          :return: True or False depending on breached or not
          :rtype: bool

    .. note:: This method is run at object creation if `email` param is passed

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
