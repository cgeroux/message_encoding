#!/usr/bin/env python3
from __future__ import print_function
import optparse as op
import sys

class Random():
  """Provides a version independent random number generator
  """
  
  def __init__(self):
    """Based on the pseudocode in 
    https://en.wikipedia.org/wiki/Mersenne_Twister. Generates uniformly 
    distributed 32-bit integers in the range [0, 2^32 - 1] with the MT19937 
    algorithm.
    """
  
    self.MT = [0 for i in range(624)]
    self.index = 0
    
    # To get last 32 bits
    self.bitmask_1 = (2 ** 32) - 1
    
    # To get 32. bit
    self.bitmask_2 = 2 ** 31
    
    # To get last 31 bits
    self.bitmask_3 = (2 ** 31) - 1
    self.maxInt=2**32-1
  def _genNums(self):
    """Generate an array of 624 untempered numbers
    """
    
    for i in range(624):
        y=(self.MT[i]&self.bitmask_2)+(self.MT[(i+1)%624]&self.bitmask_3)
        self.MT[i]=self.MT[(i+397)%624]^(y>>1)
        if y%2 != 0:
            self.MT[i] ^= 2567483615
  def seed(self,number):
    """Initialize the generator from a seed
    """
    
    assert(type(number)==type(0))
    
    self.MT[0] = number
    for i in range(1,624):
        self.MT[i]=((1812433253*self.MT[i-1])^((self.MT[i-1]>>30)+i)) \
          &self.bitmask_1
  def getNum(self,min=0,max=2**32-1):
    """Extract a tempered pseudorandom number based on the index-th value,
    calling _genNums() every 624 numbers
    """
    
    if self.index == 0:
        self._genNums()
    y = self.MT[self.index]
    y ^= y >> 11
    y ^= (y << 7) & 2636928640
    y ^= (y << 15) & 4022730752
    y ^= y >> 18

    self.index = (self.index + 1) % 624
    return int(float(y)/float(self.maxInt)*(float(max)-float(min))+float(min))
def addParserOptions(parser):
  """Adds command line options
  """
  
  parser.add_option("--key",type="int",dest="encryptionKey",help="Sets the "
    +"encryption key [default: %default].",default=0)
  parser.add_option("-e",action="store_true",dest="encode",help="Indicates "
    +"that the given string should be encoded [not default].",default=False)
  parser.add_option("-d",action="store_false",dest="encode",help=" [default].")
def parseOptions():
  """Parses command line options
  """
  
  parser=op.OptionParser(usage="Usage: %prog [options] STRING"
    ,version="%prog 1.0",description="Encrypts and decrypts the given STRING."
    +"Encodings are not consistent between python2 and python3.")
  
  #add options
  addParserOptions(parser)
  
  #parse command line options
  return parser.parse_args()
def decrypt(encryptedString,key="0"):
  '''Decrypts a given string'''
  
  decryptedString=""
  random=Random()
  random.seed(key)
  for encryptedChar in encryptedString:
    shift=random.getNum(1,4)
    decryptedString+=chr(ord(encryptedChar)-shift)
  return decryptedString
def encrypt(inputString,key="0"):
  '''Encrypts a given string'''
  
  encryptedString=""
  random=Random()
  random.seed(key)
  for inputChar in inputString:
    shift=random.getNum(1,4)
    encryptedString+=chr(ord(inputChar)+shift)
  return encryptedString
def main():
  
  #parse command line options
  (options,args)=parseOptions()
  
  #check we got the expected number of arguments
  if (len(args)!=1):
    raise Exception("Expected a string.")
  
  #do the encryption/decryption
  if options.encode:
    print(encrypt(args[0],key=options.encryptionKey))
  else:
    print(decrypt(args[0],key=options.encryptionKey))

if __name__=="__main__":
  main()