
from batchspawner import BatchSpawnerRegexStates

from traitlets import Unicode, default

class NERSCSlurmSpawner(BatchSpawnerRegexStates):
    """Spawner that connects to a job-submit (login node) and submits a job to
    start a process running in the Slurm batch queue.

    NOTE Right now we allow the hub to pre-select a random port but when multiple
    users are on the same compute node, a la shared-interactive, we need to control
    the port selected deterministically or ensure they don't collide in some way."""

    # all these req_foo traits will be available as substvars for templated strings

    req_qos = Unicode('regular',
            help="QoS name to submit job to resource manager"
            ).tag(config=True)

    req_remote_host = Unicode('remote_host',
                          help="""The SSH remote host to spawn sessions on."""
                          ).tag(config=True)

    req_constraint = Unicode('haswell',
            help="""Users specify which features are required by their job
            using the constraint option, which is required at NERSC on Cori/Gerty."""
            ).tag(config=True)

    req_env_text = Unicode()

    @default("req_env_text")
    def _req_env_text(self):
        env = self.get_env()
        text = ""
        for item in env.items():
            text += 'export %s=%s\n' % item
        return text

    batch_script = Unicode("""#!/bin/bash
#SBATCH --constraint={constraint}
#SBATCH --job-name=jupyter
#SBATCH --output=jupyter-%j.log
#SBATCH --qos={qos}
#SBATCH --time={runtime}

sdnpath=/global/common/shared/das/sdn

/usr/bin/python $sdnpath/cli.py associate

export PATH=/global/common/cori/software/python/3.6-anaconda-4.4/bin:$PATH
which jupyterhub-singleuser
{env_text}
unset XDG_RUNTIME_DIR
{cmd}
""").tag(config=True)

    prefix = "ssh -q -o StrictHostKeyChecking=no -o preferredauthentications=publickey -l {username} -i /tmp/{username}.key {remote_host} "

    # outputs line like "Submitted batch job 209"
    batch_submit_cmd = Unicode(prefix + '/usr/bin/sbatch').tag(config=True)
    # outputs status and exec node like "RUNNING hostname"
#   batch_query_cmd = Unicode(prefix + 'squeue -h -j {job_id} -o \\"%T %B\\"').tag(config=True) # Added backslashes here for quoting
    batch_query_cmd = Unicode(prefix + '/usr/bin/python /global/common/shared/das/sdn/getip.py {job_id}').tag(config=True) # Added backslashes here for quoting
    batch_cancel_cmd = Unicode(prefix + '/usr/bin/scancel {job_id}').tag(config=True)
    # use long-form states: PENDING,  CONFIGURING = pending
    #  RUNNING,  COMPLETING = running
    state_pending_re = Unicode(r'^(?:PENDING|CONFIGURING)').tag(config=True)
    state_running_re = Unicode(r'^(?:RUNNING|COMPLETING)').tag(config=True)
    state_exechost_re = Unicode(r'\s+((?:[\w_-]+\.?)+)$').tag(config=True)

    def parse_job_id(self, output):
        # make sure jobid is really a number
        try:
            id = output.split(' ')[-1]
            int(id)
        except Exception as e:
            self.log.error("SlurmSpawner unable to parse job ID from text: " + output)
            raise e
        return id

    # This is based on SSH Spawner
    def get_env(self):
        """Add user environment variables"""
        env = super().get_env()

        env.update(dict(
            JPY_USER=self.user.name,
            JPY_COOKIE_NAME=self.user.server.cookie_name,
            JPY_BASE_URL=self.user.server.base_url,
            JPY_HUB_PREFIX=self.hub.server.base_url,
            JUPYTERHUB_PREFIX=self.hub.server.base_url,
            # PATH=self.path
            # NERSC local mod
            PATH=self.path
        ))

        if self.notebook_dir:
            env['NOTEBOOK_DIR'] = self.notebook_dir

        hub_api_url = self.hub.api_url
        if self.hub_api_url != '':
            hub_api_url = self.hub_api_url

        env['JPY_HUB_API_URL'] = hub_api_url
        env['JUPYTERHUB_API_URL'] = hub_api_url

        return env
