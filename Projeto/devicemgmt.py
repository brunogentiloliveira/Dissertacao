from onvif import ONVIFCamera

def gethostName(camara):
    name = camara.devicemgmt.GetHostname()
    return name.Name

def getDateTime(camara):
    dttm = camara.devicemgmt.GetSystemDateAndTime()
    localTime = dttm.UTCDateTime.Time
    localDate = dttm.UTCDateTime.Date
    return [localDate,localTime]