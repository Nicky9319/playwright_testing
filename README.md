#Setting up playwright with chrome profile
Steps


## 1. install chrome inside the Linux

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

sudo apt install ./google-chrome-stable_current_amd64.deb

## 2. Folder to store the fresh chrome profile data => /home/user/chrome-debug-profile/
   google-chrome --remote-debugging-port=9222 --user-data-dir=/home/user/chrome-debug-profile
   Run and test the py file
   
### Note: We might need to run the browser beforehand in headful mode and do google login

### Note: We are using Ubuntu-20.04 for the same
