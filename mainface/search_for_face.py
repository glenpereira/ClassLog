import boto3

client = boto3.client("rekognition")

def search_face(photo, bucket):

    try:
        collection_id = "CSA2023"
        threshold = 70
        # maxFaces = 2

        response = client.search_faces_by_image(CollectionId=collection_id, Image={"S3Object":{"Bucket":bucket, "Name":photo}}, QualityFilter="LOW")

        faceMatches = response["FaceMatches"]
        print("Matching faces ")
        for match in faceMatches:
            print("Similarity: " + "{:.2f}".format(match["Similarity"]) + "%")
            return (str(match["Face"]["ExternalImageId"]))
        
    except client.exceptions.InvalidParameterException as e:
        return None
        
    
        