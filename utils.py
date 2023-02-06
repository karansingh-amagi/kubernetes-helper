import os
import sys
import subprocess
import shlex
# from nyx.logger import Log


class Utils:

    def __init__(self):
        # self.log = Log.get_logger(__name__)
        pass

    def run_cmd(self, cmd, *args, **kwargs):
        """
        run a command
        :param cmd: command
        :param args: arguments of a command
        :param kwargs:  any option flag with key value
        :return: ret_code, out, err
        """
        try:
            ignore_err = False
            cmd_as_args = shlex.split(cmd)
            if 'file_out' in kwargs:
                std_out = open(kwargs['file_out'], "w", 1)
            else:
                std_out = subprocess.PIPE

            if 'ignore_error' in kwargs:
                ignore_err = True

            print(cmd_as_args)
            p = subprocess.Popen(
                cmd_as_args, stdout=std_out, stderr=subprocess.PIPE)
            out, err = p.communicate()
            ret_code = p.returncode
            if not ignore_err and ret_code != 0:
                raise Exception()
        except FileNotFoundError as e:
            raise Exception(
                "command not found, please install and rerun, error: {}".format(e))
        except subprocess.CalledProcessError as error:
            # self.log.error('CalledProcessError:%s Output: %s ReturnCode:%s' % (error.err, error.out, error.ret_code))
            raise Exception('CalledProcessError:%s Output: %s ReturnCode:%s' % (
                error.err, error.out, error.ret_code))
        except:
            # self.log.error('Error:%s ReturnCode:%s' % (err, ret_code))
            raise Exception('Error:%s ReturnCode:%s' % (err, ret_code))
        return ret_code, out, err

    def create_directory(self, directory_to_create):
        if not os.path.exists(directory_to_create):
            os.makedirs(directory_to_create)
        # self.log.info('Created directory: %s' % (directory_to_create))
        return directory_to_create


ut = Utils()
ret, out, err = ut.run_cmd("ls -a > testing.txt")
print(ret, out.decode("utf-8"), err)

print(ut.create_directory("testing"))
