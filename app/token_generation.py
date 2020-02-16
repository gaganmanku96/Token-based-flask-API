import secrets


class TokenGeneration:
    """
    Generates token to access the API.
    """
    def __init__(self):
        """
        Well, nothing to do here
        """
        pass

    def get_token(self, lenght=20):
        """
        Generates token of specified lenght

        Parameters
        ----------
        length: int
            The default value of the argument is 10.
        """
        return str(secrets.token_urlsafe(lenght))