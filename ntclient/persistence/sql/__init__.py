from ...persistence import profile_id
from .nt.funcs import nt_ver, sql_profile_guid_from_id
from .usda.funcs import usda_ver

# TODO: prompt to create profile if copying default `prefs.json` with profile_id: -1 (non-existent)
if profile_id is None:
    profile_guid = None
else:
    profile_guid = sql_profile_guid_from_id(profile_id)


# TODO: Verify version
__db_version_nt__ = nt_ver()
__db_version_usda__ = usda_ver()
