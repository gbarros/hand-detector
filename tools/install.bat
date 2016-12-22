% Install chocolatey %
echo Install Chocolatey
@powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

echo Install Python

choco install python2-x86_32 -y

echo Install OpenCV

choco install opencv -y 

echo install eager tools

pip install eager.whl
