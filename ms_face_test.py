import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json

subscription_key = 'YOUR SUBSCRIPTION KEY'

uri_base = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0'

# Request headers.
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

# Request parameters.
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}

# Body. The URL of a JPEG image to analyze.
body = {'url': 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'}

try:
    # Execute the REST API call and get the response.
    response = requests.request('POST', uri_base + '/detect', json=body, data=None, headers=headers, params=params)

    print ('Response:')
    parsed = json.loads(response.text)
    print (json.dumps(parsed, sort_keys=True, indent=2))

except Exception as e:
    print('Error:')
    print(e)