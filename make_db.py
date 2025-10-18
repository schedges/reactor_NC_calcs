#Code to query relevant data from https://www-nds.iaea.org/relnsd/v1/data?
#which seems to be an easier approach than dealing with pyensdf, raw ensdf databases, nudel, etc.
import os
import requests
import time

#Make folder structure
if not os.path.exists("data"):
  os.mkdir("data")

subFolders = ["ground_states","levels","gammas","beta_ms","beta_ps"]
for subFolder in subFolders:
  if not os.path.exists("data/"+subFolder):
    os.mkdir("data/"+subFolder)

#Helper function for querying database
def queryAPI(destination,arg):
  basePath = "https://www-nds.iaea.org/relnsd/v1/data?"
  #Check if destination already exists
  if os.path.exists(destination):
    return
  try:
    print("Downloading...")
    r = requests.get(basePath+arg, timeout=10)
    if r.text.strip() == "5":
      print("Returned 5")
      return
    with open(destination,"w") as outFile:
      outFile.write(r.text)
    time.sleep(0.1)
  except Exception:
    print("Exception")
    return
  
################
#Initial query:#
################
queryAPI("data/all.csv",arg="fields=ground_states&nuclides=all")

#Open that CSV, make a dict of ground states
if os.path.exists("data/all.csv"):
  gnd_states = []
  with open("data/all.csv","r") as csvFile:
    for iline,line in enumerate(csvFile):
      if iline>0:
        line=line.strip("\n")
        if not line=="":
          lineParts = line.split(",")
          gnd_state = {}
          gnd_state["Z"] = int(lineParts[0])
          gnd_state["N"] = int(lineParts[1])
          gnd_state["A"] = gnd_state["Z"]+gnd_state["N"]
          gnd_state["symbol"] = lineParts[2]
          decay_1 = lineParts[18]
          decay_2 = lineParts[21]
          decay_3 = lineParts[24]
          decay_channels = []
          if not decay_1=="":
            decay_channels.append(decay_1)
          if not decay_2=="":
            decay_channels.append(decay_2)
          if not decay_3=="":
            decay_channels.append(decay_3)
          gnd_state["decay_channels"] = decay_channels
          gnd_states.append(gnd_state)

########################
##Query excited states##
########################
for gnd_state in gnd_states:
  isotope=f"{gnd_state['A']}{gnd_state['symbol']}"
  print(f"querying levels for {isotope}")
  queryAPI(f"data/levels/{isotope}.csv",arg=f"fields=levels&nuclides={isotope}")

################
##Query gammas##
################
for gnd_state in gnd_states:
  isotope=f"{gnd_state['A']}{gnd_state['symbol']}"
  print(f"querying gammas for {isotope}")
  queryAPI(f"data/gammas/{isotope}.csv",arg=f"fields=gammas&nuclides={isotope}")
  time.sleep(0.1)

########################
##Query decay channels##
########################
for gnd_state in gnd_states:
  isotope=f"{gnd_state['A']}{gnd_state['symbol']}"
  print(f"querying decays for {isotope}")
  if "EC" in gnd_state["decay_channels"]:
    queryAPI(f"data/beta_ps/{isotope}.csv",arg=f"fields=decay_rads&nuclides={isotope}&rad_types=bp")
  if "B-" in gnd_state["decay_channels"]:
    queryAPI(f"data/beta_ms/{isotope}.csv",arg=f"fields=decay_rads&nuclides={isotope}&rad_types=bm")
  time.sleep(0.1)

