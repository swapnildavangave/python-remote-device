import asyncio, asyncssh, sys
from configurations import host_conf


class SSHSession(asyncssh.SSHClientSession):
    def data_received(self, data, datatype):
        print(data, end='')

    def connection_lost(self, exc):
        if exc:
            print('SSH session error: ' + str(exc), file=sys.stderr)

class SecureHandshake(asyncssh.SSHClient):
    def connection_made(self, conn):
        print('Connection made to %s.' % conn.get_extra_info('peername')[0])

    def auth_completed(self):
        print('Authentication successful.')

async def run_client(command: str):
    conn, client = await asyncssh.create_connection(SecureHandshake, host=host_conf['host']
    ,port=host_conf['port'], username=host_conf['user'], password=host_conf['password'])

    async with conn:
        chan, session = await conn.create_session(SSHSession, command)
        await chan.wait_closed()
try:
    asyncio.get_event_loop().run_until_complete(run_client(command="ls -al"))
except (OSError, asyncssh.Error) as exc:
    sys.exit('SSH connection failed: ' + str(exc))