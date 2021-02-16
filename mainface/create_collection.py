import boto3

def create_collection(collection_id):

    client = boto3.client("rekognition")

    print("Creating a collection: " + collection_id)
    response = client.create_collection(CollectionId=collection_id)
    print("Collection ARN: " + response["CollectionArn"])
    print("Status Code: " + str(response["StatusCode"]))
    print("Done.")

def main():
    collection_id = "tempcol"
    create_collection(collection_id)

if __name__ == "__main__":
    main()