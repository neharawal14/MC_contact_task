import os
#list_of_files= ["HIG-RunIISummer20UL16wmLHEGEN-13208"]
list_of_files= ["HIG-RunIISummer20UL16wmLHEGEN-13174","HIG-RunIISummer20UL16wmLHEGEN-13201","HIG-RunIISummer20UL16wmLHEGEN-13208","HIG-RunIISummer20UL16wmLHEGEN-13212","HIG-RunIISummer20UL16wmLHEGEN-13213","HIG-RunIISummer20UL16wmLHEGEN-13214","HIG-RunIISummer20UL16wmLHEGEN-13215","HIG-RunIISummer20UL16wmLHEGEN-13216","HIG-RunIISummer20UL16wmLHEGEN-13217","HIG-RunIISummer20UL16wmLHEGEN-13218"]
path = "/afs/cern.ch/user/n/nrawal/public/Gridpacks/new_tqH_submit/"
for fragment_name in list_of_files:
  os.chdir(f"{path}")
  os.system(f"mkdir {fragment_name}")
  os.chdir(f"{fragment_name}")
  os.system(f"wget https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/{fragment_name}")
  os.system(f"mv {fragment_name} test_command.sh")
  os.system("sed -i 's/=6720/=1200/' test_command.sh")
  os.system("chmod +x test_command.sh")
  f=open("submit_test.sh","w")
  f.write("#!/usr/bin/env bash \n")
  f.write("cd {}/ \n".format(path+fragment_name))
  f.write("source test_command.sh >> {}/output.txt \n".format(path+fragment_name))
  f.close()
  os.system("chmod +x submit_test.sh")
  f_condor = open("condor.sub","w")
  f_condor.write("executable = submit_test.sh \n")
  f_condor.write("should_transfer_files   = Yes \n")
  f_condor.write("when_to_transfer_output = ON_EXIT \n")
  f_condor.write("output= Out.out \n")
  f_condor.write("error = Out.err \n")
  f_condor.write("log  = Out.log \n")
  f_condor.write("+MaxRuntime = 9000 \n")
  f_condor.write("queue")
  f_condor.close()
  os.system("condor_submit condor.sub")
