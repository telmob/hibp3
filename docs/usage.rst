=====
Usage
=====

To use hibp3 in a project::

    import hibp3
    >>> import hibp3
    >>> t = hibp3.Checkemail("test@example.com")
    >>> t.fetch()
    True
    >>> t.pwned
    True
    >>> t.status()
    test@example.com pwned in 54 breaches
    ['000webhost', '7k7k', 'Adobe', 'Anti Public Combo List', 'Bitcoin Talk', 'Bitly', 'Bolt', 'BTC-E', 'Coupon Mom / Armor Games', 'Dailymotion', 'diet.com', 'Disqus', 'Dodonew.com', 'Dropbox', 'Elance', 'Evony', 'Exploit.In', 'Funimation', 'Gawker', 'GeekedIn', 'GFAN', 'Heroes of Newerth', 'iMesh', 'Last.fm', 'Lifeboat', 'LinkedIn', 'Little Monsters', 'mail.ru Dump', 'MCBans', 'MPGH', 'mSpy', 'MySpace', 'NetEase', 'Nihonomaru', 'Onliner Spambot', 'OwnedCore', 'Patreon', 'PayAsUGym', 'QIP', 'QuinStreet', 'R2Games', 'River City Media Spam List', 'Staminus', 'Stratfor', 'Trillian', 'tumblr', 'vBulletin', 'VK', 'We Heart It', 'WHMCS', 'Wishbone', 'XSplit', 'Yahoo', 'Zomato']
