## Reverse tunnelling usage

### Usage Context
On a remote work context one solution is to use teamViewer but if you are *NIX user, one other solution is to implement
a couple of tools / script to access your Office computer in more usable / convenient way especially if your office computer 
is behind a NAT or a firewall.

Basically it consists of using reverse tunnelling  technique and open a ssh connection from your office computer to your home 
computer and redirect some useful protocol throw this ssh connection 

### Prerequisites
- [XUbuntu](https://xubuntu.org/) > 18 in the 2 sides
- Download this repository in /home/<user>/ folder
- Your Home router must be accessible and should have port-forwarding capabilities
- Optionally have a no-ip account if your router can deal with it, a ngrok account can do the job to have a fix address for your home computer
- For Methode 2 by using a Telegram bot, install Python and these libraries (This means that you must have a [Telegram](https://telegram.org/) account):
    - subprocess
    - configparser
    - requests
    - teleport
#### In the home computer side
1. Configure the port forwarding in the home router [Here an exemple](https://www.cyberpratibha.com/blog/ssh-port-forwarding-in-router/)
2. (Optional) configure a no-ip account in your router if its available
3. (Optional) you can ignore the 1 and 2 steps  by only using [ngrok](https://ngrok.com/) account directly in your home computers
4. Use your no-ip or ngrock dns as ssh server (Please see the config.ini file)
4. Install a nvcClient [RealVnc viewr](https://www.realvnc.com/en/connect/download/viewer/)

### Methode 1 Using Cron Steps  In the office computer side
1. Install x11vnc vnc server.
2. set the x11vnc password `x11vnc -storepasswd`.
3. stop the x11vnc `ps aux | grep '[u]sr.*bin/x11vnc' | awk {'print $2'} | xargs kill -9`.
4. Create /lib/systemd/system/x11vnc.service and paste the x11vnc.service file content.
5. `sudo systemctl daemon-reload`.
6. `sudo service x11vnc start`.
7. Remove the default gnome-screensaver `sudo apt remove gnome-screensaver`.
8. Install the xscreensaver : `sudo apt-get install xscreensaver`.
9. Make it default lock screen [here a tutorial](https://www.linuxbabe.com/ubuntu/install-autostart-xscreensaver-ubuntu-18-04-19-04).
10. Make it  possible to ssh your home computer without a password  [here a tutorial](https://www.thegeekstuff.com/2008/11/3-steps-to-perform-ssh-login-without-password-using-ssh-keygen-ssh-copy-id/).
11. Edit the tunnelling.sh in your convenience by replacing expected parameters (SERVER=$1, USER=$2, ... etc) with correct value.
12. configure the cron jobs :

    `*/5 8-18 * * 1-6 ~/reversetunnelling/tunnelling.sh >> /var/log/tunelingssh.log 2>&1
    */5 8-18 * * 1-6 ~/reversetunnelling/localProxy.sh >> /var/log/localproxyssh.log 2>&1`
    
    Here we execute the .sh scripts every 5 min between 8AM and 6pm from Monday to Saturday.

### Methode 2 using Telegram Bot in the office computer side
#### Motivation
In some circumstance as your office desktop cron try to establish a ssh connection every 5 min, your organization firewall, can detected this as non legit action
and your sysAdmin can decide to block this connection by blacklisting your office desktop ip or by disallowing used port (True story :grin: ) .

A more effective solution is to lunch the tunnelling on demand, inspired by this [tutorial](https://www.instructables.com/id/Set-up-Telegram-Bot-on-Raspberry-Pi/).
In this Method, user can provide a specific port to use
TODO: 
- [x] User can provide a specific port   
- [x] User can provide a specific server    
- [ ] User can provide a specific user
- [ ] any other useful options 
        
#### Steps
1. Perform the 1 to 10 steps from Method 1
2. Flow this tutorial to create a [Telegram Bot](https://core.telegram.org/bots#6-botfather)
3. Edit the config.ini cordially, please pay attention to the 'permitteduser_id' that is the unique Telegram User that can interact with the Bot
4. Create /lib/systemd/system/tunnelling.service and paste the tunnelling.service file content.
5. Edit the /lib/systemd/system/tunnelling.service in your convenience by replacing the <user> with your home user folder
6. `sudo systemctl daemon-reload`.
7. `sudo service tunnelling start`.
8. Interact with the Bot from you Telegram messaging app by:
    - Start ssh tunnelling : `Ssh run`
    - Start ssh tunnelling : `Ssh run port:200,` (You can specify the ssh port to use)
    - Stop ssh tunnelling : `Ssh stop`
    - If not possible to use Dynamic DNS we can use [NgRok](http://ngrok.com), lunch the ./ngrok tcp [port] and use the generated [server]:[port] in the following command
      `Ssh run port:[ngrokPort],server:[ngrokServer],` to stop the ssh tunnelling: `Ssh stop server:[ngrokServer]`
    - Any other message interaction will be responded by the Bot with a random quote

### Usage
The .sh scripts should be already launched before trying to connect back to the office computer

#### _Remote Desktop_
On the home computer open the vncViewer and add the address server as following : `127.0.0.1:5901`, you may have a field for the password of the vncServer
![nvcViewr](images/vncViewr.png)

#### _SSH back to the office computer_
`ssh localhost -p 4022`

#### _Socks Usage_
I'm using fireFox to browse to office computer installed web sites or to go to web application that only accessible from the  office computer
- Got to preferences > Network Settings > Settings
- Select 'Manual proxy configuration'
- In the 'SOCKS Host' field:127.0.0.1 
- In the 'Port' field : 6666
- Select the SOCKS v5 option 
![nvcViewr](images/socksConfig.png)

### Security Note
As we use the SSH connection we assume that this technique can be safe, due to the nature of ssh encrypted and secured behavior.

In addition, by configuring the cron jobs to work only on open office time, that's means the ssh connection is under the user control.

Adding a secure layer with a vncSever password can be useful, also, don't forgot to lock the office computer session via Vnc, once you finish your task  

### References
- xscreensaver : [screen saver installation](https://www.linuxbabe.com/ubuntu/install-autostart-xscreensaver-ubuntu-18-04-19-04)
- x11vnc : [x11vncserver installation](https://c-nergy.be/blog/?p=12220)
- ssh : [SSH tunnelling](https://www.ssh.com/ssh/tunneling/example)
