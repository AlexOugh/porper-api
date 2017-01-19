
import sys
sys.path.insert(0, r"..")
from handler import handler

import json
body = {
  "code":"09cc6ca0c46e81d42e24",
  "state":"08e23b0a-80fc-4811-94af-133fc3438324",
  "provider":"github",
  "redirect_uri":"https://0s31kbhnk2.execute-api.us-east-1.amazonaws.com/dev/callback"
};
body_str = json.dumps(body)

event = {
    "resource": "/{proxy+}",
    "path": "/auth",
    "httpMethod": "POST",
    "headers": {
        "external-id":
        " 1234"
    },
    "queryStringParameters": {
        "a": "1",
        "b": "2"
    },
    "pathParameters": { "proxy": "auth" },
    "stageVariables": None,
    "requestContext": {
        "accountId": "089476987273",
        "resourceId": "85hu0a",
        "stage": "test-invoke-stage",
        "requestId": "test-invoke-request",
        "identity": {
            "cognitoIdentityPoolId": None,
            "accountId": None,
            "cognitoIdentityId": None,
            "caller": None,
            "apiKey": None,
            "sourceIp": "108.248.87.133",
            "cognitoAuthenticationType": None,
            "cognitoAuthenticationProvider": None,
            "userArn": None,
            "userAgent": "Apache-HttpClient/4.5.x (Java/1.8.0_102)",
            "user": None
        },
        "resourcePath": "/{proxy+}",
        "httpMethod": "POST",
        "apiId": "obkuecl0oh"
    },
    "body": body_str
}
handler(event, None)
