# AWS-tset
``` 
pip install virtualenv  
sudo /usr/bin/easy_install virtualenv  
source ~/.virtualenvs/chalice-demo/bin/activate

sudo apt-get install httpie

deactivate
``` 


``` 
sudo apt install linuxbrew-wrapper  
brew install jq  
sudo apt-get install build-essential  
echo 'export PATH="/home/linuxbrew/.linuxbrew/bin:$PATH"' >>~/.bash_profile  
echo 'export MANPATH="/home/linuxbrew/.linuxbrew/share/man:$MANPATH"' >>~/.bash_profile  
echo 'export INFOPATH="/home/linuxbrew/.linuxbrew/share/info:$INFOPATH"' >>~/.bash_profile  
PATH="/home/linuxbrew/.linuxbrew/bin:$PATH"  
brew install gcc  
brew help  
```

``` 

svn ls https://github.com/getcarvi/Codes/trunk/environment/test  
svn export https://github.com/getcarvi/Codes/trunk/environment/test  

```

# OS installation  
## 1. Install enviroment
Website: https://brew.sh/ 

install 'brew'  
``` 
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
install python (pip)
``` 
brew install python
```

install Chalice and httpie
``` 
brew install httpie

pip install virtualenv  
sudo /usr/bin/easy_install virtualenv  
source ~/.virtualenvs/chalice-demo/bin/activate

# Double check you have python3.6
$ which python3.6
/usr/local/bin/python3.6
virtualenv --python /usr/local/bin/python3.6 ~/.virtualenvs/chalice-demo
source ~/.virtualenvs/chalice-demo/bin/activate
```

Next, in your virtualenv, install chalice:

``` 
pip install chalice
chalice --help

```
## Credentials
``` 
$ mkdir ~/.aws
$ cat >> ~/.aws/config
[default]
aws_access_key_id=YOUR_ACCESS_KEY_HERE
aws_secret_access_key=YOUR_SECRET_ACCESS_KEY
region=YOUR_REGION (such as us-west-2, us-west-1, etc)
```




reference 
python: https://www.python.org/downloads/mac-osx/ 
Chalice: https://github.com/aws/chalice 
httpie: https://gist.github.com/BlakeGardner/5586954
