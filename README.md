# receiptPhotobooth
This takes a picture and then prints it onto a receipt with a caption.
Requires python3 with tinter as well s PIL, url lib, os, time, picamera, and date time.

Theoretical (unconfirmed) steps:

Open pi, connect all the connections and plug.

Sudo apt-get update, sudo apt-get upgrade

Make sure PIL, url lib, os, time, picamera, and datetime are installed. Most should be by default, if not try pip3 install PIL , etc. Maybe apt-get install if pip3 doesn't work.

cd ~/Desktop

git clone <url>
  
cp receiptPhotobooth/photobooth.py photobooth.py
  
python3 photobooth.py


  
  If you get an error that "_tkinter.TclError: no display name and no $DISPLAY environment variable" entering this in terminal may solve your problems:
  
  export DISPLAY=:0
