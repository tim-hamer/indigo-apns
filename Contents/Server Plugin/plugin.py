#! /usr/bin/env python # -*- coding: utf-8 -*-
####################

import sys, os, pprint
from apns import APNs, Payload

class Plugin(indigo.PluginBase):

############## --- Indigo Plugin Methods --- ##############

    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.debug = True

	def __del__(self):
		indigo.PluginBase.__del__(self)

	def startup(self):
		self.debugLog(u"startup called")

	def shutdown(self):
		self.debugLog(u"shutdown called")

############## --- Helper Methods --- ##############

    def getToken(self, device):
        token = device.pluginProps['token']
        return token

    def methodFromString(self, device, prefix, methodName):
        if methodName is None or prefix is None:
            self.debugLog(u"ERROR: both prefix and method name must be specified.")
            return
        fullName = prefix+"."+methodName
        try:
            return getattr(self.getServer(device), fullName)
        except AttributeError:
            self.debugLog(u"ERROR: method not found for '"+fullName+"'")
            return None

############## --- Action Methods --- ##############

    def sendNotification(self, action, device):
        token = self.getToken(device)
        cert = self.pluginPrefs["certificateField"]
        key = self.pluginPrefs["privateKeyField"]
        useSandbox = self.pluginPrefs["useSandbox"]

        alertStr = action.props['alert']
        badgeNum = action.props['badge']
        soundName = action.props['sound']

        apns = APNs(use_sandbox=useSandbox, cert_file=cert, key_file=key)
        payload = Payload(alert=alertStr, sound=soundName, badge=badgeNum)
        apns.gateway_server.send_notification(token, payload)
