
from jupyterhub.spawner import LocalProcessSpawner

from traitlets import List, Dict, Unicode

from wrapspawner import WrapSpawner

class NullSpawner(LocalProcessSpawner):

    def user_env(self, env):
        return env

class NERSCSpawner(WrapSpawner):

    profiles = List(Dict(),
            help="TBD",
            config=True)

    setups = List(Dict(),
            help="TBD",
            config=True)

    systems = List(Dict(),
            help="TBD",
            config=True)

    spawners = Dict(
            help="TBD",
            config=True)

    child_profile = Unicode()

    def select_profile(self, profile):
        self.log.debug("select_profile: " + profile)
        try:
            self.child_class, self.child_config = self.spawners[profile]
        except KeyError:
            self.child_class, self.child_config = NullSpawner, {}

    def construct_child(self):
        # self.child_profile = self.user_options.get('profile', "")
        self.child_profile = self.name
        self.select_profile(self.child_profile)
        super().construct_child()
        self.child_spawner.orm_spawner = self.orm_spawner  ### IS THIS KOSHER?!?!!?
        self.options_form = self.child_spawner.options_form # another one...
        self.options_from_form = self.child_spawner.options_from_form # yet another
        ### Think we need to do this to get JUPYTERHUB_OAUTH_CALLBACK_URL set properly

    def load_child_class(self, state):
        try:
            self.child_profile = state['profile']
        except KeyError:
            self.child_profile = ''
        self.select_profile(self.child_profile)

    def get_state(self):
        state = super().get_state()
        state['profile'] = self.child_profile
        return state

    def clear_state(self):
        super().clear_state()
        self.child_profile = ''

    @property
    def model_updated(self):
        return True
