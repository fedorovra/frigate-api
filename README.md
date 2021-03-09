# frigate-api
#
###
### Команды для установки окружения
###

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh  
bash Miniconda3-latest-Linux-x86_64.sh  
/usr/local/miniconda3/bin/conda init  
git clone https://github.com/fedorovra/frigate-api.git  
/usr/local/miniconda3/bin/conda env create -f /root/frigate-api/frigate-api.yml  

/bin/bash /root/iptables.rules   
/bin/bash /root/frigate-api/launcher.sh   

