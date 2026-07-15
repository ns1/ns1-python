#
# Copyright (c) 2026 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

import os
import sys
import json

from ns1 import NS1, Config

zone_name = sys.argv[1]
env_api_key = os.environ.get("NS1_API_KEY", None)

if env_api_key:
    api_key = env_api_key
    ns1_config = Config()
    ns1_config.createFromAPIKey(api_key)
    api = NS1(config=ns1_config)
else:
    # NS1 will use config in ~/.nsone by default
    api = NS1()

# turn on "follow pagination". This will handle paginated responses for
# zone list and the records for a zone retrieve. It's off by default to
# avoid a breaking change
config = api.config
config["follow_pagination"] = True

zone = api.zones().retrieve(zone_name, params={"export": True})
print(json.dumps(zone, indent=2, sort_keys=True))
