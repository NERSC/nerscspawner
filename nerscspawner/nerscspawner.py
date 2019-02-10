
from traitlets import List, Dict, Unicode

from wrapspawner import WrapSpawner

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
        self.child_class, self.child_config = self.spawners[profile]

    def construct_child(self):
        self.child_profile = self.user_options.get('profile', "")
        self.select_profile(self.child_profile)
        super().construct_child()

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
