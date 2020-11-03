# CoT proxy for CloudRF API
## Overview
With this script you can connect your ATAK position to the CloudRF API to receive a dynamic radio propagation study on your location using pre-defined profiles.


## Requirements

 - Python 3
 - python requests
 - python lxml
 - A CloudRF account
 
 ## Server Setup 
 
1)	Install the script dependencies:

     pip3 install requests lxml
    
2)	Ensure your firewall permits TCP 8099 for the CoT TCP server
3)	Edit the script's 'radios' dictionary on line 9 to match your ATAK callsign(s) and radio profiles
4)	Edit the JSON radio profile within the /radios directory with API parameters and your account UID and KEY. The filenames should match the names in the script.

## ATAK Setup
1)	Add a TAK server within Settings > Network Preferences > Network Connection Preferences > Manage Server Connections > {corner dots} > Add
2)	Set the address to **your server** 
3)	Set the Protocol to TCP under Advanced
4) 	Add a network KML link via "Import Manager" with name "{callsign} RF layer" and URL **https://cloudrf.com/users/{uid}/{atak callsign}.kml** eg. https://cloudrf.com/users/1/BROADSWORD.kml
5)	Set the KML auto refresh interval to 30(s)

## Operation
When your position moves, a CoT message will be processed by your server. This will trigger a CloudRF API call and the response (JSON) will be printed in the console.
If the API call is OK, you will be notified the ATAK KML has been refreshed as follows:

    {"message": "Updated RF for BROADSWORD: /users/1/BROADSWORD.kml"}

At this point the KML layer is ready for consumption by ATAK (or other KML viewers). Stream your KML link in ATAK to view the layer. 

## Performance tips
ATAK doesn't support KML Groundoverlay so instead of small PNG images, giant (text) polygons are used which is slow to download and render, especially for high resolution calculations. 

 - Limit your radius. If you don't need more than 2km - use 2km
 - Set a reasonable resolution. 2m resolution might be available at the server but will generate a BIG KML. Use 5m for Urban planning, otherwise 30m which is the system default.
 - Set a realistic receiver threshold. Just because you can detect a signal at -90dBm doesn't mean it's workable. Raise this to match your waveform's required SNR eg. -75dBm which will give you a more realistic plot and a smaller KML
 - The minimum refresh is hard coded at 30s. You can edit this [HERE](https://github.com/deptofdefense/AndroidTacticalAssaultKit-CIV/blob/e97b9a26a0849f87b7cc97c0973ef01b28cffb77/atak/ATAK/app/src/main/java/com/atakmap/spatial/kml/KMLUtil.java#L77) in the source if you have a day to spare. 


