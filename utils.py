#Helper functions for calculating B(GT0) matrix elements
import numpy as np
import math
  
m_e = 0.51099895069 #MeV/c
amu_to_MeV = 931.49410242

class GroundState:
  def __init__(self,*,Z,N,symbol,twoJ,parity,twoT,mass,mass_unc):
    self.Z = Z
    self.N = N
    self.symbol = symbol
    self.twoJ = twoJ
    self.parity = parity
    self.twoT = twoT
    self.mass = mass
    self.mass_unc = mass_unc

class Level:
  def __init__(self,*,energy,m1,isospin,twoJ,parity):
    self.energy = energy
    self.m1 = m1
    self.isospin = isospin
    self.twoJ = twoJ
    self.parity = parity

def parseJP(JP):
  JP = JP.strip("(")
  JP = JP.strip(")")
  lineParts = JP.split()
  if len(lineParts)==1:
    parity = lineParts[0][-1]
    if parity=="+":
      parity = 1
    elif parity=="-":
      parity=-1
    twoJ = lineParts[0][0:-1]
    if "/" in twoJ:
      parts = twoJ.split("/")
      numerator = int(parts[0])
      denominator = int(parts[1])
      twoJ = int((2*numerator)/denominator)
    elif not twoJ=="":
      twoJ = 2*int(twoJ)
    else:
      return None,None
    return twoJ,parity
  else:
    return None,None
  
def parseT(T):
  if T=="":
    return None
  elif "/" in T:
    parts = T.split("/")
    numerator = int(parts[0])
    denominator = int(parts[1])
    T = int((2*numerator)/denominator)
    return T
  else:
    return int(T)
  
def parseGroundStates(fname):
  ground_states = np.zeros((200,200),dtype=object)
  with open(fname,"r") as inpFile:
    for iline,line in enumerate(inpFile):
      if iline>0 and not line=="" and not line==" ":
        line=line.strip("\n")
        lineParts = line.split(",")
        if len(lineParts)==55:
          if lineParts[12] == "STABLE":
            Z = int(lineParts[0])
            N = int(lineParts[1])
            symbol = lineParts[2]
            JP = lineParts[11]
            twoJ,parity = parseJP(JP)
            T = lineParts[27]
            twoT = parseT(T)
            mass = float(lineParts[46])
            mass_unc = float(lineParts[47])
            ground_states[Z][N] = GroundState(Z=Z,N=N,symbol=symbol,twoJ=twoJ,parity=parity,twoT=twoT,mass=mass,mass_unc=mass_unc)
  return ground_states

def parseGammas(symbol):
  levels = []
  #Get level energy, M1, twoJ, p
  with open(f"data/gammas/{symbol}.csv","r") as inpFile:
    for iline,line in enumerate(inpFile):
      print()
      
  #Get isospin
  with open(f"data/levels/{symbol}.csv","r") as inpFile:
    for iline,line in enumerate(inpFile):
      print()

  return []