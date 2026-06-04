# Workflow for Sample Code

## Connect
Connect your laptop to the local wifi: Dlink_SRL

Connect to the FSS of your choice.  You'll be logging in as Ethan.

Open a terminal and connect via ssh:

```ssh echebi@model1.local``` or ```ssh echebi@model3.local```

Model1 is the full FSS; model3 is the static pi and HDD setup.  
Find the IP address for your FSS via ```hostname -I```.  You'll need this later for file transfers.

Password: HooliganHall

## Software initialization and HDD spinup
In your terminal, now logged into the Pi, run the following commands:

```sudo pigpiod```

```python3 gui.py```

Open the gui in your web browser by copying in the address you see in the terminal.

## Running your controller

Replace "IP" below with the full IP address that you found above, and the "your_file" parameters with the filepath and filename you'd like to move to/from.

Add your code to the class_ex.py while loop, give it a new filename, then upload it to the Pi.  From a new terminal on your laptop (not logged in to Pi):

```scp ~/your_file_on_your_computer echebi@IP:/your_file_on_pi```

If you have saved data to a file on the Pi, you can get it back to your laptop via:

```scp echebi@IP:/your_file_on_pi ~/your_file_on_your_computer```

Open a new terminal and ssh into the Pi.  Run your file, replacing class_ex.py with the filepath and name you used above:

```python3 class_ex```

## Troubleshooting

If your code isn't working you can try spinning up the hard drive via a simpler program.  In a new terminall, ssh into the Pi and run:

```python3 hdd_spin``` 

To reboot the Pi:

```sudo reboot```
