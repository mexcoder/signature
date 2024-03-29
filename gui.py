import os
import sys
import pygubu
import termAux
import colorama # for colors in windows
import tkinter as tk
from sympy import randprime
from termcolor import colored
from tkinter import messagebox

from addition import addition
from product import product

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

class MyApplication:

    def __init__(self, signatureGenerator, primeBounds):
        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file(os.path.join(CURRENT_DIR, 'main.ui'))
        
        # 3: Create the toplevel widget.
        self.mainwindow = builder.get_object('mainwindow')

        # 4: Connect Callbacks
        builder.connect_callbacks(self)

        # 5: Configure layout of the master. Set master resizable:
        self.mainwindow.rowconfigure(0, weight=1)
        self.mainwindow.columnconfigure(0, weight=1)

        # extra elements
        self.generator = signatureGenerator
        self.primeBounds = primeBounds
        self.messageBox = builder.get_object('Text_1')


    def quit(self, event=None):
        self.mainwindow.quit()

    def run(self):
        self.mainwindow.mainloop()

    def makeModulo(self):
        _modulo = randprime(*self.primeBounds)
        self.modulo = _modulo
        print("modulo:", colored(_modulo, 'cyan'))

    def makeKeys(self):
        keys = self.generator.makeKeys(private=self.private_key)
        self.private_key, self.public_key = keys
        print("keys:", termAux.colorTuple(keys, ['yellow','green']))

    
    def generateSignature(self):
        self.signature = self.generator.sign(self.message)
        print("target:", colored(self.message, 'magenta'))
        print("CRC:", colored(self.generator.hashString(self.message), 'cyan'))
        print("signature:", colored(self.signature, "cyan"))

    def verifySignature(self):
        verification_colors = [termAux.colorBoolean, "blue", "cyan"]
        status = self.generator.verify(self.message,self.signature)
        if status[0]:
            msg = messagebox.showinfo
        else:
            msg = messagebox.showerror

        msg("Resultado de la verificacion",
            "Firma valida: {}\n"
            "CRC Recuperado: {}\n"
            "CRC Calculado: {}".format(*status))

        print("verification:", termAux.colorTuple(status, verification_colors))

    @property
    def modulo(self):
        value = self.builder.tkvariables["modulo"].get()
        value = value.strip()

        if value == "":
            value = None

        self.generator.modulo = value
        try:
            return int(value)
        except:
            return value

    @modulo.setter
    def modulo(self, value):
        self.builder.tkvariables["modulo"].set(value)
        self.generator.modulo = value
    
    @property
    def private_key(self):
        value = self.builder.tkvariables["private_key"].get()
        value = value.strip()

        if value == "":
            value = None

        self.generator.private_key = value
        try:
            return int(value)
        except:
            return value

    @private_key.setter
    def private_key(self, value):
        self.builder.tkvariables["private_key"].set(value)
        self.generator.private_key = value
        
    @property
    def public_key(self):
        value = self.builder.tkvariables["public_key"].get()
        value = value.strip()
        
        if value == "":
            value = None

        self.generator.public_key = value
        try:
            return int(value)
        except:
            return value

    @public_key.setter
    def public_key(self, value):
        self.builder.tkvariables["public_key"].set(value)
        self.generator.public_key = value
    
    @property
    def message(self):
        return self.messageBox.get("1.0",tk.END).strip()

    @message.setter
    def message(self, value):
        self.messageBox.set(value)

    @property
    def signature(self):
        value = self.builder.tkvariables["signature"].get()
        value = value.strip()
        try:
            return int(value)
        except:
            return value

    @signature.setter
    def signature(self, value):
        self.builder.tkvariables["signature"].set(value)


if __name__ == '__main__':

    colorama.init()
    
    if len(sys.argv) > 1 and sys.argv[1] == "product":
        signer = product()
        modulo = 1014265245160156964
        bounds = 2**60, 2**64
    else:
        signer = addition()
        modulo = 4386756709
        bounds = 2**32,2**40

    app = MyApplication(signer, bounds)
    app.modulo = modulo

    ready = False
    while not ready:
        try:
            app.makeKeys()
        except ValueError as e:
            print(colored("Exception while trying to generate the keys", "red"))
            print(colored(str(e),"red"))
        else:
            ready = True
        
    app.run()
