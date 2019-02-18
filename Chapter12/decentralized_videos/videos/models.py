import os.path, json
import ipfsapi
import cv2
from web3 import Web3, IPCProvider
from populus.utils.wait import wait_for_transaction_receipt
from decentralized_videos.settings import STATICFILES_DIRS, STATIC_URL, BASE_DIR, MEDIA_ROOT


class VideosSharing:

    def __init__(self):
        self.w3 = Web3(IPCProvider('/tmp/geth.ipc'))
        with open('../address.txt', 'r') as f:
            address = f.read().rstrip("\n")

        with open('../videos_sharing_smart_contract/build/contracts.json') as f:
            contract = json.load(f)
            abi = contract['VideosSharing']['abi']

        self.SmartContract = self.w3.eth.contract(address=address, abi=abi)

        self.ipfs_con = ipfsapi.connect()

    def recent_videos(self, amount=20):
        events = self.SmartContract.events.UploadVideo.createFilter(fromBlock=0).get_all_entries()
        videos = []
        for event in events:
            video = {}
            video['user'] = event['args']['_user']
            video['index'] = event['args']['_index']
            video['path'] = self.get_video_path(video['user'], video['index'])
            video['title'] = self.get_video_title(video['user'], video['index'])
            video['thumbnail'] = self.get_video_thumbnail(video['path'])
            videos.append(video)
        videos.reverse()
        return videos[:amount]

    def get_videos(self, user, amount=20):
        latest_index = self.SmartContract.functions.latest_videos_index(user).call()
        i = 0
        videos = []
        while i < amount and i < latest_index:
            video = {}
            index = latest_index - i - 1
            video['user'] = user
            video['index'] = index
            video['path'] = self.get_video_path(user, index)
            video['title'] = self.get_video_title(user, index)
            video['thumbnail'] = self.get_video_thumbnail(video['path'])
            videos.append(video)
            i += 1
        return videos

    def get_video_path(self, user, index):
        return self.SmartContract.functions.videos_path(user, index).call().decode('utf-8')

    def get_video_title(self, user, index):
        return self.SmartContract.functions.videos_title(user, index).call().decode('utf-8')

    def get_video_thumbnail(self, ipfs_path):
        thumbnail_file = STATICFILES_DIRS[0] + '/' + ipfs_path + '.png'
        url_file = STATIC_URL + '/' + ipfs_path + '.png'
        if os.path.isfile(thumbnail_file):
            return url_file
        else:
            return "https://bulma.io/images/placeholders/640x480.png"

    def get_video(self, user, index):
        video = {}
        ipfs_path = self.get_video_path(user, index)
        video_title = self.get_video_title(user, index)
        video_file = STATICFILES_DIRS[0] + '/' + ipfs_path + '.mp4'
        thumbnail_file = STATICFILES_DIRS[0] + '/' + ipfs_path + '.png'
        video['title'] = video_title
        video['user'] = user
        video['index'] = index
        video['aggregate_likes'] = self.SmartContract.functions.video_aggregate_likes(user, index).call()

        if os.path.isfile(video_file):
            video['url'] = STATIC_URL + '/' + ipfs_path + '.mp4'
        else:
            self.ipfs_con.get(ipfs_path)
            os.rename(BASE_DIR + '/' + ipfs_path, STATICFILES_DIRS[0] + '/' + ipfs_path + '.mp4')
            video['url'] = STATIC_URL + '/' + ipfs_path + '.mp4'

        if not os.path.isfile(thumbnail_file):
            self.process_thumbnail(ipfs_path)

        return video

    def upload_video(self, video_user, password, video_file, title):
        video_path = MEDIA_ROOT + '/video.mp4'
        with open(video_path, 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)
        ipfs_add = self.ipfs_con.add(video_path)
        ipfs_path = ipfs_add['Hash'].encode('utf-8')
        title = title[:20].encode('utf-8')
        nonce = self.w3.eth.getTransactionCount(Web3.toChecksumAddress(video_user))
        txn = self.SmartContract.functions.upload_video(ipfs_path, title).buildTransaction({
                    'from': video_user,
                    'gas': 200000,
                    'gasPrice': self.w3.toWei('30', 'gwei'),
                    'nonce': nonce
                  })
        txn_hash = self.w3.personal.sendTransaction(txn, password)
        wait_for_transaction_receipt(self.w3, txn_hash)

    def process_thumbnail(self, ipfs_path):
        thumbnail_file = STATICFILES_DIRS[0] + '/' + ipfs_path + '.png'
        if not os.path.isfile(thumbnail_file):
            video_path = STATICFILES_DIRS[0] + '/' + ipfs_path + '.mp4'
            cap = cv2.VideoCapture(video_path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            _, frame = cap.read()
            cv2.imwrite(thumbnail_file, frame)

    def like_video(self, video_liker, password, video_user, index):
        if self.SmartContract.functions.video_has_been_liked(video_liker, video_user, index).call():
            return
        nonce = self.w3.eth.getTransactionCount(Web3.toChecksumAddress(video_liker))
        txn = self.SmartContract.functions.like_video(video_user, index).buildTransaction({
                    'from': video_liker,
                    'gas': 200000,
                    'gasPrice': self.w3.toWei('30', 'gwei'),
                    'nonce': nonce
                  })
        txn_hash = self.w3.personal.sendTransaction(txn, password)
        wait_for_transaction_receipt(self.w3, txn_hash)


videos_sharing = VideosSharing()
