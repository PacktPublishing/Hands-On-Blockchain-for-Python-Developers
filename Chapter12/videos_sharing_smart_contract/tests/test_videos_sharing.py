import pytest
import eth_tester


def upload_video(video_sharing, chain, account, video_path, video_title):
    txn_hash = video_sharing.functions.upload_video(video_path, video_title).transact({'from': account})
    chain.wait.for_receipt(txn_hash)

def transfer_coins(video_sharing, chain, source, destination, amount):
    txn_hash = video_sharing.functions.transfer(destination, amount).transact({'from': source})
    chain.wait.for_receipt(txn_hash)

def like_video(video_sharing, chain, video_liker, video_uploader, index):
    txn_hash = video_sharing.functions.like_video(video_uploader, index).transact({'from': video_liker})
    chain.wait.for_receipt(txn_hash)


def test_upload_video(web3, chain):
    video_sharing, _ = chain.provider.get_or_deploy_contract('VideosSharing')

    t = eth_tester.EthereumTester()
    video_uploader = t.get_accounts()[1]

    index = video_sharing.functions.latest_videos_index(video_uploader).call()
    assert index == 0

    upload_video(video_sharing, chain, video_uploader, b'video-ipfs-path', b"video title")

    index = video_sharing.functions.latest_videos_index(video_uploader).call()
    path = video_sharing.functions.videos_path(video_uploader, 0).call()
    title = video_sharing.functions.videos_title(video_uploader, 0).call()
    assert index == 1
    assert path == b'video-ipfs-path'
    assert title == b"video title"

    upload_video(video_sharing, chain, video_uploader, b'video-ipfs-path2', b"video title2")

    index = video_sharing.functions.latest_videos_index(video_uploader).call()
    path = video_sharing.functions.videos_path(video_uploader, 1).call()
    title = video_sharing.functions.videos_title(video_uploader, 1).call()
    assert index == 2
    assert path == b'video-ipfs-path2'
    assert title == b"video title2"

    events = video_sharing.events.UploadVideo.createFilter(fromBlock=0).get_all_entries()

    assert events[0]['args']['_user'] == video_uploader
    assert events[0]['args']['_index'] == 0

    assert events[1]['args']['_user'] == video_uploader
    assert events[1]['args']['_index'] == 1

def test_like_video(web3, chain):
    video_sharing, _ = chain.provider.get_or_deploy_contract('VideosSharing')

    t = eth_tester.EthereumTester()
    manager = t.get_accounts()[0]
    video_uploader = t.get_accounts()[1]
    video_liker = t.get_accounts()[2]
    video_liker2 = t.get_accounts()[3]

    transfer_coins(video_sharing, chain, manager, video_liker, 100)
    transfer_coins(video_sharing, chain, manager, video_liker2, 100)
    transfer_coins(video_sharing, chain, manager, video_uploader, 50)
    upload_video(video_sharing, chain, video_uploader, b'video-ipfs-path', b"video title")

    liked = video_sharing.functions.video_has_been_liked(video_liker, video_uploader, 0).call()
    assert liked == False
    liked2 = video_sharing.functions.video_has_been_liked(video_liker2, video_uploader, 0).call()
    assert liked2 == False
    video_uploader_balance = video_sharing.functions.balanceOf(video_uploader).call()
    assert video_uploader_balance == 50
    video_liker_balance = video_sharing.functions.balanceOf(video_liker).call()
    assert video_liker_balance == 100
    video_liker2_balance = video_sharing.functions.balanceOf(video_liker2).call()
    assert video_liker2_balance == 100
    aggregate_likes = video_sharing.functions.video_aggregate_likes(video_uploader, 0).call()
    assert aggregate_likes == 0

    like_video(video_sharing, chain, video_liker, video_uploader, 0)

    liked = video_sharing.functions.video_has_been_liked(video_liker, video_uploader, 0).call()
    assert liked == True
    liked2 = video_sharing.functions.video_has_been_liked(video_liker2, video_uploader, 0).call()
    assert liked2 == False
    video_uploader_balance = video_sharing.functions.balanceOf(video_uploader).call()
    assert video_uploader_balance == 51
    video_liker_balance = video_sharing.functions.balanceOf(video_liker).call()
    assert video_liker_balance == 99
    video_liker2_balance = video_sharing.functions.balanceOf(video_liker2).call()
    assert video_liker2_balance == 100
    aggregate_likes = video_sharing.functions.video_aggregate_likes(video_uploader, 0).call()
    assert aggregate_likes == 1

    like_video(video_sharing, chain, video_liker2, video_uploader, 0)

    liked = video_sharing.functions.video_has_been_liked(video_liker2, video_uploader, 0).call()
    assert liked == True
    liked2 = video_sharing.functions.video_has_been_liked(video_liker2, video_uploader, 0).call()
    assert liked2 == True
    video_uploader_balance = video_sharing.functions.balanceOf(video_uploader).call()
    assert video_uploader_balance == 52
    video_liker_balance = video_sharing.functions.balanceOf(video_liker).call()
    assert video_liker_balance == 99
    video_liker2_balance = video_sharing.functions.balanceOf(video_liker2).call()
    assert video_liker2_balance == 99
    aggregate_likes = video_sharing.functions.video_aggregate_likes(video_uploader, 0).call()
    assert aggregate_likes == 2

    events = video_sharing.events.LikeVideo.createFilter(fromBlock=0).get_all_entries()

    assert events[0]['args']['_video_liker'] == video_liker
    assert events[0]['args']['_video_uploader'] == video_uploader
    assert events[0]['args']['_index'] == 0

    assert events[1]['args']['_video_liker'] == video_liker2
    assert events[1]['args']['_video_uploader'] == video_uploader
    assert events[1]['args']['_index'] == 0

    with pytest.raises(eth_tester.exceptions.TransactionFailed):
        like_video(video_sharing, chain, video_liker, video_uploader, 0)
