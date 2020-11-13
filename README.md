# IAT
Adapted from: 
Dablander, F. (2014). Implicit Association Test in Python (Version 1.00)[Software].
Available from [https://github.com/dostodabsi/implicit-association-test]

# Run it
* python ./iat.py
* Take the test
* run calcIAT.py to see result, note that if there are mutliple result files in the directory calcIAT.py reads and calculates them all, which is nice if you want to get bulk scores and store them somewhere.

# Updates by Sonny Parlin
* Converted code for Python 3
* added calcIAT.py to calculate the result files created by iat.py

# Scoring
* Based on the code it seems a negative score is indicitive of bias for the first data set (in this case self), while a positive number indicates a bias towards the second data set (in this case other) but I'm not 100% certain on this, it's a guess based on how Harvard said they score. 

"Negative IAT scores indicate implicit preference for whites relative to blacks. Positive scores indicate implicit preference for blacks relative to whites. Many-though not all-black Americans exhibit an implicit evaluative preference for whites relative to blacks (e.g., Livingston, 2002)."
