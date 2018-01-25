=====
Usage
=====

To use hibp3 in a project::

    import hibp3
    >>> import hibp3
    >>> t = hibp3.Checkemail("test@example.com")
    True
    >>> t.pwned
    True
    >>> t.status()
    test@example.com pwned in 54 breaches
    ['000webhost', '7k7k', 'Adobe', ...]
