
import copy
import salt.config

DEFAULT_UEVENT_OPTS = {
    'conf_file': '/etc/salt/uevent',
    'color': True,
    'state_tabular': True,
    'state_output': 'changes',
    'state_verbose': False,
}

class SaltConfigMixin(object):
    _minion_opts = None
    _master_opts = None
    _my_opts     = None

    def _normalize_and_copy(self, attr):
        c = copy.deepcopy( getattr(self,attr) )
        if not isinstance(c,dict):
            return {}
        return c

    @property
    def minion_opts(self):
        if not SaltConfigMixin._minion_opts:
            SaltConfigMixin._minion_opts = salt.config.minion_config('/etc/salt/minion')
        return self._normalize_and_copy('_minion_opts')

    @property
    def master_opts(self):
        if not SaltConfigMixin._master_opts:
            SaltConfigMixin._master_opts = salt.config.master_config('/etc/salt/master')
        return self._normalize_and_copy('_master_opts')

    @property
    def my_opts(self):
        if not SaltConfigMixin._my_opts:
            SaltConfigMixin._my_opts = DEFAULT_UEVENT_OPTS.copy()
            SaltConfigMixin._my_opts.update(
                salt.config.load_config('/etc/salt/uevent', 'SALT_UEVENT_CONFIG', DEFAULT_UEVENT_OPTS['conf_file'])
            )
        return self._normalize_and_copy('_my_opts')

    @property
    def mmin_opts(self):
        o = self.minion_opts
        o.update( self.master_opts )
        o.update( self.my_opts )
        return o

    @property
    def salt_opts(self):
        o = self.mmin_opts
        o.pop('conf_file')
        return o

def get_config():
    class GenericConfigObject(SaltConfigMixin):
        pass
    return GenericConfigObject()
