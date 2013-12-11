foscam-python-lib
=================

Foscam Python Library for H.264 IP Cameras (FI9821W/HD816W)

TODO: Package setup.py and upload to pypi.


Getting Start
-------------
### Sample example
Here is a simple example to move a camera up and stop it after 1s.
    from foscam import FoscamCamera
    from time import sleep

    mycam = FoscamCamera('192.168.0.110', 88, 'admin', 'foscam')
    mycam.ptz_move_up()
    sleep(1)
    mycam.ptz_stop_run()

### Asynchronous feature.
This example does not use the asynchronous features provided by ``FoscamCamera``.
So a command will be sent synchronously, waiting for the results. Then the next
command will be sent. 
By initilizing ``FoscamCamera`` with `daemon` = True(defaults to False), 
we can send commands asynchronously. 

    mycam = FoscamCamera('192.168.0.110', 88, 'admin', 'foscam', daemon=False)
    mycam.get_ip_info()
    mycam.get_port_info()
    mycam.refresh_wifi_list()

### Send command with callback
    from foscam import FoscamCamera, FOSCAM_SUCCESS
    def print_ipinfo(returncode, params):
        if returncode != FOSCAM_SUCCESS:
            print 'Failed to get IPInfo!'
            return
        print 'IP: %s, Mask: %s' % (params['ip'], params['mask'])
        
    
    mycam = FoscamCamera('192.168.0.110', 88, 'admin', 'foscam', daemon=False)
    mycam.get_ip_info(print_ipinfo)

