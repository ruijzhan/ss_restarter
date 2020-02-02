from docker import DockerClient
import socket
import time
import argparse

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

class SSRestarter():
    def __init__(self, ss_name, ss_host, interval):
        self.docker_cli = DockerClient(base_url='unix://var/run/docker.sock')
        self.ss_host = ss_host
        self.c = self.docker_cli.containers.get(ss_name)
        self.ip = self.get_ss_ip()
        self.i = interval
        logging.info('Watching address {}: current IP is {}'.format(ss_host, self.ip))

    def get_ss_ip(self):
        return socket.gethostbyname(self.ss_host)

    def check_ip_change(self):
        return self.get_ss_ip() != self.ip

    def restart_container(self):
        self.c.restart()

    def run(self):
        while True:
            if self.check_ip_change():
                self.restart_container()
                self.ip = self.get_ss_ip()
                logging.info('Detected IP changed to {}, restarted container'.format(self.ip))
            time.sleep(self.i)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--container", type=str, help="name of container to restart")
    parser.add_argument("-s", "--ss_host", type=str, help="ss host address")
    parser.add_argument("-i", "--interval", type=int, help="IP address checking interval in seconds")
    args = parser.parse_args()

    restarter = SSRestarter(ss_name=args.container, ss_host=args.ss_host, interval=args.interval)
    restarter.run()
