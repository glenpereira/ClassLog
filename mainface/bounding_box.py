import boto3
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor
from mainface.s3_functions import *
from mainface.search_for_face import *

def show_faces(photo,bucket):
     

    client=boto3.client('rekognition')
    upload_file(photo, bucket) #upload main photo to bucket
    # Load image from S3 bucket
    s3_connection = boto3.resource('s3')
    s3_object = s3_connection.Object(bucket,photo)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image=Image.open(stream)
    
    #Call DetectFaces 
    response = client.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
        Attributes=['ALL'])

    imgWidth, imgHeight = image.size   
    draw = ImageDraw.Draw(image)
    face_area = []
                    
    # calculate and display bounding boxes for each detected face       
    print('Detected faces for ' + photo)    
    for faceDetail in response['FaceDetails']:
        print('The detected face is between ' + str(faceDetail['AgeRange']['Low']) 
              + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
        
        box = faceDetail['BoundingBox']
        left = imgWidth * box['Left']
        top = imgHeight * box['Top']
        width = imgWidth * box['Width']
        height = imgHeight * box['Height']

        area = (left, top, width, height)

        face_area.append(area)
                

        print('Left: ' + '{0:.0f}'.format(left))
        print('Top: ' + '{0:.0f}'.format(top))
        print('Face Width: ' + "{0:.0f}".format(width))
        print('Face Height: ' + "{0:.0f}".format(height))

        print("Area: " + str(face_area))

        points = (
            (left,top),
            (left + width, top),
            (left + width, top + height),
            (left , top + height),
            (left, top)

        )
        draw.line(points, fill='#00d400', width=2)

        # Alternatively can draw rectangle. However you can't set line width.
        #draw.rectangle([left,top, left + width, top + height], outline='#00d400') 

    crop_master_image = image
    num = 0
    faces = []

    for box in face_area:
        x,y,w,h = box
        #print(x + y + w + h)
        crop_img = crop_master_image.crop((x, y, x+w, y+h))
        crop_img.save("crop_{}.jpg".format(num))
        upload_file("crop_{}.jpg".format(num), bucket)
        faces.append(search_face("crop_{}.jpg".format(num), bucket))
        print(faces)
        num += 1
       
   # image.show() #//show the image in desktop

    # return len(response['FaceDetails'])
    return faces

# def main():
#     bucket="classlogpublic"
#     photo="IMG_4137.jpg"

#     faces_count=show_faces(photo,bucket)
#     print("faces detected: " + str(faces_count))


# if __name__ == "__main__":
#     main()