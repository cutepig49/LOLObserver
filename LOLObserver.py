# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
from PyObserver import RecordData, get_running_game
import json
import time
import win32api
import pickle
import traceback
import thread
import requests

import os

record_data = None


# def bf_ecb_decrypt(key, data):
#     return Blowfish.new(key, Blowfish.MODE_ECB).decrypt(data)


class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(record_data.version)


class MetaDataHandler(tornado.web.RequestHandler):
    def get(self, platform, game_id):
        print 'request game:', platform, game_id
        record_data.game_meta_data['gameEnded'] = True
        record_data.game_meta_data['pendingAvailableChunkInfo'] = []
        record_data.game_meta_data['pendingAvailableKeyFrameInfo'] = []
        record_data.game_meta_data['clientBackFetchingEnabled'] = True
        self.write(json.dumps(record_data.game_meta_data))


total_time = 0
last_request_time = 0
curr_frame_id = 0
curr_chunk_id = 0
last_update_time = 0
num_chunks = 0
chunk_requested = False
delta = 0
last_flag = False


class LastChunkInfoHandler(tornado.web.RequestHandler):
    def get_first_chunk(self):
        last_chunk_info_copy = dict(record_data.last_chunk_info)
        chunk_ids = record_data.chunk_frame_map.keys()
        chunk_ids.sort()
        last_chunk_info_copy['chunkId'] = chunk_ids[0]
        last_chunk_info_copy['keyFrameId'] = record_data.chunk_frame_map[last_chunk_info_copy['chunkId']]
        last_chunk_info_copy['nextChunkId'] = last_chunk_info_copy['chunkId']
        last_chunk_info_copy['endGameChunkId'] = chunk_ids[-1]
        return last_chunk_info_copy

    def get_last_chunk(self):
        last_chunk_info_copy = dict(record_data.last_chunk_info)
        chunk_ids = record_data.chunk_frame_map.keys()
        chunk_ids.sort()
        last_chunk_info_copy['endGameChunkId'] = chunk_ids[-1]
        last_chunk_info_copy['chunkId'] = chunk_ids[-1]
        last_chunk_info_copy['keyFrameId'] = record_data.chunk_frame_map[chunk_ids[-1]]
        last_chunk_info_copy['nextChunkId'] = last_chunk_info_copy['chunkId']
        return last_chunk_info_copy

    def get(self, platform, game_id):
        global total_time
        global last_request_time
        global curr_chunk_id
        global curr_frame_id
        global last_update_time
        global num_chunks
        global chunk_requested
        global delta
        global last_flag
        if last_update_time == 0:
            last_update_time = time.time() * 1000
        if last_request_time == 0:
            last_request_time = time.time() * 1000
        record_data.last_chunk_info['availableSince'] += time.time() * 1000 - last_request_time
        total_time += time.time() * 1000 - last_request_time
        if curr_frame_id == 0:
            chunk_ids = record_data.chunk_frame_map.keys()
            chunk_ids.sort()
            curr_chunk_id = chunk_ids[0]
            curr_frame_id = record_data.chunk_frame_map[curr_chunk_id]
        # print last_chunk_info_copy['keyFrameId']
        # print last_chunk_info_copy['chunkId']
        # print 'send keyFrameId:', last_chunk_info_copy['keyFrameId']
        # print 'send chunkId:', last_chunk_info_copy['chunkId']
        # print 'availableSince:', last_chunk_info_copy['availableSince']
        # if curr_chunk_id + 1 in record_data.game_data_chunk_dict:
        #     curr_chunk_id += 1
        #     num_chunks += 1
        # else:
        #     record_data.last_chunk_info['endGameChunkId'] = curr_chunk_id
        #     last_chunk_info_copy['endGameChunkId'] = curr_chunk_id
        # if curr_chunk_id in record_data.chunk_frame_map:
        #     curr_frame_id = record_data.chunk_frame_map[curr_chunk_id]

        # if time.time() * 1000 - last_request_time < 10000 and delta > 10000 and last_flag is False:
        #     last_flag = True
        #     print len(record_data.key_frame_dict) - 20
        #     time.sleep(len(record_data.key_frame_dict) - 20)
        #     print 'here'
        if last_flag:
            last_chunk_info_copy = self.get_last_chunk()
        else:
            last_chunk_info_copy = self.get_first_chunk()
        last_chunk_info_copy = self.get_last_chunk()
        self.write(json.dumps(last_chunk_info_copy))
        delta = time.time() * 1000 - last_request_time
        last_request_time = time.time() * 1000
        return
        if chunk_requested:
            chunk_requested = False
            if time.time() * 1000 - last_update_time > 2000:
                print time.time() * 1000 - last_update_time
                last_update_time = time.time() * 1000
                if curr_chunk_id + 10 in record_data.chunk_frame_map:
                    curr_chunk_id += 10
                    curr_frame_id = record_data.chunk_frame_map[curr_chunk_id]
                else:
                    chunk_ids = record_data.chunk_frame_map.keys()
                    chunk_ids.sort()
                    curr_chunk_id = chunk_ids[-1]
                    curr_frame_id = record_data.chunk_frame_map[curr_chunk_id]
                    record_data.last_chunk_info['endGameChunkId'] = curr_chunk_id
        last_chunk_info_copy = dict(record_data.last_chunk_info)
        last_chunk_info_copy['keyFrameId'] = curr_frame_id
        last_chunk_info_copy['chunkId'] = curr_chunk_id
        self.write(json.dumps(last_chunk_info_copy))


class GameDataChunkHandler(tornado.web.RequestHandler):
    def get(self, platform, game_id, chunk_id):
        chunk_id = int(chunk_id)
        print 'request chunk:', chunk_id, chunk_id in record_data.game_data_chunk_dict
        global chunk_requested
        global curr_chunk_id
        if chunk_id == curr_chunk_id:
            chunk_requested = True
        if chunk_id in record_data.game_data_chunk_dict:
            self.set_header('Content-Type', 'application/octet-stream')
            self.write(record_data.game_data_chunk_dict[chunk_id])
        else:
            self.write_error(500)


class KeyFrameHandler(tornado.web.RequestHandler):
    def get(self, platform, game_id, key_frame_id):
        key_frame_id = int(key_frame_id)
        print 'request keyframe:', key_frame_id, key_frame_id in record_data.key_frame_dict
        global first_keyframe_requested
        first_keyframe_requested = True
        if key_frame_id in record_data.key_frame_dict:
            self.set_header('Content-Type', 'application/octet-stream')
            self.write(record_data.key_frame_dict[key_frame_id])
        else:
            self.write_error(500)


class EndInfoHandler(tornado.web.RequestHandler):
    def get(self, platform, game_id):
        if 'end_info' in record_data:
            pass
        else:
            self.write_error(500)


def start_observe(client_path, rd):
    params = '"8391" "" "" "spectator %s %s %s %s"' % ('127.0.0.1:8088', rd.encryption_key, rd.game_id, rd.platform)
    print params
    global record_data
    record_data = rd
    client_dir = os.path.dirname(client_path)
    win32api.ShellExecute(0, 'open', client_path, params, client_dir, 0)


import wx
import WxGui


def reset_global_variables():
    global last_request_time
    global curr_chunk_id
    global curr_frame_id
    global last_update_time
    global chunk_requested
    global total_time
    total_time = 0
    chunk_requested = False
    last_update_time = 0
    last_request_time = 0
    curr_chunk_id = 0
    curr_frame_id = 0


class MainFrame(WxGui.MainFrame):
    def __init__(self):
        super(MainFrame, self).__init__(None)
        self.config_dict = dict()
        self.game_dict = dict()
        self.download_dict = dict()
        self.recording_dict = dict()

        if os.path.exists('config.bin'):
            with open('config.bin', 'rb') as f:
                self.config_dict = pickle.load(f)
        if 'record_path' not in self.config_dict:
            self.config_dict['record_path'] = os.path.join(os.environ['APPDATA'], 'LOLObserverRecord')
        if not os.path.exists(self.config_dict['record_path']):
            os.makedirs(self.config_dict['record_path'])
        self.update_game_dict()
        self.download_loop_thread = thread.start_new_thread(self.download_loop, ())
        self.home_browser.SetPage(requests.get('http://lolobserver.sinaapp.com/').text)
        self.help_browser.SetPage(requests.get('http://lolobserver.sinaapp.com/help').text)
        self.check_new_version()

    def update_game_dict(self):
        self.game_dict.clear()
        for root, dirs, files in os.walk(self.config_dict['record_path']):
            for f in files:
                filename = os.path.join(root, f)
                rd = RecordData.load_from_file(filename)
                self.game_dict[rd.game_id] = {
                    'game_length': rd.get_game_length(),
                    'platform': rd.platform,
                    'filename': filename
                }
        self.update_game_page()

    def update_game_page(self):
        existed_page = []
        for index in xrange(self.game_listbook.GetPageCount()):
            if self.game_listbook.GetPageText(index) not in self.game_dict:
                self.game_listbook.RemovePage(index)
            else:
                existed_page.append(self.game_listbook.GetPageText(index))
        for game_id in self.game_dict:
            if game_id in existed_page:
                continue
            panel = wx.Panel(self.game_listbook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
            sizer = wx.BoxSizer(wx.VERTICAL)
            button = wx.Button(panel, wx.ID_ANY, u'Play', wx.DefaultPosition, wx.DefaultSize, 0)
            button.Bind(wx.EVT_BUTTON, self.button_playOnButtonClick)
            sizer.Add(button, 1, wx.ALL | wx.EXPAND, 5)
            panel.SetSizer(sizer)
            panel.Layout()
            sizer.Fit(panel)
            self.game_listbook.AddPage(panel, game_id, False)

    def check_new_version(self):
        if json.loads(requests.get('http://lolobserver.sinaapp.com/version').text)['version'] > self.version():
            result = wx.MessageBox(u'软件已更新，是否到主页下载最新版本？', u'发现更新', wx.YES_NO)
            if result == wx.YES:
                win32api.ShellExecute(0, 'open', 'http://lolobserver.sinaapp.com', '', '', 0)


    def button_playOnButtonClick(self, event):
        global record_data
        record_info = self.game_dict[self.game_listbook.GetPageText(self.game_listbook.GetSelection())]
        rd = RecordData.load_from_file(record_info['filename'])
        start_observe(self.config_dict['client_path'], rd)

    def update_record_page(self):
        existed_page = []
        for index in xrange(self.download_listbook.GetPageCount()):
            if self.download_listbook.GetPageText(index) not in self.recording_dict:
                self.download_listbook.RemovePage(index)
            else:
                existed_page.append(self.download_listbook.GetPageText(index))
        for game_id in self.recording_dict:
            if game_id in existed_page:
                continue
            panel = wx.Panel(self.download_listbook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
            self.download_listbook.AddPage(panel, game_id, False)


    def MainFrameOnClose(self, event):
        with open('config.bin', 'wb') as f:
            pickle.dump(self.config_dict, f)
        os.sys.exit()


    def download_loop(self):
        while True:
            for game_info in get_running_game():
                if game_info['game_id'] in self.recording_dict:
                    continue
                self.recording_dict[game_info['game_id']] = RecordData(game_info['server'], game_info['platform'],
                                                                       game_info['game_id'],
                                                                       game_info['encryption_key'])
            wx.CallAfter(self.update_record_page)
            pop_list = []
            for game_id in self.recording_dict:
                if self.recording_dict[game_id].initialized is False:
                    self.recording_dict[game_id].initialize()
                if self.recording_dict[game_id].record() is False:
                    pop_list.append(game_id)
                    rd = self.recording_dict[game_id]
                    save_path = os.path.join(self.config_dict['record_path'], '%s_%s.lob' % (rd.platform, rd.game_id))
                    rd.save_to_file(save_path)
                    print save_path
                    wx.CallAfter(self.update_game_dict)
            for pop_game in pop_list:
                self.recording_dict.pop(pop_game)
            wx.CallAfter(self.update_record_page)

    @staticmethod
    def version():
        return 1

    def button_choose_clientOnButtonClick(self, event):
        file_wildcard = 'Leagued Of Legends.exe(League Of Leagends.exe)|League Of Legends.exe'
        dlg = wx.FileDialog(self, 'Open League Of Legends.exe:',
                            os.getcwd(), style=wx.OPEN, wildcard=file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.txt_client_path.SetValue(dlg.GetPath())
        dlg.Destroy()

    def button_choose_record_dirOnButtonClick(self, event):
        dlg = wx.DirDialog(self, 'Choose record directory:', style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            self.txt_lob_path.SetValue(dlg.GetPath())
        dlg.Destroy()

    def button_applyOnButtonClick(self, event):
        self.config_dict['client_path'] = self.txt_client_path.GetValue()
        self.config_dict['record_path'] = self.txt_lob_path.GetValue()

    def button_cancelOnButtonClick(self, event):
        self.txt_client_path.SetValue(self.config_dict.get('client_path', ''))
        self.txt_lob_path.SetValue(self.config_dict['record_path'])

    def m_notebook2OnNotebookPageChanged(self, event):
        curr_page_title = self.m_notebook2.GetPageText(self.m_notebook2.GetSelection())
        if curr_page_title == u'首页':
            pass
        elif curr_page_title == u'我的录像':
            pass
        elif curr_page_title == u'下载列表':
            pass
        elif curr_page_title == u'帮助':
            pass
        elif curr_page_title == u'设置':
            client_path = self.config_dict.get('client_path', '')
            record_path = self.config_dict.get('record_path', '')
            self.txt_client_path.SetValue(client_path)
            self.txt_lob_path.SetValue(record_path)

            # def open_menu_itemOnMenuSelection(self, event):
            #     file_type = 'LOL Observer File(*.lob)|*.lob'
            #     dlg = wx.FileDialog(self, 'Open Observer File',
            #                         os.getcwd(), style=wx.OPEN, wildcard=file_type)
            #     if dlg.ShowModal() == wx.ID_OK:
            #         self.stop_tornado()
            #         self.txt_filename.SetLabelText(os.path.basename(dlg.GetPath()))
            #         self.record_data = RecordData.load_from_file(dlg.GetPath())
            #         self.txt_game_id.SetLabelText(self.record_data.game_id)
            #         self.txt_platform.SetLabelText(self.record_data.platform)
            #         print self.record_data.key_frame_dict.keys()
            #         print self.record_data.game_data_chunk_dict.keys()
            #         print self.record_data.chunk_frame_map
            #         print self.record_data.last_chunk_info
            #         print self.record_data.game_meta_data
            #     dlg.Destroy()
            #     self.Layout()
            #
            # def stop_tornado(self):
            #     reset_global_variables()
            #
            # def btn_play_stopOnButtonClick(self, event):
            #     if 'client_path' not in self.config:
            #         file_wildcard = 'Leagued Of Legends.exe(League Of Leagends.exe)|League Of Legends.exe'
            #         dlg = wx.FileDialog(self, 'Open League Of Legends.exe',
            #                             os.getcwd(), style=wx.OPEN, wildcard=file_wildcard)
            #         if dlg.ShowModal() == wx.ID_OK:
            #             self.config['client_path'] = dlg.GetPath()
            #             with open('config.bin', 'wb') as f:
            #                 pickle.dump(self.config, f)
            #         dlg.Destroy()
            #     if self.btn_play_stop.GetLabelText() == 'Stop':
            #         self.stop_tornado()
            #         self.btn_play_stop.SetLabelText('Play')
            #     else:
            #         if self.record_data is not None and 'client_path' in self.config:
            #             self.stop_tornado()
            #             global record_data
            #             record_data = self.record_data
            #             start_observe(self.config['client_path'], '127.0.0.1:8088', record_data.platform, record_data.game_id,
            #                           record_data.encryption_key)
            #             self.btn_play_stop.SetLabelText('Stop')


application = tornado.web.Application([
    (r'/observer-mode/rest/consumer/version', VersionHandler),
    (
        r'/observer-mode/rest/consumer/getGameMetaData/([A-Za-z0-9_]+)/([0-9]+)/.+',
        MetaDataHandler),
    (
        r'/observer-mode/rest/consumer/getLastChunkInfo/([A-Za-z0-9_]+)/([0-9]+)/.+',
        LastChunkInfoHandler),
    (
        r'/observer-mode/rest/consumer/getGameDataChunk/([A-Za-z0-9_]+)/([0-9]+)/([0-9]+)/.+',
        GameDataChunkHandler),
    (
        r'/observer-mode/rest/consumer/getKeyFrame/([A-Za-z0-9_]+)/([0-9]+)/([0-9]+)/.+',
        KeyFrameHandler),
    (
        r'/observer-mode/rest/consumer/end/([A-Za-z0-9_]+)/([0-9]+)/.+',
        EndInfoHandler
    )
])

import thread


def tornado_main_loop():
    application.listen(8088)
    tornado.ioloop.IOLoop.instance().start()


def wx_main_frame():
    pass


if __name__ == "__main__":
    thread.start_new_thread(tornado_main_loop, ())
    app = wx.App()
    main_frame = MainFrame()
    main_frame.Show()
    app.MainLoop()
    # start_observe(client_path, '127.0.0.1:8088', record_data.platform, record_data.game_id,
    #               record_data.encryption_key)