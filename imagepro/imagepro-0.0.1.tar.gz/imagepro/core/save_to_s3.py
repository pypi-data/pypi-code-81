import io


def save_to_s3(connection, bucket_name, key_name, image):
    """
    Save image to S3

    Args:
        connection (boto3.object): S3 connection
        bucket_name (str): bucket name
        key_name (str): key name
        image (stream data): image

    Output:
        flag (int): 1 for success
    """
    in_mem_file = io.BytesIO()
    image.save(in_mem_file, format='png')
    in_mem_file.seek(0)
    try:
        connection.upload_fileobj(
            in_mem_file,
            bucket_name,
            key_name
        )
        return 1
    except Exception as error:
        raise error
