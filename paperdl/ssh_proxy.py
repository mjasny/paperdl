import paramiko
import os


SOCKS_HOST = '127.0.0.1'
SOCKS_PORT = 34579


class SSHProxy:
    def __init__(self, ssh_host):
        ssh_config = paramiko.SSHConfig()
        user_config_file = os.path.expanduser('~/.ssh/config')
        if os.path.exists(user_config_file):
            with open(user_config_file) as f:
                ssh_config.parse(f)

        user_config = ssh_config.lookup(ssh_host)
        cfg = {
            'hostname': user_config.get('hostname', ssh_host),
            'port': user_config.get('port'),
            'username': user_config.get('user'),
            'key_filename': user_config.get('identityfile')
        }
        cfg = {k: v for k, v in cfg.items() if v is not None}

        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.load_system_host_keys()
        self.ssh_client.connect(**cfg)

        self.proxy = self.ssh_client.open_socks_proxy(
            bind_address=SOCKS_HOST,
            port=SOCKS_PORT,
        )

    def __del__(self):
        self.proxy.close()
        self.ssh_client.close()

    def get_proxies(self):
        return  {
            'http': f'socks5://{SOCKS_HOST}:{SOCKS_PORT}',
            'https': f'socks5://{SOCKS_HOST}:{SOCKS_PORT}',
        }