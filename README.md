# AWS-tset
``` 
pip install virtualenv  
sudo /usr/bin/easy_install virtualenv  
source ~/.virtualenvs/chalice-demo/bin/activate

sudo apt-get install httpie

deactivate
``` 


``` 
brew install awscli
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

### 1-1. install 'brew'  
``` 
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

### 1-2. Installing Java 8
Visit website: http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html  

``` 
export JAVA_HOME=$(/usr/libexec/java_home)
$ echo $JAVA_HOME
/Library/Java/JavaVirtualMachines/1.7.0.jdk/Contents/Home
```

```
brew cask install java
```
verify the java version
``` 
brew cask info java
```


### 1-3. install python (pip/pip3)
``` 
brew install python
sudo easy_install pip
```  


### 1-4. install boto3 

``` 
sudo easy_install nose
sudo easy_install tornado
sudo -H pip install --ignore-installed six
sudo pip install boto3
```

### 1-5. install jq
``` 
brew install jq  
(optional)sudo apt-get install build-essential  
echo 'export PATH="/home/linuxbrew/.linuxbrew/bin:$PATH"' >>~/.bash_profile  
echo 'export MANPATH="/home/linuxbrew/.linuxbrew/share/man:$MANPATH"' >>~/.bash_profile  
echo 'export INFOPATH="/home/linuxbrew/.linuxbrew/share/info:$INFOPATH"' >>~/.bash_profile  
PATH="/home/linuxbrew/.linuxbrew/bin:$PATH"  
brew install gcc  
brew help  
```

### 1-6. install Chalice and httpie
``` 
brew install httpie

sudo pip install virtualenv
virtualenv ~/.virtualenvs/chalice-demo
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

Credentials
``` 
mkdir ~/.aws
cat >> ~/.aws/config
[default]
aws_access_key_id=YOUR_ACCESS_KEY_HERE
aws_secret_access_key=YOUR_SECRET_ACCESS_KEY
region=YOUR_REGION (such as us-west-2, us-west-1, etc)
```
or
``` 
aws configure

``` 
check the credentials
``` 
aws sts get-caller-identity
```

Not in virtualenv,
``` 
sudo pip install awsebcli --upgrade --ignore-installed six
sudo pip install chalice
```


## Note  
- rule name can not include '-' (use '_')  
- 



reference 
Java installaion & java home setting: https://www.mkyong.com/java/how-to-set-java_home-environment-variable-on-mac-os-x/
python: https://www.python.org/downloads/mac-osx/ 
boto3: https://github.com/boto/boto3  
Chalice: https://github.com/aws/chalice 
httpie: https://gist.github.com/BlakeGardner/5586954


https://chalice.readthedocs.io/en/latest/topics/cfn.html
