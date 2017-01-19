
import sys
sys.path.insert(0, r"..")
from handler import handler

import json
body = {
};
body_str = json.dumps(body)

event = {
    "resource": "/{proxy+}",
    "path": "/user",
    "httpMethod": "GET",
    "headers": {
        "access_token": "88436668f9a2b5c4dc75c76c60e005e04f8484bd"
    },
    "queryStringParameters": {
        'role_id': 'f3e798ee-6fee-4b79-b615-12cc2004f622'
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
        "httpMethod": "GET",
        "apiId": "obkuecl0oh"
    },
    "body": body_str
}
handler(event, None)
