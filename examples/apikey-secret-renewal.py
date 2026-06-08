#
# Copyright (c) 2026 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from ns1 import NS1


def print_secret(secret):
    print(f"  Secret ID: {secret['secret_id']}")
    print(f"  Secret Value: {secret['secret']}")
    print(f"  Expires At: {secret['expires_at']}")
    print(f"  Enabled: {secret['enabled']}")


# NS1 will use config in ~/.nsone by default
api = NS1()

# to specify an apikey here instead, use:
# api = NS1(apiKey='<<CLEARTEXT API KEY>>')

# to load an alternate configuration file:
# api = NS1(configFile='/etc/ns1/api.json')

# Get the API key interface
apikey_api = api.apikey()

# Create a new API key with a name and expiry_duration
# You can also specify teams, ip_whitelist, ip_whitelist_strict, and permissions
# If permissions are not specified, default permissions (all false) will be used
# expiry_duration is set to 30 days
apikey_id = ""
try:
    ###########################
    # CREATE EXPIRING API KEY #
    ###########################
    print("Creating API key with 30 day expiry...")
    apikey = apikey_api.create(
        "example-api-key-with-expiry", expiry_duration="30d"
    )
    apikey_id = apikey["id"]
    print(f"Created API key: {apikey_id}")

    # Store the key ID for later operations

    # Store the actual apikey for later operations
    apikey_id = apikey["id"]
    apikey_secret = apikey["secrets"][0]
    apikey_secret_is = apikey_secret["secret_id"]
    apikey_secret_key = apikey_secret["secret"]

    print("Initial api key secret:")
    print_secret(apikey_secret)

    ########################
    # RENEW API KEY        #
    ########################

    # Use self renewal to renew this secret by creating a new api
    # instance that uses the new secret for authentication.
    api_with_secret_auth = NS1(apiKey=apikey_secret_key)
    apikeysecrets_with_secret_auth = api_with_secret_auth.apikeysecrets()
    # The default secret id for renew() is "self" and this will
    # renew the secret being used for authentication.
    new_secret = apikeysecrets_with_secret_auth.renew()
    print("Renewed api key secret:")
    print_secret(new_secret)
finally:
    # Clean up the API key so this script can be re-run
    if apikey_id != "":
        apikey_api.delete(apikey_id)
