import socket, json, requests
from lxml import etree
# ATAK CoT proxy for CloudRF API

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# EDIT ME: Radio templates are read from local JSON files and mapped to ATAK callsigns here
radios = {"CloudRF": "radios/bigradio.json", "droneyMcDroneFace": "radios/drone.json"}

def parseCoT(xml):
	root = etree.fromstring(xml.encode("utf-8"))
	lat=round(float(root.xpath("//event/point")[0].attrib["lat"]),5)
	lon=round(float(root.xpath("//event/point")[0].attrib["lon"]),5)
	cs=root.xpath("//event/detail/contact")[0].attrib["callsign"]
	return {"cs": cs, "lat": lat, "lon": lon}

def areaAPI(update):
	if update["cs"] not in radios: # Warn if user didn't setup radios {}
		print("Callsign %s does not have a radio allocated!" % update["cs"])
	else:
		print("\nCalculating coverage for c/s %s at %.5f,%.5f using %s..." % (update["cs"],update["lat"],update["lon"],radios[update["cs"]]))
		with open(radios[update["cs"]]) as json_file:
			radio = json.load(json_file)
			radio["lat"] = update["lat"] # Use loc from CoT message..
			radio["lon"] = update["lon"] 
			print(radio)
		r = requests.post("https://cloudrf.com/API/area?atak", data=radio, verify=False) # DO IT 
		print("\nAPI RESPONSE:\n"+r.text)
		j = json.loads(r.text)
		if 'kmz' in j: 
			r = requests.get("https://cloudrf.com/API/archive/data?callsign="+str(update["cs"])+"&atak="+str(j["id"])+"&uid="+str(radio["uid"])+"&key="+radio["key"], verify=False) # ATAK fairy
			print(r.text)
s.bind(('', 8099)) # Default TAK server port
s.listen(1)
conn, addr = s.accept()

while 1:
	data = conn.recv(1024)
	conn.sendall(data) # Heartbeat expects a copy of the data
	try:
		if "contact" in data.decode("utf-8"):
			update = parseCoT(data.decode("utf-8")) # Callsign, lat, lon..
			areaAPI(update)
		else:
			print(data)
	except Exception as e:
		print(e)
		pass
conn.close()
