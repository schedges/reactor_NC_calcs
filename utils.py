#Helper functions for calculating B(GT0) matrix elements
import numpy as np
import math
  
m_e = 0.51099895069 #MeV/c
amu_to_MeV = 931.49410242

#Ground state objects 
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
    self.levels = []
    self.decays = []

  def calcIsospinProjection(self):
    return #TODO
    
class Level:
  def __init__(self,*,Z,N,symbol,energy,twoJ,parity,m1,m1_unc):
    self.Z = Z
    self.N = N
    self.energy = energy
    self.twoJ = twoJ
    self.parity = parity
    self.m1 = m1
    self.m1_unc = m1_unc
    self.symbol = symbol

    self.decay_intensity = None
    self.decay_intensity_unc = None
    self.decay_halflife_sec = None
    self.decay_halflife_sec_unc = None
    self.decay_logft = None
    self.decay_logft_unc = None
    self.decay_isospin = None
    self.parent_Z = None
    self.parent_A = None
    self.parent_symbol = None

  def assignIsospin(self,energies,isospins):
    #Step through energies, find one closest. 
    diff = np.inf
    closestIDX = -1
    for i,energy in enumerate(energies):
      deltaE = abs(energy-self.energy)
      if deltaE < diff:
        diff = deltaE
        closestIDX = i
    if closestIDX==-1:
      self.twoT = None
    else:
      self.twoT = isospins[closestIDX]

class DecayState:
  def __init__(self,*,Z,N,symbol,twoJ,parity,twoT,decay_channels,halflife_sec,halflife_sec_unc,mass,mass_unc):
    self.Z = Z
    self.N = N
    self.symbol = symbol
    self.decay_channels = decay_channels
    self.halflife_sec = halflife_sec
    self.halflife_sec_unc = halflife_sec_unc
    self.mass = mass
    self.mass_unc = mass_unc

#Pass in either beta+ or beta- folder, get list of files, step through parsing and extracting relevant info.
#We'll store this either in bms or bps
def parseDecays(fname):
  decays = np.full((200, 200), None, dtype=object)
  with open(fname,"r") as inpFile:
    for iline,line in enumerate(inpFile):
      if iline>0:
        line=line.strip("\n")
        if not line=="":
          lineParts = line.split(",")
          if len(lineParts) == 29:
            daughter_level = float(lineParts[5])
            logft = float(lineParts[10])
            logft_unc = float(lineParts[11])
            

def parseJP(JP):
  JP = JP.replace("(", "").replace(")", "")
  JP = JP.replace("[", "").replace("]", "")
  lineParts = JP.split()

  if len(lineParts)>1:
    lineParts = lineParts[0]

  if len(lineParts)==1:
    parity = lineParts[0][-1]
    if parity=="+":
      parity = 1
    elif parity=="-":
      parity=-1
    else:
      return None,None

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
  elif "&" in T:
    return None
  elif "+" in T:
    return None
  elif " " in T:
    return None
  elif "/" in T:
    parts = T.split("/")
    numerator = int(parts[0])
    denominator = int(parts[1])
    twoT = int((2*numerator)/denominator)
    return twoT
  else:
    return 2*int(T)


def parseStableGroundStates(fname):
  ground_states = np.full((200, 200), None, dtype=object)
  with open(fname,"r") as inpFile:
    for iline,line in enumerate(inpFile):
      if iline>0:
        line=line.strip("\n")
        if not line=="" and not line==" ":
          lineParts = line.split(",")
          print(len(lineParts))
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
      if iline>0:
        line=line.strip("\n")
        if not line=="" and not line==" ":
          lineParts = line.split(",")
          if not lineParts[23]=="":
            Z = int(lineParts[0])
            N = int(lineParts[1])
            parsedSymbol = lineParts[2]
            energy = float(lineParts[4])
            JP = lineParts[10]
            twoJ,parity = parseJP(JP)
            m1 = float(lineParts[23])
            if not lineParts[24]=="":
              m1_unc = float(lineParts[24])
            else:
              m1_unc = 0
            levels.append(Level(Z=Z,N=N,symbol=parsedSymbol,energy=energy,twoJ=twoJ,parity=parity,m1=m1,m1_unc=m1_unc))
      
  #Get isospin
  energies = []
  isospins = []
  with open(f"data/levels/{symbol}.csv","r") as inpFile:
    for iline,line in enumerate(inpFile):
      if iline>0:
        line=line.strip("\n")
        if not line=="" and not line==" ":
          lineParts = line.split(",")
          if not lineParts[5]=="":
            energy = float(lineParts[5])
            T = lineParts[25]
            twoT = parseT(T)
            energies.append(energy)
            isospins.append(twoT)

  #Assign:
  for ilev,level in enumerate(levels):
    levels[ilev].assignIsospin(energies,isospins)
  
  return levels

#TODO
def calcCGCoefficient():
  return