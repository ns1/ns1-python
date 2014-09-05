#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from nsone import NSONE, Config

# you can either build your own config, or let NSONE build a default one for
# you. the latter is easier and works like this:

# NSONE will use config in ~/.nsone by default
nsone = NSONE()

# to specify an apikey here instead, use:
nsone = NSONE(apiKey='qACMD09OJXBxT7XOuRs8')

# to load an alternate configuration file:
nsone = NSONE(configFile='/etc/nsone/api.json')

# to load a specific keyID inside of your config file (see config format
# in docs), use this. this only makes sense for config file loads, not
# apiKey loads:
nsone = NSONE(keyID='all-access')

# if you have special needs, build your own Config object and pass it to
# NSONE:
config = Config()
config.createFromAPIKey('qACMD09OJXBxT7XOwv9v')
config['verbosity'] = 5
config['transport'] = 'twisted'
nsone = NSONE(config=config)

#  you can get the current config object NSONE is using via
config = nsone.config

# change config variables
config['verbosity'] = 5

# write out new config files
config.write('/tmp/newconfig.json')

# the config file format supports different apiKeys (see docs) using keyID

# get the current keyID
print(config.getCurrentKeyID())

# use a different keyID
config.useKeyID('read-access')
