
import copy
import salt.config

DEFAULT_UEVENT_OPTS = {
    'conf_file': '/etc/salt/uevent',
    'color': False,
}

class SaltConfigMixin(object):
    _minion_opts = None
    _master_opts = None
    _my_opts     = None

    def _normalize_and_copy(self, attr):
        c = copy.deepcopy( getattr(self,attr) )
        if not isinstance(c,dict):
            return {}
        if 'conf_file' in c:
            c.pop('conf_file')
        return c

    @property
    def minion_opts(self):
        if not self._minion_opts:
            self._minion_opts = salt.config.minion_config(None)
        return self._normalize_and_copy('_minion_opts')

    @property
    def master_opts(self):
        if not self._master_opts:
            self._master_opts = salt.config.master_config(None)
        return self._normalize_and_copy('_master_opts')

    @property
    def my_opts(self):
        if not self._my_opts:
            self._my_opts = salt.config.load_config(None, 'SALT_UEVENT_CONFIG', DEFAULT_UEVENT_OPTS)
        return self._normalize_and_copy('_my_opts')

    @property
    def salt_opts(self):
        o = self.minion_opts
        o.update( self.master_opts )
        o.update( self.my_opts )
        return o

def get_config():
    class GenericConfigObject(SaltConfigMixin):
        pass
    return GenericConfigObject().salt_opts
