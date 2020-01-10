#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from ns1 import NS1
import uuid

# NS1 will use config in ~/.nsone by default
#api = NS1()

# to specify an apikey here instead, use:
# api = NS1(apiKey='qACMD09OJXBxT7XOuRs8')

# to load an alternate configuration file:
# api = NS1(configFile='/etc/ns1/api.json')

########################
# CREATE / UPDATE TEAM #
########################
teamAPI = api.team()

# create a new team
# you can also specify an ip_whitelist and permissions
# if left blank, all permissions will be defaulted to false
team = teamAPI.create('test-team')
print (team)
teamID = team['id']

# modify some of the default permissions
perms = team['permissions']
perms['data']['push_to_datafeeds'] = True
perms['account']['view_invoices'] = True

# update the team with new permissions
team = teamAPI.update(teamID, permissions=perms)
print (team)

######################
# USERS AND API KEYS #
######################

userAPI = api.user()

# create a uuid to use as the username
uid = str(uuid.uuid1()).replace('-', '_')[:32]

# create a new user
# you can also specify ip_whitelist, ip_whitelist_strict, notify, and permissions
# if left blank, all permissions will be defaulted to false
user = userAPI.create('example', uid, 'email@ns1.io')
print (user)

# update the user and assign it to the team previously created
userAPI.update(uid, teams=[teamID])
user = userAPI.retrieve(uid)

# the user will inherit the permissions of the team
print (user)

apikeyAPI = api.apikey()

# create a new apikey
# you can also specify ip_whitelist, ip_whitelist_strict, and permissions
# if left blank, all permissions will be defaulted to false
apikey = apikeyAPI.create('example-key')
print (apikey)

# update the apikey and assign it to the team previously created
apikey = apikeyAPI.update(apikey['id'], teams=[teamID])

# the key will inherit the permissions of the team
print (apikey)

############
# CLEAN UP #
############

# delete the created resources
userAPI.delete(uid)
apikeyAPI.delete(apikey['id'])
teamAPI.delete(teamID)
