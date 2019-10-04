import Adafruit_DHT as dht

h = None
t = None

while (h==None and t==None) :
	h,t = dht.read_retry(dht.DHT22, 24)
print(round(float(h), 2))
print(round(float(t), 2))

h = None
t = None

while (h==None and t==None) :
	h,t = dht.read_retry(dht.DHT22, 14)
print(round(float(h), 2))
print(round(float(t), 2))
