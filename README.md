##### MasterProject

*How to fork:*
 1. fork project: https://github.com/cmpe295/MasterProject.git to your github account
  * click on the + button @ (MasterProject/+)
 2. clone https://github.com/YourAccount/MasterProject.git to your localhost
  * git clone https://github.com/YourAccount/MasterProject.git
 3. define upstream
  * git remote add upstream https://github.com/cmpe295/MasterProject.git

*Commit to your github account*
 1. git add .
 2. git commit -m "your commit message"
 3. git push

*Merge your changes to upstream*
 1. create pull request from your github account
 2. optionally tag ppl as reviewer
 3. merge your change to upstream/master

*fetch/merge changes made in upstream/master*
 1. git fetch upstream
 2. git merge upstream/master
 3. (it is good to do this before you start any developments to avoid future conflicts)
