# The following functions are modified from Face API provided by Microsoft Azure

import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import http.client, urllib.request, urllib.parse, urllib.error, base64




def faceDetection(image):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'f38bcf11f84f4457a556800d0334016c',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': '',
    })

    try:
        conn = http.client.HTTPSConnection('eastus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, "{'url': '%s'}" % image, headers)
        response = conn.getresponse()
        data = response.read()
        return data
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def findSimilarFaces(faceId, faceListId, maxNum):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'f38bcf11f84f4457a556800d0334016c',
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('eastus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/findsimilars?%s" % params, 
            "{'faceId': '%s', 'faceListId': '%s', 'maxNumOfCandidatesReturned': %d, 'mode': 'matchFace'}" % (faceId, faceListId, maxNum),
             headers)
        response = conn.getresponse()
        data = response.read()
        return data
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))



def match(url):
    face = str(faceDetection(url))[3:-2]
    data = json.loads(face)
    faceId = data['faceId']
    faceListId = "facedatabase1"
    maxNum = 1
    resultData = str(findSimilarFaces(faceId, faceListId, maxNum))[3:-2]
    resultFace = json.loads(resultData)
    return resultFace

def getInfo(url):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'f38bcf11f84f4457a556800d0334016c',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender',
    })

    try:
        conn = http.client.HTTPSConnection('eastus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, "{'url': '%s'}" % url, headers)
        response = conn.getresponse()
        data = response.read()
        resultFace = json.loads(str(data)[3:-2])
        info = resultFace['faceAttributes']
        return info
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

