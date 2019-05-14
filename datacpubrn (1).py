#!/usr/bin/python

import shutil,os,sys,time,random

def cpuburn(comptime):
  t1=time.time()
  t2=t1+comptime

  maxr=8

  a=0.0
  t=time.time()
  while (t<t2):
    ta=t
    for b in range(1,maxr):
      a=a+(t+b)/t
    t=time.time()

    # automatically adapt internal loop
    if ((t-ta)<(comptime/64.0)):
      maxr*=4

def copyrun(fname, comptime, time):
  shutil.copyfile(fname,"./a.tmp")
  cpuburn(comptime)
  os.remove("./a.tmp")
  wall_time(time)
  
def seqrun(fname, comptime, blocksize, filesize, time):
  nblocks = int(filesize/blocksize)
  dcomptime = comptime*1.0/nblocks

  with open(fname,"rb") as fd:
    for n in range(nblocks):
      dummy = fd.read(blocksize)
      cpuburn(dcomptime)
      wall_time(time)

def skiprun(fname, comptime, readbytes, blocksize, filesize, time):
  nblocks = int(filesize/blocksize)
  dcomptime = comptime*1.0/nblocks

  with open(fname,"rb") as fd:
    for n in range(nblocks):
      dummy = fd.read(readbytes)
      fd.seek(blocksize-readbytes,1) # relative
      cpuburn(dcomptime)
      wall_time(time)

def randomrun(fname, comptime, readbytes, nreads, filesize, time):
  random.seed(1) # deterministic

  dcomptime = comptime*1.0/nreads

  with open(fname,"rb") as fd:
    for n in range(nreads):
      sp = random.randrange(0,filesize-readbytes-1)
      fd.seek(sp,0) # abs position
      dummy = fd.read(readbytes)
      cpuburn(dcomptime)
      wall_time(time)

def wall_time(start_time):
  w_time = time.time() - start_time
  print("Wall time %i" %w_time)


# Fix area to read from
basedir="/cvmfs/gwosc.osgstorage.org/gwdata/O2/strain.16k/hdf.v1/H1/1163919360/"
files=["H-H1_GWOSC_O2_16KHZ_R1-1164779520-4096.hdf5",
"H-H1_GWOSC_O2_16KHZ_R1-1164713984-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164722176-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164726272-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164709888-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164693504-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164701696-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164705792-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164775424-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164824576-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164828672-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164689408-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164820480-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164840960-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164832768-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164836864-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164857344-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164861440-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164816384-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164849152-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164865536-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164845056-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164869632-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164771328-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164685312-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164873728-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164877824-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164881920-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164886016-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164898304-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164890112-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164894208-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164902400-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164910592-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164906496-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164914688-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164918784-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164681216-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164922880-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164931072-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164926976-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164935168-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164939264-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164943360-4096.hdf5",
#3"H-H1_GWOSC_O2_16KHZ_R1-1164947456-4096.hdf5",
#3"H-H1_GWOSC_O2_16KHZ_R1-1164677120-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164963840-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164599296-4096.hdf5",
#"H-H1_GWOSC_O2_16KHZ_R1-1164570624-4096.hdf5",
"H-H1_GWOSC_O2_16KHZ_R1-1164562432-4096.hdf5"]
fsizeall = 515637248

file_process_time=20.0
modestr="copyrun"

if len(sys.argv)<3:
  print("ERROR: Not enough parameters")
  print("Usage:")
  print("  datacpubrn.py cpusecs mode [modeargs]")
  print("where")
  print("  mode is either copyrun, seqrun, skiprun or randomrun")
  sys.exit(1)

file_process_time=float(sys.argv[1])
modestr=sys.argv[2][0:]

if modestr=="copyrun":
  #ignore any other arg
  print("Using mode %s"%modestr)
elif modestr=="seqrun":
  if len(sys.argv)<4:
    print("ERROR: Not enough parameters")
    print("Usage:")
    print("  datacpubrn.py cpusecs seqrun blocksize")
    sys.exit(1)
  seqrun_blocksize = int(sys.argv[3])
  print("Using mode %s, block size of %i"%(modestr,seqrun_blocksize))
elif modestr=="skiprun":
  if len(sys.argv)<5:
    print("ERROR: Not enough parameters")
    print("Usage:")
    print("  datacpubrn.py cpusecs skiprun readsize skipblock")
    sys.exit(1)
  skiprun_readsize = int(sys.argv[3])
  skiprun_blocksize = int(sys.argv[4])

  print("Using mode %s, read size of %i, skip block of %i"%(modestr,skiprun_readsize,skiprun_blocksize))
elif modestr=="randomrun":
  if len(sys.argv)<5:
    print("ERROR: Not enough parameters")
    print("Usage:")
    print("  datacpubrn.py cpusecs randomrun readsize nreads")
    sys.exit(1)
  randomrun_readsize = int(sys.argv[3])
  randomrun_nreads = int(sys.argv[4])

  print("Using mode %s, read size of %i, %i reads"%(modestr,randomrun_readsize,randomrun_nreads))
else:
  print("ERROR: Unknown mode '%s'"%modestr)
  sys.exit(1)

s_time = time.time()
print("Processing %i files (%.1fGB total), CPU usage %.1fs (total %.1fs)"%(len(files),len(files)*fsizeall/(1024.0*1024*1024), file_process_time, len(files)*file_process_time))

for f1 in files:
  print("%i %s"%(time.time(),f1))
  fp = os.path.join(basedir,f1)
  if modestr=="copyrun":
    copyrun(fp,file_process_time,s_time)
  elif modestr=="seqrun":
    seqrun(fp,file_process_time,seqrun_blocksize,fsizeall,s_time)
  elif modestr=="skiprun":
    skiprun(fp,file_process_time,skiprun_readsize,skiprun_blocksize,fsizeall,s_time)
  elif modestr=="randomrun":
    randomrun(fp,file_process_time,randomrun_readsize,randomrun_nreads,fsizeall,s_time)
  else:
    print("ERROR: Unknown mode '%s'"%modestr)
    sys.exit(1)

wall_time(s_time)

#w_time = time.time() - s_time
# print("%i" %w_time)

