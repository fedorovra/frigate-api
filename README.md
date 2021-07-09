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

cat > /etc/systemd/system/gunicorn.service << END
### BEGIN ANSIBLE MANAGED BLOCK
[Unit]  
Description=gunicorn daemon  
After=network.target  
[Service]  
User=root  
Group=root  
WorkingDirectory=/root/frigate-api  
ExecStart=/usr/local/miniconda3/envs/frigate-api/bin/gunicorn --worker-class gthread --reload --bind '0.0.0.0:1025' --workers 5 --threads 10 api.wsgi  
ExecReload=/bin/kill -s HUP $MAINPID  
KillMode=mixed  
TimeoutStopSec=5  
Restart=always  
RestartSec=30  
[Install]  
WantedBy=default.target  
### END ANSIBLE MANAGED BLOCK  
END  

systemctl start gunicorn.service; systemctl enable gunicorn.service  

/bin/bash /root/iptables.rules   
/bin/bash /root/frigate-api/launcher.sh   

conda activate frigate-api   
   
pip install mobile-balance  
   
   
В файле "/usr/local/miniconda3/envs/frigate-api/lib/python3.7/site-packages/mobile_balance/megafon.py" строка 16  
было:  
csrf_token = re.search(r'name="CSRF" value="(.*?)"', response.content)  
стало:  
csrf_token = re.search(r'name="CSRF" value="(.*?)"', response.content.decode("utf-8"))  
