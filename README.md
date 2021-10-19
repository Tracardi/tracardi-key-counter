# Key counter

This plugin counts keys provided in payload. Key string provided in payload will be treated as an information 
to increase the value of a key in profile. 

# Configuration

```json
{
  "path": "profile@stats.counters.MobileVisits"
}
```

This configuration point to data in profile that will hold the information on key counts. 
It should be empty object `{}` or the object in the key-value format

*Example*

```json
{
  "key1": 1,
  "key2": 33
}
```

This action will place additional counts in the provided path.

# Payload

Payload for this plugin must be either string or list of stings. Each string is a key to be counted.

For example if you would like to count mobile and desktop visits. Get the agent type from context (see: `event.context`) 
and cut out information about platform. Then send it to this plugin to be counted. If the value equals to 'mobile',
then the key value in profile will be increased by 1, if the payload value is 'desktop' then desktop key value will increase.
Example of payload:

```json
{
  "payload": "mobile"
}
```

There may be multiple keys in the payload. 

```json
{
  "payload": ["mobile", "android"]
}
```
