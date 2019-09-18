import module_manager
module_manager.review()
import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import numpy as np

imageList = [
"https://cdn.pixabay.com/photo/2013/11/14/13/11/front-view-210383_960_720.jpg",
"https://image1.masterfile.com/getImage/NjQxLTA3MDc5MzA4ZW4uMDAwMDAwMDA=ANdY8k/641-07079308en_Masterfile.jpg",
"https://c8.alamy.com/comp/C698A7/portrait-young-chinese-man-front-face-in-suit-C698A7.jpg",
"https://i.dailymail.co.uk/i/pix/2012/06/28/article-2166021-13C59DF4000005DC-630_468x571.jpg",
"https://i.pinimg.com/originals/03/be/44/03be44fef8ab5105a9cc1699da165f20.jpg",
"https://st4.depositphotos.com/2760050/20320/i/1600/depositphotos_203204024-stock-photo-man-with-beard-and-mustache.jpg",
"https://image1.masterfile.com/getImage/NjAwLTAyNjk0MjE5ZW4uMDAwMDAwMDA=AHg5w9/600-02694219en_Masterfile.jpg",
"https://hips.hearstapps.com/elleuk.cdnds.net/15/37/2048x2730/2048x2730-b4-ddd491614b97-assets-elleuk-com-gallery-12487-robert-downey-jr-arrives-at-the-lacma-2013-getty-jpg.jpg",
"https://i.pinimg.com/originals/b1/c8/af/b1c8af415b4b25f94d66be4f685024de.jpg",
"https://image.shutterstock.com/image-photo/young-man-making-stop-his-260nw-104946482.jpg",
"http://www.innovationchain.org/site/images/2014_event/speakers/wei_liu.jpg",
"http://www.etc.cmu.edu/wp-content/uploads/2013/08/Zhu_Chaojie_Zacks-1.jpg",
"https://static1.squarespace.com/static/54c2a5c7e4b043776a0b0036/5c01afca2b6a287874558781/5c01b0124fa51ac227152675/1543615941656/Philip+Kuehne.jpg?format=1000w",
"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQTpf0gp9amHfYWyP1UXy04r29WRIBVljeEg9St_ZJyiE1WCmOS",
"https://pittnews.com/wp-content/uploads/2017/11/N_PDMA_TY-475x317.jpg",
"https://cs.stanford.edu/people/rexy/uploads/2/3/9/0/23903170/2017-by-hector-3-medium_1_orig.jpg",
"https://cdn.filestackcontent.com/WfYZLgGRW681CYZjJ5Bn",
"https://www.hindustantimes.com/rf/image_size_640x362/HT/p2/2016/08/26/Pictures/_c94e157e-6b74-11e6-8382-bd2fa398f652.jpg",
"https://www.goodfreephotos.com/cache/people/pretty-young-women-smiling.jpg", 
"https://www.99status.com/wp-content/uploads/young-women.jpg", 
"https://s14870.pcdn.co/wp-content/uploads/2017/02/vyVCeshtGIa6Lh9i6Dqe62ah6L5afsYyuKct0a0D3GE.jpg", 
"https://img.playbuzz.com/image/upload/ar_1.5,c_pad,f_jpg,b_auto/q_auto:good,f_auto,fl_lossy,w_640,c_limit/cdn/66e5496b-192f-413d-8236-144afb65fd15/5ebae3f1-ed51-478b-8992-d487be1e70fd_560_420.jpg", 
"https://cdn.playbuzz.com/cdn/11572c25-3aa8-41c5-8fef-795de51e4346/ee72093c-3c01-433a-8d25-701cca06c975.jpg",  
"http://www.thexerxes.com/wp-content/uploads/2016/04/Glam-Celebrity-Hairstyles-for-Women.jpg", 
"https://i.pinimg.com/originals/17/14/b9/1714b96920468389e6b4618bde8cef94.jpg", 
"https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/celebrity-bob-hairstyles-1536054527.jpg", 
"https://img-s-msn-com.akamaized.net/tenant/amp/entityid/BBMEHpf.img?h=1080&w=1920&m=6&q=60&o=f&l=f&x=514&y=335", 
"https://s2.r29static.com//bin/entry/779/0,0,2000,2400/720x864,80/2040589/image.jpg", 
"http://www.bob-hairstyle.com/wp-content/uploads/2017/06/15.Bob-Haircuts-Celebrity.jpg", 
"https://www.juanparksforcongress.com/wp-content/uploads/2018/12/lob-bob-hairstyles-great-the-most-pretty-lob-and-bob-haircuts-for-2017-de-lob-bob-hairstyles.jpg"]


# The following function is modified from Face API provided by Microsoft Azure
def list(imageURL):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'f38bcf11f84f4457a556800d0334016c',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'userData': '',
        'targetFace': '',
    })

    try:
        conn = http.client.HTTPSConnection('eastus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/facelists/facedatabase1/persistedFaces?%s" % params, "{'url' : '%s'}" % imageURL, headers)
        response = conn.getresponse()
        data = response.read()
        resultData = str(data)[2:-1]
        result = json.loads(resultData)
        return(result['persistedFaceId'])
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))



def imageProcess(imageList, faceListId):
    dataDict = dict()

    for image in imageList: #image is a url
        faceId = list(image)
        dataDict[faceId] = image

    np.save('database.npy', dataDict)

imageProcess(imageList, 'facedatabase1')

