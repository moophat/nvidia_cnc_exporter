import http.server
import time, requests
import yaml, sys
from yaml.loader import SafeLoader
from prometheus_client import start_http_server, Gauge, Counter

#METRIC_PORT = 9023
#LIQID_STORAGE_API = "http://10.98.12.18:8080/liqid/api/v2/status/storage?filter=true"
#LIQID_GPU_API = "http://10.98.12.18:8080/liqid/api/v2/status/gpu?filter=true"
#LIQID_HOST_API = "http://10.98.12.18:8080/liqid/api/v2/fabric/topology"
#LIQID_MGMT_API = "http://10.98.12.18:8080/liqid/api/v2/fabric/topology"

class Exporter:
    METRIC_PORT = 9023
    LIQID_STORAGE_API = ""
    LIQID_GPU_API = ""
    LIQID_HOST_API = ""
    LIQID_MGMT_API = ""
    
    LABEL_FOR_STORAGE = ["name", "dev_id", "device_type"]
    LABEL_FOR_GPU = ["name", "dev_id", "device_type"]
    LABEL_FOR_HOST = ["id", "device_type"]
    LABEL_FOR_MGMT = ["index", "fabr_gid"]
    
    STORAGE_DEVICE_STATE = Gauge('storage_device_state', "Storage device state, 1 -> \"active | online\"", LABEL_FOR_STORAGE)
    STORAGE_DEVICE_CAPACITY = Gauge('storage_device_capacity', "Storage device capacity(MB)", LABEL_FOR_STORAGE)
    GPU_DEVICE_STATE = Gauge("gpu_device_state", "GPU device state, 1 -> \"active | online\"", LABEL_FOR_GPU)
    HOST_STATE = Gauge("host_state", "Host state 1-> OK", LABEL_FOR_HOST)
    MGMT_STATE = Gauge("mgmt_state", "MGMT state 1-> OK", LABEL_FOR_MGMT)

    def __init__(self, storageApi, gpuApi, hostApi, mgmtApi):
        self.LIQID_STORAGE_API = storageApi
        self.LIQID_GPU_API = gpuApi
        self.LIQID_HOST_API = hostApi
        self.LIQID_MGMT_API = mgmtApi
        
        start_http_server(self.METRIC_PORT)
        while(True):
            self.getData()
            time.sleep(60)

    def getStorageData(self):
        data = requests.get(self.LIQID_STORAGE_API).json()
        obj = data["response"]["data"]
        for d in obj:
            try:
                x = 0
                if d["device_state"] == "active | online":
                    x = 1
                self.STORAGE_DEVICE_STATE.labels(d["name"], d["dev_id"], d["device_type"]).set(x)
                self.STORAGE_DEVICE_CAPACITY.labels(d["name"], d["dev_id"], d["device_type"]).set(d["capacity(MB)"])
            except:
                print("Some error has been occurred")
        

    def getGpuData(self):
        data = requests.get(self.LIQID_GPU_API).json()
        obj = data["response"]["data"]
        for d in obj:
            try:
                x = 0
                if d["device_state"] == "active | online":
                    x = 1
                self.GPU_DEVICE_STATE.labels(d["name"], d["dev_id"], d["device_type"]).set(x)
            except:
                print("Some error has been occurred")

    def getHostData(self):
        data = requests.get(self.LIQID_HOST_API).json()
        obj = data["response"]["data"]
        for o in obj:
            for d in o:
                try:
                    hardwareComponent = d["hardwareComponent"]
                    if hardwareComponent["type"] != "HOST":
                        continue
                    x = 0
                    if hardwareComponent["device_state"] == "OK":
                        x = 1
                    self.HOST_STATE.labels(d["id"], d["deviceType"]).set(x)
                except:
                    print("Some error has been occurred")
    
    def getMGMTData(self):
        data = requests.get(self.LIQID_MGMT_API).json()
        obj = data["response"]["data"]
        for o in obj:
             for d in o:
                try:
                    hardwareComponent = d["hardwareComponent"]
                    if hardwareComponent["type"] != "MGMT":
                        continue
                    x = 0
                    if hardwareComponent["device_state"] == "OK":
                        x = 1
                    self.MGMT_STATE.labels(*[hardwareComponent["index"], hardwareComponent["fabr_gid"]]).set(x)
                except:
                    print("Some error has been occurred")
    
    def getData(self):
        self.getStorageData()
        self.getGpuData()
        self.getHostData()
        self.getMGMTData()
    
def readConfig(DEFAULT_CONFIG):
    with open(DEFAULT_CONFIG) as f:
        conf = yaml.load(f, Loader=SafeLoader)
        for d in conf["links"]:
            LIQID_STORAGE_API = d["storage_api"]
            LIQID_GPU_API = d["gpu_api"]
            LIQID_HOST_API = d["host_api"]
            LIQID_MGMT_API = d["mgmt_api"]
    Exporter(LIQID_STORAGE_API, LIQID_GPU_API, LIQID_HOST_API, LIQID_MGMT_API)

def main():
    DEFAULT_CONFIG = "config.yaml"
    if len(sys.argv) == 2:
        DEFAULT_CONFIG = sys.argv[1]
    if len(sys.argv) > 2:
        print("Please enter only 1 file name for config")
        exit(0)
        
    readConfig(DEFAULT_CONFIG)
          
    

if __name__ == "__main__":
    main()
