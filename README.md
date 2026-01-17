# Setup  
## Main components of the setup of a new computer are -:  
1.) Settings and accounts which are usually on the icloud settings and thus can be directly imported on the new computer.  
2.) Passwords and apps which are again usually imported by icloud directly on its own.  
3.) Workflow setup that is reconfiguring the terminal, competitive programming setup and ide's for projects and also university/office workspace.  
4.) The university/ office workspace should usually be on the cloud so the only job is to login the cloud.  
   
The repository focuses on setting up the computer's terminal, vpn, competitive programming setup and the ide for creating projects and latex and other things.   
## Terminal Setup  
Beware that there are a lot of file name dependent aliases in the zshrc, so kindly update those aliases as per requirement and naming of folders.  
Use the zshrc for the ohmyzsh and get the zsh from brew. That is all. Also then install mvim and paste the vimrc file in the vimrc file and also in mvimrc file. To check where vimrc file resides run the command :   
``` bash
vim --version
```
You will see at the bottom the location of vimrc. Only one of those files I believe is writable so just write/ paste the config file in there.  


## Competitive Programming Setup  
Use chrome for best compatibility with competitive programming scripts and everything. The first and important extension is the competitive companion which parses
the problems. To use that, I have written a download_problem.py which just listens to the competitive companion on port 10046. Note, that the file structure assumed is as follows -:
```
Desktop
  |- UNI
      |- Programming
            |- Scripts
```
All the aliases have been setup in the zshrc according to the above file structure, in case of changes kindly change both the aliases one for download_problem.py and the other for
make_prob.sh. Moreover, download_problem.py should be given permissions to run using the command :  
``` bash
sudo chmod +x download_problem.py
```
Also, note that you must install miniconda to create a virtual environment for competitive programming so that other projects running on the system don't break because of 
the competitive prorgamming scripts since they are highly dependent on the competitive companion extension. After installing conda run -:  
``` bash
# creating a new virtual environment by the name of programming in the Programming Folder
conda create --name programming
# starting the newly created virtual environment
conda activate programming
```
Now, you while in the virtual environment (activated) install the dependency docopt which has been used to parse the cli and stuff. To do that first you need to install pip
the python package manager in the conda virtual environment and then using pip u need to install docopt.  
``` bash
conda install pip
pip install docopt
pip install setuptools
```
I believe, now the download_problem.py should be fully working (Note: It only works in the programming virtual environment).  
You can test by creating a new folder in the Programming folder called Practice and then name by platform and then opening a terminal there and typing the alias that you created
in zshrc.   
``` bash
getprob
```
It should ask for make_prob.sh.  
Next, we setup the make_prob.sh. Download the script and paste it in the Scripts folder. Give it permissions to run using the code provided above. Then again setup the aliases correctly as pointed out earlier.   
Then we move on to setting up the templates and the makefile for building and running the system.  Create a folder by the name of .template using terminal in the programming folder. Then in the .terminal folder create a file named template.cpp the one which you want to use for competitive programming. The also paste the makefile in the same .template folder and your competitive programming setup is done.  
Next we move on to fast submit, we use a python library called online-judge-tools, install it using pip. Login to all the websites using it, type oj login website-url.  
U now have everything setup completely i believe. Just test if everything works fine or not.  


