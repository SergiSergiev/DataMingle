'''
free-space path loss (FSPL)
For typical radio applications, it is common to find f measured in units of GHz and d in km, in which case the FSPL equation becomes

=20\log _{10}(d)+20\log _{10}(f)+92.45} \ =20\log _{{10}}(d)+20\log _{{10}}(f)+92.45
For d,f in meters and kilohertz, respectively, the constant becomes  -87.55 .

For  d,f in meters and megahertz, respectively, the constant becomes -27.55 .

For d,f in kilometers and megahertz, respectively, the constant becomes  32.45 .
https://en.wikipedia.org/wiki/Free-space_path_loss#Free-space_path_loss_in_decibels
'''
import math

freq_in_mhz = 2462

def campute_distance (level_in_db)-> int:
    result = (27.55 - (20 * math.log10(freq_in_mhz)) + math.fabs(level_in_db)) / 20.0
    meters = math.pow(10, result)

#    feet = meters * 3.2808
    return meters
