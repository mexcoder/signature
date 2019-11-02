from abc import ABC, abstractmethod

class baseSignature(ABC):

    # properties

    @property
    def private_key(self):
        """this instance private key, used for signature generation"""
        return self._private_key

    @private_key.setter
    def private_key(self, value):
        self._private_key = value

    @private_key.deleter
    def private_key(self):
        del self._private_key

    @property
    def public_key(self):
        """this instance public key, used for validation"""
        return self._public_key

    @public_key.setter
    def public_key(self, value):
        self._public_key = value

    @public_key.deleter
    def public_key(self):
        del self._public_key

    # constructor

    def __init__(self, public_key=None, private_key=None):
        super().__init__
        self.private_key = private_key
        self.public_key = public_key

    # methods (abstract)
    @abstractmethod
    def hashString(self,target):
        """returns the hash of the target string
        
        :param target: the string to hash
        :type target: str
        """
        pass

    @abstractmethod
    def makeKeys(self, private=None):
        """generates a pair of cryptographic keys
        
        :param private: the already existing private key, defaults to None
        :type private: any, optional
        :rtype tuple(privateKey, publicKey)
        """
        pass

    @abstractmethod
    def sign(self, target):
        if self.private_key is None:
            raise ValueError("Private Key its needed for signing")

    @abstractmethod
    def verify(self, target, signature):
        if self.public_key is None:
            raise ValueError("public Key its needed for signature verification")
