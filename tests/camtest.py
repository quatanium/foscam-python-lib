import os.path
import unittest
from time import sleep

try:  # PY3
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

from foscam.foscam import FoscamCamera, FOSCAM_SUCCESS

config = ConfigParser()
config_filepath = os.path.join(os.path.dirname(__file__), 'camtest.cfg')

if os.path.exists(config_filepath):
    config.read([config_filepath])

config_defaults = config.defaults()

CAM_HOST = config_defaults.get('host') or ''
CAM_PORT = config_defaults.get('port') or 88
CAM_USER = config_defaults.get('user') or 'admin'
CAM_PASS = config_defaults.get('pass') or 'foscam'
CAM_WIFI_SSID = config_defaults.get('wifi_ssid') or ''
CAM_WIFI_PASS = config_defaults.get('wifi_pass') or ''


class CallbackForTest(object):
    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class TestFoscam(unittest.TestCase):
    def setUp(self):
        self.foscam = FoscamCamera(CAM_HOST, CAM_PORT, CAM_USER, CAM_PASS)

    # ***************** Test Account Functions ***************************
    def test_change_user_name(self):
        self.foscam.change_user_name('admin', 'cherish')
        self.foscam.usr = 'cherish'
        self.foscam.get_ip_info()
        self.foscam.change_user_name('cherish', 'admin')

    def test_change_password(self):
        self.foscam.change_password('admin', 'foscam', 'qhomecam')
        self.foscam.pwd = 'qhomecam'
        self.foscam.get_ip_info()
        self.foscam.change_password('admin', 'qhomecam', 'foscam')

    # ***************** Test AV Functions *********************
    def test_sub_video_stream(self):
        self.foscam.get_sub_video_stream_type()
        self.foscam.set_sub_stream_format(1)
        self.foscam.get_sub_video_stream_type()

    def test_video_stream_param(self):
        self.foscam.get_main_video_stream_type()
        self.foscam.get_video_stream_param()
        self.foscam.set_video_stream_param(0, 0, 2 * 1024 * 1024, 30, 30, 1)
        self.foscam.get_video_stream_param()

    def test_mirror_video(self):
        # Turn on mirror
        rc, args = self.foscam.mirror_video(1)
        self.assertEqual(rc, 0)
        # Turn off mirror
        rc, args = self.foscam.mirror_video(0)
        self.assertEqual(rc, 0)

    def test_flip_video(self):
        # Filp
        rc, args = self.foscam.flip_video(1)
        self.assertEqual(rc, 0)
        # Not Filp
        rc, args = self.foscam.flip_video(0)
        self.assertEqual(rc, 0)

    def test_get_mirror_and_flip_setting(self):
        rc, args = self.foscam.get_mirror_and_flip_setting()
        self.assertEqual(rc, 0)

    # ***************** Test Network Functions *********************
    def test_get_ip_info(self):
        rc, info = self.foscam.get_ip_info()
        self.assertTrue(rc == 0)

    # ***************** Test Network Functions *********************
    def test_set_ip_info(self):
        old = self.foscam.get_ip_info()
        self.foscam.set_ip_info(is_dhcp=0, ip='192.168.0.110',
                                gate='192.168.0.1', mask='255.255.255.0',
                                dns1='192.168.0.1', dns2='8.8.8.8')
        # Wait to reboot.
        sleep(30)
        self.foscam.get_ip_info()

    def test_set_port(self):
        rc, args = self.foscam.get_port_info()
        rc, args = self.foscam.set_port_info(webport=88, mediaport=88,
                                             httpsport=443, onvifport=888)
        self.assertEqual(rc, 0)
        rc, args = self.foscam.get_port_info()

    def test_set_upnp(self):
        self.foscam.get_upnp_config()
        self.foscam.set_upnp_config(0)
        self.foscam.set_upnp_config(1)

    def test_wifi(self):
        self.foscam.refresh_wifi_list()
        self.foscam.get_wifi_list(0)
        self.foscam.get_wifi_config()

        self.foscam.set_wifi_setting(
            ssid=CAM_WIFI_SSID,
            psk=CAM_WIFI_PASS,
            isenable=0,
            isusewifi=0,
            nettype=0,
            encryptype=4,
            authmode=1,
            keyformat=0,
            defaultkey=1)

    # *************** PTZ Move ********************************

    def test_move_up(self):
        # Test Move up
        self.foscam.ptz_move_up()
        self.foscam.ptz_stop_run()

    def test_move_down(self):
        # Test Move down
        self.foscam.ptz_move_down()
        self.foscam.ptz_stop_run()

    def test_move_left(self):
        # Test Move left
        self.foscam.ptz_move_left()
        self.foscam.ptz_stop_run()

    def test_move_right(self):
        self.foscam.ptz_move_right()
        self.foscam.ptz_stop_run()

    def test_move_top_left(self):
        self.foscam.ptz_move_top_left()
        self.foscam.ptz_stop_run()

    def test_move_top_right(self):
        self.foscam.ptz_move_top_right()
        self.foscam.ptz_stop_run()

    def test_move_bottom_left(self):
        self.foscam.ptz_move_bottom_left()
        self.foscam.ptz_stop_run()

    def test_move_bottom_right(self):
        self.foscam.ptz_move_bottom_right()
        self.foscam.ptz_stop_run()

    def test_reset(self):
        self.foscam.ptz_reset()

    def test_ptz_speed(self):
        self.foscam.get_ptz_speed()
        self.foscam.set_ptz_speed(4)
        self.foscam.ptz_move_up()
        self.foscam.ptz_stop_run()

    def test_ptz_selftest(self):
        self.foscam.set_ptz_selftestmode(mode=1)
        flag, kwargs = self.foscam.get_ptz_selftestmode()
        self.assertTrue('mode' in kwargs and int(kwargs['mode']) is 1)

        self.foscam.set_ptz_selftestmode(mode=0)
        flag, kwargs = self.foscam.get_ptz_selftestmode()
        self.assertTrue('mode' in kwargs and int(kwargs['mode']) is 0)

    # ***************** Test device manage ******************

    def test_get_set_system_time(self):
        rc, args = self.foscam.get_system_time()
        self.assertTrue(rc == 0)
        self.foscam.set_system_time(time_source=args['timeSource'],
                                    ntp_server=args['ntpServer'],
                                    date_format=args['dateFormat'],
                                    time_format=args['timeFormat'],
                                    time_zone=args['timeZone'],
                                    is_dst=args['isDst'],
                                    dst=args['dst'],
                                    year=args['year'],
                                    mon=args['mon'],
                                    day=args['day'],
                                    hour=args['hour'],
                                    minute=args['minute'],
                                    sec=args['sec'],
                                    )

    def test_devname(self):
        args = self.foscam.get_dev_name()
        self.foscam.set_dev_name('cherish`s cam')
        self.foscam.get_dev_name()
        self.foscam.set_dev_name(args['devName'])

    def test_dev_state(self):
        rc, args = self.foscam.get_dev_state()
        self.assertEqual(rc, 0)

    def test_dev_info(self):
        rc, args = self.foscam.get_dev_info()
        self.assertEqual(rc, 0)

    def test_open_infra_led(self):
        rc, args = self.foscam.open_infra_led()
        self.assertEqual(rc, 0)

    def test_close_infra_led(self):
        rc, args = self.foscam.close_infra_led()
        self.assertEqual(rc, 0)

    def test_get_infra_led_config(self):
        rc, args = self.foscam.get_infra_led_config()
        self.assertEqual(rc, 0)

    def test_set_infra_led_config(self):
        rc, args = self.foscam.set_infra_led_config(1)
        self.assertEqual(rc, 0)

    def test_open_white_light(self):
        rc, args = self.foscam.open_white_light()
        self.assertEqual(rc, 0)

    def test_close_white_light(self):
        rc, args = self.foscam.close_white_light()
        self.assertEqual(rc, 0)

    def test_get_white_light_config(self):
        rc, args = self.foscam.get_white_light_config()
        self.assertEqual(rc, 0)

    def test_set_white_light_config(self):
        rc, args = self.foscam.set_white_light_config(2)
        self.assertEqual(rc, 0)

    def test_get_product_all_info(self):
        rc, args = self.foscam.get_product_all_info()
        self.assertEqual(rc, 0)
        self.assertIn('modelName', args)

    # ************ Test AV Function *************************

    def test_get_alarm_record_config(self):
        print(self.foscam.get_alarm_record_config())

    def test_set_alarm_record_config(self):
        rc, old_args = self.foscam.get_alarm_record_config()
        new_args = {'isEnablePreRecord': 1,
                    'alarmRecordSecs': 240,
                    'preRecordSecs': 5
                    }
        self.foscam.set_alarm_record_config(
            alarm_record_secs=new_args['alarmRecordSecs'],
            prerecord_secs=new_args['preRecordSecs'])

        rc, args = self.foscam.get_alarm_record_config()
        self.assertTrue(rc == 0)
        self.assertTrue(int(args['alarmRecordSecs']) ==
                        new_args['alarmRecordSecs'])
        self.assertTrue(int(args['preRecordSecs']) ==
                        new_args['preRecordSecs'])

        self.foscam.set_alarm_record_config(
            alarm_record_secs=old_args['alarmRecordSecs'],
            prerecord_secs=old_args['preRecordSecs'])

    def test_get_local_alarm_record_config(self):
        rc, args = self.foscam.get_local_alarm_record_config()
        self.assertTrue(set(args) == {'isEnableLocalAlarmRecord',
                                      'localAlarmRecordSecs'})

    def test_set_local_alarm_recor_config(self):
        rc, args = self.foscam.set_local_alarm_record_config(
            is_enable_local_alarm_record=1,
            local_alarm_record_secs=60)
        self.assertTrue(rc == 0)
        rc, args = self.foscam.get_local_alarm_record_config()
        self.assertTrue(all([rc == 0,
                             args['isEnableLocalAlarmRecord'] == '1',
                             args['localAlarmRecordSecs'] == '60']))

    def test_get_h264_frm_ref_mode(self):
        rc, args = self.foscam.get_h264_frm_ref_mode()
        self.assertEqual(rc, 0)
        self.assertEqual(args.keys(), ['mode'])

    def test_set_h264_frm_ref_mode(self):
        mode = 3
        rc, args = self.foscam.set_h264_frm_ref_mode(mode=mode)
        self.assertEqual(rc, 0)
        rc, args = self.foscam.get_h264_frm_ref_mode()
        self.assertEqual(rc, 0)
        self.assertEqual(args['mode'], str(mode))

    def test_get_schedule_record_config(self):
        all_args = {'isEnable', 'isEnableAudio', 'recordLevel',
                    'schedule0', 'schedule1', 'schedule2',
                    'schedule3', 'schedule4', 'schedule5',
                    'schedule6', 'spaceFullMode'}
        rc, args = self.foscam.get_schedule_record_config()
        self.assertTrue(rc == 0)
        self.assertTrue(set(args) == all_args)

    def test_set_schedule_record_config(self):
        rc, args = self.foscam.set_schedule_record_config(
            is_enable=1, record_level=4,
            space_full_mode=0, is_enable_audio=0)
        self.assertTrue(rc == 0)

    def test_get_record_path(self):
        rc, args = self.foscam.get_record_path()
        self.assertTrue(rc == 0)
        self.assertTrue(set(args) == {'path', 'free', 'total'})

    def test_set_record_path(self):
        rc, args = self.foscam.get_record_path()
        self.assertTrue(rc == 0)
        rc, args = self.foscam.set_record_path(path=0)
        self.assertTrue(rc == 0)

    def test_get_ptz_preset_point_list(self):
        rc, args = self.foscam.get_ptz_preset_point_list()
        self.assertTrue('point0' in args)

    # ******************* Other *****************************
    def test_unblocked_execute(self):
        self.foscam.daemon = True
        self.foscam.ptz_move_up()
        sleep(0.5)
        self.foscam.ptz_stop_run()

    def test_callback(self):
        def print_res(*args, **kwargs):
            with open('temp.txt', 'w') as f:
                f.write(str(args))
                f.write(str(kwargs))

        self.foscam.daemon = True
        self.foscam.get_ip_info(print_res)
        timeout = 10
        flag = False
        while timeout >= 0:
            try:
                with open('temp.txt', 'r') as new_f:
                    self.assertTrue(new_f.read() != '')
                    flag = True
                    break
            except Exception as e:
                print(e)
                pass
            sleep(0.5)
            timeout -= 0.5
        self.assertTrue(flag)

    # *************** SnapPicture Function *******************

    def test_snap_picture_2(self):
        # also test callback with raw data
        callback = CallbackForTest()
        rc, data = self.foscam.snap_picture_2(callback=callback)
        self.assertEqual(rc, FOSCAM_SUCCESS)
        with open('test.jpg', 'wb') as fp:
            fp.write(data)
        self.assertSequenceEqual(callback.args, (rc, data))

    # ********************** Misc ****************************

    def test_get_log(self):
        # also test callback with non-raw data
        callback = CallbackForTest()
        rc, args = self.foscam.get_log(0, callback=callback)
        self.assertEqual(rc, FOSCAM_SUCCESS)
        self.assertTrue('log0' in args)
        self.assertSequenceEqual(callback.args, (rc, args))


if __name__ == '__main__':
    unittest.main()
