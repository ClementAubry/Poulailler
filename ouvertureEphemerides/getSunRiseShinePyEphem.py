import ephem

o=ephem.Observer()
o.lat='48.395574'
o.long='-4.333449'
# o.elev=143 #elevation in meters, http://veloroutes.org/elevation/?location=kerudu+29470+loperhet&units=m
# o.horizon = '-6' #-6=civil twilight, -12=nautical, -18=astronomical
# o.date = '2016/6/21'
s=ephem.Sun()
s.compute()

sunrise = ephem.localtime(o.previous_rising(s))
sunset = ephem.localtime(o.next_setting(s))
print('Prochain lever de soleil : ' + str(sunrise))
print('Prochain coucher de soleil : ' + str(sunset))

beg_twilight=ephem.localtime(o.previous_rising(s, use_center=True)) #Begin civil twilight
end_twilight=ephem.localtime(o.next_setting(s, use_center=True)) #End civil twilight
print('Lumiere a partir de : ' + str(beg_twilight))
print('Couche a partir de : ' + str(end_twilight))


#We relocate the horizon to get twilight times
print('\nCorrige par rapport a l\'elevation : \n')
o.horizon = '-6' #-6=civil twilight, -12=nautical, -18=astronomical

sunrise = ephem.localtime(o.previous_rising(s))
sunset = ephem.localtime(o.next_setting(s))
print('Prochain lever de soleil : ' + str(sunrise))
print('Prochain coucher de soleil : ' + str(sunset))

beg_twilight=ephem.localtime(o.previous_rising(s, use_center=True)) #Begin civil twilight
end_twilight=ephem.localtime(o.next_setting(s, use_center=True)) #End civil twilight
print('Lumiere a partir de : ' + str(beg_twilight))
print('Couche a partir de : ' + str(end_twilight))

ouverturePorte = ephem.Date(sunrise)
fermeturePorte = ephem.Date(ephem.Date(sunset) + 30 * ephem.minute)
print('Ouverture poulailler : ' + str(ouverturePorte))
print('Fermeture poulailler : ' + str(fermeturePorte))

## Horaires du soleil pour aujourd'hui
maintenant = ephem.now()
if (maintenant > ouverturePorte):
    print "Le soleil est leve, la porte doit etre ouverte"
elif(maintenant > fermeturePorte):
    print "Le soleil est couche, la porte doit etre fermee"

#filename = str(ephem.now())[0:10].strip().replace("/","_")+"_poulailler.log"
today = str(ephem.now()).split()[0]
filename = today.replace("/","_")+"_poulailler.log"
#filename = str(ephem.now()).split()[0].replace("/","_")+"_poulailler.log"
print(filename)
maintenant = ephem.Date(ephem.localtime(ephem.now()))
lastlog = ephem.Date(ephem.Date(ephem.localtime(ephem.now()))-59*ephem.minute)
print("maintenant : "+str(maintenant))
print("lastlog : "+str(lastlog))
if ( ephem.Date(ephem.Date(lastlog)+ephem.hour) > maintenant):
  print "ok"

# print(ephem.Date(ephem.localtime(ephem.Date(ephem.now()) + ephem.hour)))
