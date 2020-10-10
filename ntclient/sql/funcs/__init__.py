from ...utils import profile_id
from .nt import sql_profile_guid_from_id

# TODO: prompt to create profile if copying default `prefs.json` with profile_id: -1 (non-existent)
profile_guid = sql_profile_guid_from_id(profile_id)
