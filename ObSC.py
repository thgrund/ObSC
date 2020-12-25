import sys,time,argparse,math
from pythonosc import dispatcher
from pythonosc import osc_server

import logging
logging.basicConfig(level=logging.INFO)

sys.path.append('../')
from obswebsocket import obsws, requests  # noqa: E402

host = "localhost"
port = 4444
password = "secret"

ws = obsws(host, port, password)
ws.connect()

ScenesNames = []
SceneSources = []

def removePrefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

def sourceSwitch(address):  # This function is untested
    sourceName = removePrefix(address, '/source/')
    ws.call(requests.SetSceneItemProperties(sourceName,scene,visible=switch))

def sceneSwitch(address):  
    sceneName = removePrefix(address, '/scene/')
    ws.call(requests.SetCurrentScene(sceneName))

def recordingControl(address):  
    controlType = removePrefix(address, '/recording/')
    if controlType == 'start':
        ws.call(requests.StartRecording())
    elif controlType == 'stop':
        ws.call(requests.StopRecording())
    elif controlType == 'toggle':
        ws.call(requests.StartStopRecording())

def streamingControl(address):  
    controlType = removePrefix(address, '/streaming/')
    if controlType == 'start':
        ws.call(requests.StartStreaming())
    elif controlType == 'stop':
        ws.call(requests.StopStreaming())
    elif controlType == 'toggle':
        ws.call(requests.StartStopStreaming())

def getCurrentScenes():
    scenes = ws.call(requests.GetSceneList())
    for s in scenes.getScenes():
        name = s['name']
#        print(ws.call(requests.GetSourcesList()),"\n")  # Get The list of available sources in each scene in OBS
        ScenesNames.append(name)  # Add every scene to a list of scenes
    printScenes(ScenesNames)
    return scenes

def printScenes(ScenesNames):
    print("Current scenes and their OSC addresses:")
    print("=====================================\n")
    for scene in ScenesNames:
        spaceWarning = ""
        if ' ' in scene:
            spaceWarning = "    **** Warning!  Spaces are not valid in OSC addresses.  Please rename Scene in OBS. ****"
        print(scene + ": /scene/" + scene + spaceWarning + "")
    print("=====================================\n")
    print("\n")

def printGeneralAddressInfo():
    print("General Addresses:")
    print("=====================================\n")
    print("Streaming:")
    print("Start: /streaming/start")
    print("Stop: /streaming/stop")
    print("Toggle: /streaming/toggle")
    print("\nRecording:")
    print("Start: /recording/start")
    print("Stop: /recording/stop")
    print("Toggle: /recording/toggle")
    print("=====================================\n")
    print("\n")


if __name__ == "__main__":
    try:
        print("\n")
        print("\n")
        printGeneralAddressInfo()
        scenes = getCurrentScenes()
#        sources = getCurrentSources()
        ### OSC Settings
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip",default="127.0.0.1", help="The ip to listen on")
        parser.add_argument("--port",type=int, default=5005, help="The port to listen on")

        args = parser.parse_args()  # parser for --ip --port arguments

        dispatcher = dispatcher.Dispatcher()

        ### OSC Address Mappings
        dispatcher.map("/scene/*", sceneSwitch)
        dispatcher.map("/source/*", sourceSwitch)
        
        dispatcher.map("/recording/start", recordingControl)
        dispatcher.map("/recording/stop", recordingControl)
        dispatcher.map("/recording/toggle", recordingControl)

        dispatcher.map("/streaming/start", streamingControl)
        dispatcher.map("/streaming/stop", streamingControl)
        dispatcher.map("/streaming/toggle", streamingControl)

        server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)  
        print("Serving on {}".format(server.server_address))
        
        server.serve_forever()

    except KeyboardInterrupt:
        pass

    ws.disconnect()

