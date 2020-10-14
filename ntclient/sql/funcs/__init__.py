from ...persistence import profile_id
from .nt import sql_profile_guid_from_id

# TODO: prompt to create profile if copying default `prefs.json` with profile_id: -1 (non-existent)
if profile_id is None:
    profile_guid = None
else:
    profile_guid = sql_profile_guid_from_id(profile_id)
