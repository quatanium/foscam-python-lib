=================
foscam-python-lib
=================

.. image:: https://img.shields.io/pypi/v/pyfoscam.svg
    :target: https://pypi.python.org/pypi/pyfoscam

Foscam Python2 Library for H.264 IP Cameras (FI9821W/P/HD816W/P)

TODO
====

1. Support more camera models.

Getting Started
===============

Install
-------


.. code:: bash

  pip install pyfoscam

Simple example
--------------
Here is a simple example to move camera lens up and stop after 1s.

.. code:: python

    from foscam import FoscamCamera
    from time import sleep

    mycam = FoscamCamera('192.168.0.110', 88, 'admin', 'pwd')
    mycam.ptz_move_up()
    sleep(1)
    mycam.ptz_stop_run()

Asynchronous feature
--------------------
This example uses the asynchronous feature provided by ``FoscamCamera``.

Normally, a command is sent synchronously, waiting for results and blocking the main thread.

By initializing ``FoscamCamera`` with `daemon=True` (defaults to False), commands are sent asynchronously.

.. code:: python

    mycam = FoscamCamera('192.168.0.110', 88, 'admin', 'pwd', daemon=True)
    mycam.get_ip_info()
    mycam.get_port_info()
    mycam.refresh_wifi_list()


Send command with callback
--------------------------
This example illustrates the use of a callback function when the command completes.

.. code:: python

    from foscam import FoscamCamera, FOSCAM_SUCCESS
    def print_ipinfo(returncode, params):
        if returncode != FOSCAM_SUCCESS:
            print 'Failed to get IPInfo!'
            return
        print 'IP: %s, Mask: %s' % (params['ip'], params['mask'])

    mycam = FoscamCamera('192.168.0.110', 88, 'admin', 'pwd', daemon=False)
    mycam.get_ip_info(print_ipinfo)
