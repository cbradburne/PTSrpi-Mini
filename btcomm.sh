#!/bin/bash
sudo tee /etc/sudoers.d/$USER <<END
END

sudo rfcomm connect hci0 00:14:03:05:5A:A7

sudo /bin/rm /etc/sudoers.d/$USER
sudo -k