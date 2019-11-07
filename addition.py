from baseSignature import baseSignature
import binascii
import secrets

class addition(baseSignature):

    # properties

    @property
    def modulo(self):
        """this modulo, using on all cryptographic operations"""
        return self._modulo

    @modulo.setter
    def modulo(self, value):
        self._modulo = value

    @modulo.deleter
    def modulo(self):
        del self._modulo
    
    #constructor (override)   
    def __init__(self, public_key=None, private_key=None, modulo=None):
        super().__init__(public_key, private_key)
        self.modulo = modulo
    

    # methods (override)
    def hashString(self,target, encoding='utf-8'):
        """returns the hash of the target string
        :param target: the string to hash
        :type target: str
        :rtype int32
        """
        target_bytes=bytes(target, encoding)
        return binascii.crc32(target_bytes)

    def makeKeys(self, private=None, modulo=None):
        # set the instance value to the parameters if they are provided
        if modulo:
            self.modulo = modulo

        if self.modulo is None:
            # the modulo is needed as part as the formula for the encryption,
            # it is the base of the public key schema as it gives the necessary
            # mathematical properties for it to work
            raise ValueError("Modulo its needed for the generation of the keys")

        if private:
            self.private_key = private
        else:
            # get a cryptographically secure private key
            # it must be any number less than the modulo
            self.private_key = secrets.randbelow(self.modulo)
        
        # pubic key must be the inverse of the private key such as both keys
        # computed together result in the identity element
        # in the case of this demo algorithm, the operation will be defined 
        # by the formula ´a + b mod c = 0´ where a is the private key, b is the 
        # public key and c is the field or modulo of the operation so the 
        # identity would be 0. as the keys would be positive integers only,
        # the public key must be the module minus the private key.
        #
        # this is not a secure formula and is only intended for academic use
        # as the modulo is public one could derive the private key substracting
        # the public key from the modulo, ideally it should be way harder to do
        # this, RSA for an instance is based on the product of to large prime
        # numbers, this makes deriving the private key from the public key
        # almost impossible
        self.public_key = self.modulo - self.private_key

        # return a tuple containing both keys
        return self.private_key, self.public_key

    def sign(self, target):
       super().sign(target)

       # in asymmetric cryptography the public key is used to cipher the data
       # and the private to decipher, this ensures only the holder of the
       # private key can decipher the message.
       #
       # to sign the private key is used to cipher a hash of the message
       # and the public key is used to decipher the hash and compare it against
       # the message

       # hash the message to have an small easy to cipher and constant output
       digest = self.hashString(target)

       # this implementation uses crc32, this means digest is now an integer
       # it can now be plug into the formula, replacing for one of the keys in
       # this case the public key will be replaced by the hash, the properties
       # of the mod allows to do this
       
       signature = (digest + self.private_key) % self.modulo

       return signature
    
    def verify(self, target, signature):
        super().verify(target, signature)
        # to verify we use private key to decrypt the hash and compare it
        # against a freshly calculated one

        signature = (signature + self.public_key) % self.modulo
        digest = self.hashString(target)
        return signature == digest, signature, digest 

def main():
    from termcolor import colored
    import termAux
    # for colors in windows
    import colorama
    colorama.init()

    # modulo must be a prime to ensure the probability of colission is low
    # it also should be bigger than the hash to keep the colissions low
    big_prime = 4386756709 # this is a 33 bit prime number
    instance = addition(modulo=big_prime)
    target_str = "anita lava la tina"
    print("modulo:", colored(instance.modulo, 'cyan'))
    print("keys:", termAux.colorTuple(instance.makeKeys(), ['yellow','green']))
    print("target:", colored(target_str, 'magenta'))
    print("CRC:", colored(instance.hashString(target_str), 'cyan'))
    signature = instance.sign(target_str)
    print("signature:", colored(signature, "cyan"))

    verification_colors = [termAux.colorBoolean, "blue", "cyan"]

    print("verification:", 
          termAux.colorTuple(instance.verify(target_str, signature),
                             verification_colors
                            )
         )
    print("verification",
          termAux.colorTuple(("failed for control",), "yellow"),
          ":",
          termAux.colorTuple(instance.verify(target_str + "a", signature),
                  verification_colors
                 )
         )

if __name__ == '__main__':
    main()