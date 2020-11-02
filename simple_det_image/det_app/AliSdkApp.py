import os
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkfacebody.request.v20191230.HandPostureRequest import HandPostureRequest
from aliyunsdkfacebody.request.v20191230.BodyPostureRequest import BodyPostureRequest

from BucketOp import Bucket

import cv2


class AliSdkApp(Bucket):
    def __init__(self, AccessKeyid='', AccessKeySecret='',
                 region='cn-shanghai', BucketName=None, oss_img_save_dir=None):
        super(AliSdkApp, self).__init__(AccessKeyid=AccessKeyid,
                                        AccessKeySecret=AccessKeySecret,
                                        region=region,
                                        BucketName=BucketName)
        self.AccessKeyid = AccessKeyid
        self.AccessKeySecret = AccessKeySecret
        self.region = region
        self.BucketName = BucketName
        if oss_img_save_dir is None:
            self.img_save_dir = "image"
        else:
            self.img_save_dir = oss_img_save_dir

        self.client = AcsClient(AccessKeyid, AccessKeySecret, region)
        self.handPosture = HandPostureRequest()
        self.handPosture.set_accept_format('json')

        self.bodyPosture = BodyPostureRequest()
        self.bodyPosture.set_accept_format('json')

    # def HandPostureDetection(self, img_path):
    #     self.SimpleImageFileUpload(self.img_save_dir + '/' + os.path.basename(img_path), img_path)
    #
    #     self.handPosture.set_ImageURL("http://{BucketName}.oss-{region}.aliyuncs.com/{oss_file_path}".format(
    #         BucketName=self.BucketName,
    #         region=self.region,
    #         oss_file_path=self.img_save_dir + '/' + os.path.basename(img_path)))
    #
    #     response = self.client.do_action_with_exception(self.handPosture)
    #     return response

    def HandPostureDetection(self, im_name, im):
        self.SimpleImageDataUpload(self.img_save_dir + '/' + im_name, im_name, im)

        oss_file_path = self.img_save_dir + '/' + im_name

        self.handPosture.set_ImageURL("http://{BucketName}.oss-{region}.aliyuncs.com/{oss_file_path}".format(
            BucketName=self.BucketName,
            region=self.region,
            oss_file_path=oss_file_path))

        response = self.client.do_action_with_exception(self.handPosture)

        self.DeleteOssFile(oss_file_path)

        return response

    # def BodyPostureDetection(self, img_path):
    #     self.SimpleImageFileUpload(self.img_save_dir + '/' + os.path.basename(img_path), img_path)
    #
    #     self.bodyPosture.set_ImageURL("http://{BucketName}.oss-{region}.aliyuncs.com/{oss_file_path}".format(
    #         BucketName=self.BucketName,
    #         region=self.region,
    #         oss_file_path=self.img_save_dir + '/' + os.path.basename(img_path)))
    #
    #     response = self.client.do_action_with_exception(self.bodyPosture)
    #     return response

    def BodyPostureDetection(self, im_name, im):
        self.SimpleImageDataUpload(self.img_save_dir + '/' + im_name, im_name, im)

        oss_file_path = self.img_save_dir + '/' + im_name

        self.bodyPosture.set_ImageURL("http://{BucketName}.oss-{region}.aliyuncs.com/{oss_file_path}".format(
            BucketName=self.BucketName,
            region=self.region,
            oss_file_path=oss_file_path))

        response = self.client.do_action_with_exception(self.bodyPosture)

        self.DeleteOssFile(oss_file_path)

        return response


if __name__ == "__main__":
    hand = AliSdkApp(BucketName="")
    # response = hand.HandPostureDetection('19.jpg', cv2.imread("19.jpg", -1)[..., ::-1])
    response = hand.BodyPostureDetection('18.jpg', cv2.imread("18.jpg", -1)[..., ::-1])
    print(response)

    open('18.json', 'wb').write(response)
