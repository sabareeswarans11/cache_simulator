* ######### CACHE SIMULATOR ######### 
  * Cache simulator for tracing memory references to measure the cache performance (miss ratio, etc.).

* ######### Compile and Run ######### 
  * python cache_simulator.py -dinfile 085.gcc.din -cache_config type1
  * cache_simultor.py -- Main File
  * arg parameter -dinfile can accept different din files.
  * arg parameter -cache_config allows user to try different cache and block size 16B~128B (4 cases)
* ######### Inorder To Acheive 12 Cases for any One Input Din File  #########
  * run as below,
  * python cache_simulator.py -dinfile 085.gcc.din -cache_config type1  
  * python cache_simulator.py -dinfile 085.gcc.din -cache_config type2
  * python cache_simulator.py -dinfile 085.gcc.din -cache_config type3
  * python cache_simulator.py -dinfile 085.gcc.din -cache_config type4
* ######### Sample Output Trace (log.txt)-- all 12 cases ######### 
<img width="900" height="700" alt="Screen Shot 2022-12-08 at 1 40 02 PM" src="https://user-images.githubusercontent.com/94094997/206539718-763d6e3e-65f8-44b2-80c3-664b696c00e5.png">
