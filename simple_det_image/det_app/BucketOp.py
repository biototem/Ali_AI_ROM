import oss2
import cv2


class Bucket(object):
    def __init__(self, AccessKeyid='LTAI4GB9aSoCseAsc6iUWWz7', AccessKeySecret='vSdxbd3uxpZLspZlNpBsjcYpTQj7fl',
                 region='cn-shanghai', BucketName=None):
        self.auth = oss2.Auth(AccessKeyid, AccessKeySecret)
        if BucketName is not None:
            self.bucket = oss2.Bucket(self.auth, 'http://oss-{region}.aliyuncs.com'.format(region=region),
                                      BucketName)
        else:
            self.bucket = None

    def SimpleImageFileUpload(self, oss_file_path, local_file_path):
        if self.bucket is None:
            raise ValueError("you must specify bucketname")

        self.bucket.put_object_from_file(oss_file_path, local_file_path)

    def SimpleImageDataUpload(self, oss_file_path, im_name, im_data):
        if self.bucket is None:
            raise ValueError("you must specify bucketname")

        r, im_data = cv2.imencode('.jpg', cv2.cvtColor(im_data, cv2.COLOR_BGR2RGB))
        if not r:
            raise RuntimeError('cv2.imencode failure')
        im_data = bytes(im_data)
        headers = oss2.utils.set_content_type(oss2.http.CaseInsensitiveDict(None), im_name)
        self.bucket.put_object(oss_file_path, im_data, headers=headers)

    def GetAllFileOssPath(self):
        if self.bucket is None:
            raise ValueError("you must specify bucketname")

        path = []
        for obj in oss2.ObjectIterator(self.bucket):
            path.append(obj)
        return path

    def GetSpecifiedDir(self, prefix):
        if self.bucket is None:
            raise ValueError("you must specify bucketname")

        files = []
        for obj in oss2.ObjectIterator(self.bucket, prefix=prefix):
            files.append(obj.key)
        return files

    def DeleteOssFile(self, file_path):
        if self.bucket is None:
            raise ValueError("you must specify bucketname")

        if isinstance(file_path, str):
            self.bucket.delete_object(file_path)
        elif isinstance(file_path, list):
            # 批量删除文件。每次最多删除1000个文件。
            result = self.bucket.batch_delete_objects(file_path)
            # 打印成功删除的文件名。
            print('\n'.join(result.deleted_keys))
        else:
            raise ValueError("file_path must be str or list")

    def DeteleSpecifiedDir(self, prefix):
        if self.bucket is None:
            raise ValueError("you must specify bucketname")

        # 删除指定前缀的文件
        for obj in oss2.ObjectIterator(self.bucket, prefix=prefix):
            self.bucket.delete_object(obj.key)


if __name__ == "__main__":
    import imageio
    bucket = Bucket(BucketName="bio-totem")
    bucket.SimpleImageFileUpload("img/18.jpg", "18.jpg")
    bucket.SimpleImageDataUpload("img/18.jpg", "18.jpg", imageio.imread("18.jpg"))
    # bucket.GetAllFileOssPath()
    # bucket.GetSpecifiedDir(prefix="image")
