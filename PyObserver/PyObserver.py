# -*- coding:utf-8 -*-
import requests
import socket
import json
import pickle
import psutil
import msvcrt
import zlib
import time
import datetime

AVAILABLE_URL = '/observer-mode'
VERSION_URL = '/observer-mode/rest/consumer/version'
METADATA_URL = '/observer-mode/rest/consumer/getGameMetaData/%s/%s/1/token'
CHUNKINFO_URL = '/observer-mode/rest/consumer/getLastChunkInfo/%s/%s/1/token'
CHUNKDATA_URL = '/observer-mode/rest/consumer/getGameDataChunk/%s/%s/%s/token'
GAMESTATS_URL = '/observer-mode/rest/consumer/endOfGameStats/%s/%s/token'
KEYFRAME_URL = '/observer-mode/rest/consumer/getKeyFrame/%s/%s/%s/token'
END_URL = '/observer-mode/rest/consumer/end/%s/%s/1/token'


# def waiting_for_game():
#     host = socket.gethostbyname(socket.gethostname())
#     s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
#     s.bind((host, 0))
#     s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
#     s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
#
#     while True:
#         data = s.recv(65535)
#         keyword = 'getGameMetaData/'
#         offset = len(keyword)
#         resule = data.find(keyword)
#         if resule != -1:
#             print data
#             data = data[resule + offset:]
#             data = data.split('/')
#             s.close()
#             return data[0], data[1]


def get_running_game():
    for proc in psutil.process_iter():
        cmdline = proc.cmdline()
        if len(cmdline) > 0:
            print cmdline
            if cmdline[0].find('League of Legends') != -1 and len(cmdline) >= 5:
                cmdline = cmdline[4]
                cmdline = cmdline.split(' ')
                if cmdline[1].find('127.0.0.1') != -1:
                    continue
                cmdline = {
                    'server': 'http://' + cmdline[1],
                    'encryption_key': cmdline[2],
                    'platform': cmdline[4],
                    'game_id': cmdline[3]
                }
                yield cmdline


# def get_end_of_game_stats(server, platform, game_id):
#     response = requests.get(server + GAMESTATS_URL % (platform, game_id))
#     if response.ok:
#         return response.text


# def get_end_info(server, platform, game_id, retry=0):
#     repeat = 0
#     while True:
#         response = requests.get(server + END_URL % (platform, game_id))
#         if response.ok:
#             return response.text
#         repeat += 1
#         if repeat > retry > 0:
#             return


# def gen_last_chunk_info(last_chunk_info):
#     json_dict = json.loads(last_chunk_info)
#     json_dict['chunkId'] = json_dict['startGameChunkId']
#     json_dict['keyFrameId'] = 1
#     json_dict['availableSince'] = 0
#     json_dict['nextAvailableChunk'] = 29989
#     json_dict['nextChunkId'] = json_dict['chunkId']
#     return json.dumps(json_dict)


class RecordData:
    def __init__(self, server, platform, game_id, encryption_key):
        self.server = server
        self.platform = platform
        self.game_id = game_id
        self.encryption_key = encryption_key
        if self.check_observer_server_available() is False:
            raise Exception('Error: Observer server is down.')
        self.version = self.get_observer_server_version()
        self.game_meta_data = self.get_game_meta_data()
        self.last_chunk_info = self.get_last_chunk_info()
        self.key_frame_dict = dict()
        self.game_data_chunk_dict = dict()
        self.chunk_frame_map = dict()
        self.initialized = False


    # def __getitem__(self, item):
    #     print item

    def check_observer_server_available(self):
        return requests.get(self.server + AVAILABLE_URL).ok

    def get_observer_server_version(self):
        respond = requests.get(self.server + VERSION_URL)
        if respond.ok:
            return respond.text

    def get_last_chunk_info(self):
        response = requests.get(self.server + CHUNKINFO_URL % (self.platform, self.game_id))
        if response.ok:
            jsons = response.text
            return json.loads(jsons)

    def get_game_meta_data(self):
        response = requests.get(self.server + METADATA_URL % (self.platform, self.game_id))
        if response.ok:
            jsons = response.text
            return json.loads(jsons)

    def get_key_frame(self, key_frame_id, retry=0):
        repeat = 0
        while True:
            response = requests.get(self.server + KEYFRAME_URL % (self.platform, self.game_id, key_frame_id),
                                    stream=True)
            if response.ok:
                data = str()
                for block in response.iter_content(1024):
                    if not block:
                        break
                    data += block
                return data
            repeat += 1
            if repeat > retry > 0:
                return

    def get_game_data_chunk(self, chunk_id, retry=0):
        repeat = 0
        while True:
            response = requests.get(self.server + CHUNKDATA_URL % (self.platform, self.game_id, chunk_id), stream=True)
            if response.ok:
                data = str()
                for block in response.iter_content(1024):
                    if not block:
                        break
                    data += block
                print 'chunk_id:', chunk_id
                print len(data)
                return data
            repeat += 1
            if repeat > retry > 0:
                print 'here'
                return

    # def get_start_timestamp(self):
    #     if self.game_meta_data is not None:
    #         if 'startTime' in self.game_meta_data:
    #             return float(self.game_meta_data['startTime'])
    #         else:
    #             return None

    def get_game_length(self):
        if self.game_meta_data is not None:
            game_length = self.game_meta_data['gameLength']
            return game_length * 0.001

    # def get_end_timestamp(self):
    #     if self.game_meta_data is not None:
    #         if 'endTime' in self.game_meta_data:
    #             return float(self.game_meta_data['endTime'])
    #         else:
    #             return None

    def initialize(self):
        for key_frame_id in range(self.last_chunk_info['keyFrameId'] + 1):
            key_frame = self.get_key_frame(key_frame_id, 5)
            if key_frame is not None:
                self.key_frame_dict[key_frame_id] = key_frame
        for chunk_id in range(self.last_chunk_info['chunkId'] + 1):
            chunk = self.get_game_data_chunk(chunk_id, 5)
            if chunk is not None:
                self.game_data_chunk_dict[chunk_id] = chunk
        self.initialized = True

    def start_recording(self):
        while True:
            if self.record() is False:
                break

    def record(self):
        last_chunk_info = self.get_last_chunk_info()
        if last_chunk_info is None:
            return False
        if self.last_chunk_info['keyFrameId'] == 0:
            self.last_chunk_info = last_chunk_info
        chunk_id = last_chunk_info['chunkId']
        key_frame_id = last_chunk_info['keyFrameId']
        if key_frame_id not in self.key_frame_dict and key_frame_id > 0:
            self.key_frame_dict[key_frame_id] = self.get_key_frame(key_frame_id)
        if chunk_id not in self.game_data_chunk_dict and chunk_id > 0:
            self.game_data_chunk_dict[chunk_id] = self.get_game_data_chunk(chunk_id)
            if key_frame_id > 0:
                self.chunk_frame_map[chunk_id] = key_frame_id
        self.game_meta_data = self.get_game_meta_data()
        if last_chunk_info['endGameChunkId'] == last_chunk_info['chunkId']:
            return False

    def save_to_file(self, filename=None):
        text = pickle.dumps(self)
        text = zlib.compress(text)
        if filename is None:
            filename = '%s.lob' % (self.platform + '_' + self.game_id)
        f = open(filename, 'wb')
        f.write(text)
        f.close()

    @staticmethod
    def load_from_file(filename):
        f = open(filename, 'rb')
        text = f.read()
        f.close()
        text = zlib.decompress(text)
        return pickle.loads(text)


if __name__ == '__main__':
    while True:
        for game in get_running_game():
            server = game['server']
            encryption_key = game['encryption_key']
            platform = game['platform']
            game_id = game['game_id']
        print server, platform, game_id
        record_data = RecordData(server, platform, game_id, encryption_key)
        record_data.initialize()
        print 'record'
        while True:
            if record_data.record() is False:
                break
        record_data.save_to_file()