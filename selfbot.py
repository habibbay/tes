# -*- coding: utf-8 -*-
from Bahan import LineClient
from Bahan.LineApi import LineTracer
from Bahan.LineThrift.ttypes import Message
from Bahan.LineThrift.TalkService import Client
import time, datetime, random ,sys, re, string, os, json

reload(sys)
sys.setdefaultencoding('utf-8')

client = LineClient()
client._qrLogin("line://au/q/")

profile, setting, tracer = client.getProfile(), client.getSettings(), LineTracer(client)
offbot, messageReq, wordsArray, waitingAnswer = [], {}, {}, {}

print client._loginresult()

wait = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{},
    'ProtectQR':False,
  #  "Protectguest":False,
  #  "Protectcancel":False,
  #  "protectionOn":True,	
   }

setTime = {}
setTime = wait["setTime"]

def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text

    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1
    client._client.sendMessage(messageReq[to], mes)
	
def NOTIFIED_ADD_CONTACT(op):
    try:
        sendMessage(op.param1, client.getContact(op.param1).displayName + " Thanks udah ngeadd 馃槝 ")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ADD_CONTACT\n\n")
        return

tracer.addOpInterrupt(5,NOTIFIED_ADD_CONTACT)

def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    #print op
    ginfo = client.getGroup(op.param1)
    try:
        sendMessage(op.param1,"Hi, " + client.getContact(op.param2).displayName + "\nSelamat Datang Di Grup :\n=> " + str(ginfo.name) + "\nOwner Grup Kami Adalah :\n=> " + str(ginfo.creator.displayName))
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ACCEPT_GROUP_INVITATION\n\n")
        return

tracer.addOpInterrupt(17,NOTIFIED_ACCEPT_GROUP_INVITATION)

def NOTIFIED_KICKOUT_FROM_GROUP(op):
    try:
	client.kickoutFromGroup(op.param1,[op.param2])
	sendMessage(op.param1, client.getContact(op.param3).displayName + "Bye! Kamu di kick Hahaha 魛渷魛厰Har Har魪靠")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_KICKOUT_FROM_GROUP\n\n")
        return

tracer.addOpInterrupt(19,NOTIFIED_KICKOUT_FROM_GROUP)

def NOTIFIED_LEAVE_GROUP(op):
    try:
        sendMessage(op.param1, client.getContact(op.param2).displayName + " Bye! Semoga bisa ketemu lagi ya 魛渷魛厰Har Har魪靠")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_LEAVE_GROUP\n\n")
        return

tracer.addOpInterrupt(15,NOTIFIED_LEAVE_GROUP)

def NOTIFIED_CANCEL_INVITATION_GROUP(op):
    try:
        client.kickoutFromGroup(op.param1,[op.param2])
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_CANCEL_INVITATION_GROUP\n\n")
        return

tracer.addOpInterrupt(32,NOTIFIED_CANCEL_INVITATION_GROUP)

def CANCEL_INVITATION_GROUP(op):
    try:
        client.cancelGroupInvitation(op.param1,[op.param3])
    except Exception as e:
        print e
        print ("\n\nCANCEL_INVITATION_GROUP\n\n")
        return

tracer.addOpInterrupt(31,CANCEL_INVITATION_GROUP)

def NOTIFIED_READ_MESSAGE(op):
    #print op
    try:
        if op.param1 in wait['readPoint']:
            Name = client.getContact(op.param2).displayName
            if Name in wait['readMember'][op.param1]:
                pass
            else:
                wait['readMember'][op.param1] += "\n銉�" + Name
                wait['ROM'][op.param1][op.param2] = "銉�" + Name
        else:
            pass
    except:
        pass

tracer.addOpInterrupt(55, NOTIFIED_READ_MESSAGE)

def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.to in wait['readPoint']:
                    if msg.from_ in wait["ROM"][msg.to]:
                        del wait["ROM"][msg.to][msg.from_]
                else:
                    pass
            except:
                pass
        else:
            pass
    except KeyboardInterrupt:
	       sys.exit(0)
    except Exception as error:
        print error
        print ("\n\nRECEIVE_MESSAGE\n\n")
        return

tracer.addOpInterrupt(26, RECEIVE_MESSAGE)

def SEND_MESSAGE(op):
    msg = op.message
    try:
        if msg.toType == 0:
            if msg.contentType == 0:
#-----------------------------------------------------------------------------------------------------------------------------------
                if msg.text == "mid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "me":
                    sendMessage(msg.to, text=None, contentMetadata={'mid': msg.from_}, contentType=13)
                if msg.text == "gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
		else:
                    pass
            else:
                pass
        if msg.toType == 2:
            if msg.contentType == 0:
                if msg.text == "mid":
                    sendMessage(msg.to, msg.from_)
                if msg.text == "gid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "ginfo":
                    group = client.getGroup(msg.to)
		    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "Error"
                    md = "[Nama Grup]:\n" + group.name + "\n\n[Id Grup]:\n" + group.id + "\n\n[Pembuat Grup]:\n" + gCreator + "\n\n[ProfilGrup]:\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                    if group.preventJoinByTicket is False: md += "\n\nKode Url : Diizinkan"
                    else: md += "\n\nLink Url : Diblokir"
                    if group.invitee is None: md += "\nJumlah Member : " + str(len(group.members)) + " Orang" + "\nUndangan Yang Belum Diterima : 0 Member"
                    else: md += "\nJumlah Member : " + str(len(group.members)) + " Member" + "\nUndangan Yang Belum Diterima : " + str(len(group.invitee)) + "Member"
                    sendMessage(msg.to,md)
		if "Gn " in msg.text:
		    if msg.toType == 2:
			X = client.getGroup(msg.to)
			X.name = msg.text.replace("Gn ","")
			client.updateGroup(X)
			sendMessage(msg.to,"Success Mengganti Nama Grup")
		    else:
			client.sendMessage(msg.to,"Siap!")
		if "Gcreator" in msg.text:
		    group = client.getGroup(msg.to)
		    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "Error"
		    sendMessage(msg.to,"Pembuat Grup :\n" + group.name + "\n=> " + gCreator)
                if msg.text == "url":
                    sendMessage(msg.to,"line://ti/g/" + client._client.reissueGroupTicket(msg.to))
		if msg.text == "uni":
		    sendMessage(msg.to,"Unicode V10\n\n1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1\n\nKamu Dapat 1 Juta!!")
		if msg.text == "spam":
		    sendMessage(msg.to,"Perkenalkan Nama Gw")
		    sendMessage(msg.to,"Toby")
		    sendMessage(msg.to,"Dan Gw itu..")
                    sendMessage(msg.to,"Tamvan :v")
		    sendMessage(msg.to,"Gw juga")
		    sendMessage(msg.to,"Suka Main ML")
    		    sendMessage(msg.to,"MobileLegend")
		    sendMessage(msg.to,"dan gw juga suka main PBS")
		    sendMessage(msg.to,"PointBlank Strike")
     		    sendMessage(msg.to,"Karena kedua game tersebut sangat seru!!")
		    sendMessage(msg.to,"Bodolah :v")
		    sendMessage(msg.to,"gw juga youtuber")
		    sendMessage(msg.to,"nama channel")
		    sendMessage(msg.to,"gw")
		    sendMessage(msg.to,"adalah")
    		    sendMessage(msg.to,"TobyGaming74")
		    sendMessage(msg.to,"")
		if msg.text == "buka":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == False:
                        sendMessage(msg.to, "Url dibuka")
                    else:
                        group.preventJoinByTicket = False
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL dibuka")
                        sendMessage(msg.to,"Link Grup : ")
                        sendMessage(msg.to,"line://ti/g/" + client._client.reissueGroupTicket(msg.to))
                if msg.text == "tutup":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == True:
                        sendMessage(msg.to, "Url ditutup")
                    else:
                        group.preventJoinByTicket = True
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL ditutup")
                if "kick:" in msg.text:
                    key = msg.text[5:]
                    client.kickoutFromGroup(msg.to, [key])
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+" maapin say 魛渷魛厰Har Har魪靠")
		if "nk" in msg.text:
                    bamz0 = msg.text.replace("nk ","")
                    bamz1 = bamz0.lstrip()
                    bamz2 = bamz1.replace("@","")
                    bamz3 = bamz2.rstrip()
                    _linedev = bamz3
                    group = client.getGroup(msg.to)
                    Names = [contact.displayName for contact in group.members]
                    Mids = [contact.mid for contact in group.members]
                    if _linedev in Names:
                        kazu = Names.index(_linedev)
                        sendMessage(msg.to, "Jgn kangem kaka..")
                        client.kickoutFromGroup(msg.to, [""+Mids[kazu]+""])
                        contact = client.getContact(Mids[kazu])
                        sendMessage(msg.to, ""+contact.displayName+" Sorry ya...")
                    else:
                        sendMessage(msg.to,"Gk ditemukan")
		if "k:" in msg.text:
                    key = msg.text[3:]
                    group = client.getGroup(msg.to)
                    Names = [contact.displayName for contact in group.members]
                    Mids = [contact.mid for contact in group.members]
                    if key in Names:
                        kazu = Names.index(key)
                        sendMessage(msg.to, "sorry kaka..")
                        client.kickoutFromGroup(msg.to, [""+Mids[kazu]+""])
                        contact = client.getContact(Mids[kazu])
                        sendMessage(msg.to, ""+contact.displayName+" Sorry ya...")
                    else:
                        sendMessage(msg.to, "gk ditemukan")
		if "Bye " in msg.text:
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    targets = []
                    for x in key["MENTIONEES"]:
                         targets.append(x["M"])
                    for target in targets:
                         try:
                            client.kickoutFromGroup(msg.to,[target])
                         except:
                            pass
		if "grandom:" in msg.text:
		    if msg.toType == 2:
		        strnum = msg.text.replace("grandom:","")
			source_str = 'abcdefghijklmnopqrstuvwxyz1234567890@:;./_][!&%$#)(=~^|'
			try:
			    num = int(strnum)
			    group = client.getGroup(msg.to)
			    for var in range(0,num):
				name = "".join([random.choice(source_str) for x in xrange(10)])
				time.sleep(0.01)
				group.name = name
				client.updateGroup(group)
			except:
			    client.sendMessage(msg.to,"Error bang, coba ulang bang oke 魛渷魛厰double thumbs up魪靠魛渷魛厰Har Har魪靠")
		if "stealgc" in msg.text:
		    group = client.getGroup(msg.to)
		    sendMessage(msg.to,"Gambar Grup :\n=> http://dl.profile.line-cdn.net/" + group.pictureStatus)
		if msg.text == "cancel":
                    group = client.getGroup(msg.to)
                    if group.invitee is None:
                        sendMessage(op.message.to, "Gk ada invitan")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        client.cancelGroupInvitation(msg.to, gInviMids)
                        sendMessage(msg.to, str(len(group.invitee)) + " Orang Yang udah dicancel yak")
		if "invitegc" in msg.text:
                    if msg.toType == 2:
                         ginfo = client.getGroup(msg.to)
                         gCreator = ginfo.creator.mid
                         try:
                             client.findAndAddContactsByMid(gCreator)
                             client.inviteIntoGroup(msg.to,[gCreator])
			     print "\nSuccess Invite gCreator"
                         except:
                             pass
		if "kickgc" in msg.text:
                    if msg.toType == 2:
                         ginfo = client.getGroup(msg.to)
                         gCreator = ginfo.creator.mid
                         try:
                             client.kickoutFromGroup(msg.to,[gCreator])
			     print "\nSuccess Kick gCreator"
                         except:
                             pass
		if "cancelgc" in msg.text:
                    if msg.toType == 2:
                         ginfo = client.getGroup(msg.to)
                         gCreator = ginfo.creator.mid
                         try:
                             client.cancelGroupInvitation(msg.to,[gCreator])
			     print "\nSuccess Cancel Invite gCreator"
                         except:
                             pass
		if "info @" in msg.text:
                     name = msg.text.replace("info @","")
                     target = name.rstrip(' ')
                     group = client.getGroup(msg.to)
		     contact = [contact.displayName for contact in group.members]
                     for contact in group.members:
                         if target == contact.displayName:
                             contact = client.getContact(contact.mid)
                             try:
                                 cover = client.channel.getCover(contact.mid)
                             except:
                                 cover = ""
                                 client.sendMessage(msg.to,"[Display Name]:\n" + contact.displayName + "\n\n[Mid]:\n" + contact.mid + "\n\n[BIO]:\n" + contact.statusMessage + "\n\n[Photo Profile]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n\n[Cover]:\n" + str(cover))
                         else:
                             pass
		if "Cn:" in msg.text:
                    string = msg.text.replace("Cn:","")
                    if len(string.decode('utf-8')) <= 20:
                        profile_B = client.getProfile()
                        profile_B.displayName = string
                        client.updateProfile(profile_B)
                        client.sendMessage(msg.to,"name " + string + " done")
			sendMessage(msg.to,"Change Name Success")
		if msg.text == "Help":
		    sendMessage(msg.to,"-=BotToby=-\n=> Play\n=> setpp:\n=> show:\n=> invite:\n=> time\n=> gift\n=> set+cek\n=> rename:\n=> info @\n=> kickgc\n=> cancelgc\n=> invitegc\n=> cancel\n=> invitegc\n=> stealgc\n=> grandom:\n=> Bye\n=> kick:\n=> k:\n=> buka\n=> tutup\n=> nk\n=> Gn\n=> Gcreator\n=> uni\n=> spam\n=> sp\n=> mid\n=> me")
		if msg.text == "Play":
                    print "Cleaning Member....."
                    _name = msg.text.replace("Play","")
                    gs = client.getGroup(msg.to)
                    sendMessage(msg.to,"cувєя b̸o̸t̸s̸ ċʀɨʍɛ ıṅ ṭһєяє!!")
		    sendMessage(msg.to,"Grup dibersihkan...")
		    sendMessage(msg.to,"Maafkan Kesalahan Orang Ini :v")
                    targets = []
                    for g in gs.members:
                        if _name in g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        sendMessage(msg.to,"error")
                    else:
                        for target in targets:
                            try:
                                klist=[client]
                                kicker=random.choice(klist)
                                kicker.kickoutFromGroup(msg.to,[target])
                                print (msg.to,[g.mid])
                            except:
                                sendMessage(msg.to,"Grup Dibersihkan")
		if "setpp:" in msg.text:
                    string = msg.text.replace("setpp:","")
                    if len(string.decode('utf-8')) <= 500:
                        profile = client.getProfile()
                        profile.statusMessage = string
                        client.updateProfile(profile)
                        client.sendMessage(msg.to,"Update Bio Done")
		    else:
			pass
		if msg.text == "sp":
                    start = time.time()
                    sendMessage(msg.to, "Tunggu...")
                    elapsed_time = time.time() - start
                    sendMessage(msg.to, "%s Detik" % (elapsed_time))
	        if "invite:" in msg.text:
                    key = msg.text[-33:]
                    client.findAndAddContactsByMid(key)
                    client.inviteIntoGroup(msg.to, [key])
                    contact = client.getContact(key)
                if msg.text == "me":
                    M = Message()
                    M.to = msg.to
                    M.contentType = 13
                    M.contentMetadata = {'mid': msg.from_}
                    client.sendMessage(M)
                if "show:" in msg.text:
                    key = msg.text[-33:]
                    sendMessage(msg.to, text=None, contentMetadata={'mid': key}, contentType=13)
                    contact = client.getContact(key)
                    sendMessage(msg.to, "Kontaknya si "+contact.displayName+"")
                if msg.text == "tagall":
		    group = client.getGroup(msg.to)
		    nama = [contact.mid for contact in group.members]
		    cb = ""
		    cb2 = ""
		    strt = int(0)
		    akh = int(0)
		    for md in nama:
			akh = akh + int(5)	
			cb += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(md)+"},"""
			strt = strt + int(6)
			akh = akh + 1
			cb2 += "@nrik\n"
		   
		    cb = (cb[:int(len(cb)-1)])
		    msg.contentType = 0
		    msg.text = cb2
		    msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}
		    try:
		        client.sendMessage(msg)
		    except Exception as error:
			    print error	
                if msg.text == "time":
                    sendMessage(msg.to, "Tanggal sekarang = " + datetime.datetime.today().strftime('%d-%m-%y'))
		    sendMessage(msg.to, "Waktu sekarang = " + datetime.datetime.today().strftime('%H:%M:%S'))
                if msg.text == "gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                if msg.text == "set":
                    sendMessage(msg.to, "Dasar sider \nKetik 銆宻ider銆� gua bakal ngasih tau siapa sidernya")
                    try:
                        del wait['readPoint'][msg.to]
                        del wait['readMember'][msg.to]
                    except:
                        pass
                    wait['readPoint'][msg.to] = msg.id
                    wait['readMember'][msg.to] = ""
                    wait['setTime'][msg.to] = datetime.datetime.today().strftime('%d-%m-%y %H:%M:%S')
                    wait['ROM'][msg.to] = {}
                    print wait
                if msg.text == "cek":
                    if msg.to in wait['readPoint']:
                        if wait["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait["ROM"][msg.to].items():
                                print rom
                                chiya += rom[1] + "\n"

                        sendMessage(msg.to, "Nih sider nya %s\nTadaaaa.....\n\nsider doang kerjaannya\n%sGileee benerrr..\n\nSider dilihat pada tanggal dan waktu:\n[%s]"  % (wait['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        sendMessage(msg.to, "Belom di set we 魛渷魛厰Har Har魪靠\nKetik 銆宻et銆� buat lihat siapa sider lucknut :v")
                else:
                    pass
        else:
            pass

#-----------------------------------------------------------------------------------------------------------------------------------
    except Exception as e:
        print e
        print ("\n\nSEND_MESSAGE\n\n")
        return

tracer.addOpInterrupt(25,SEND_MESSAGE)

while True:
    tracer.execute()
