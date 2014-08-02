def ADS1115_LM36(volts, unit): # return temperature conversion from LM36
     # convert the voltage to degrees celsius
     tempc = volts/.03 
     
     if unit == "C":
     	# return the degrees in celsius
     	return tempc
     
     if unit == "F":
     	# convert celsius to degrees fahrenheit
     	tempf = (tempc*9/5)+32
     	# return the degrees in fahrenheit
     	return tempf
     
     return "Failed to convert"
