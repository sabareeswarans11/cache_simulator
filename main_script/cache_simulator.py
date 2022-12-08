'''
##########################Cache Simulator##########################
Project source code:https://github.com/sabareeswarans11/cache_simulator 
Code walkthrough: https://www.youtube.com/watch?v=LDf1c1G95kI (This video will be available on DEC 9,2022 10AM(EST)
-----------------------------------------------------------------------------------
Done by: Mohamed Gani Mohamed Sulthan(2811619) || Sabareeswaran Shanmugam(2796495)
----------------------------------------------------------------------------------
1 way | 4 way | 8 way associative
-----------------------------------------------------------------------------------
Input : Run the code with arguments python cache_simulator.py -dinfile (filename) -cache_config (cache_config_types)
        Example: python cache_simulator.py -dinfile 085.gcc.din -cache_config type1
                 python cache_simulator.py -dinfile 022.li.din -cache_config type2
                 python cache_simulator.py -dinfile 078.swm256.din -cache_config type3
                 python cache_simulator.py -dinfile 047.tomcatv.din -cache_config type4
configfile.ini: Here we initialized the four types of cache with the block size and cache size
log: All the traces will be stored in the log(log.txt)
Output: It will create a text file (cache_simulation_result.txt) with the given handout parameters
---------Testcases Achieved----------------------------------------------------------
1)085.gcc.din
2)022.li.din
3)078.swm256.din
4)047.tomcatv.din
----------------------------------------------------------------------------------------'''
import math
import pandas as pd
import argparse
import configparser
import logging
import time

class cache_blocks:
  def __init__(self):
    self.valid = True  # true -> empty ; false -> not empty
    self.tag = -1
    self.count = 0  # the greater the count is, the less the block is used since last time
    self.address_in_decimal = -1
    self.address = -1

class sets:
  def __init__(self, way):
    # Create way cache blcok in each set
    self.cache_blocks = [cache_blocks() for i in range(way)]

class cache_intialize:
  def __init__(self, size_of_block, size_of_cache, way):
    self.size_of_block = size_of_block  # The size of each Cache Block, the unit is Byte,
    self.size_of_cache = size_of_cache # Cache size, the unit is KByte,
    self.way = way # The number of cache cache_blocks in a way
    self.cache_block_number = int((size_of_cache ) / size_of_block)  # The number of "Cache Block"
    self.set_number = int(self.cache_block_number / way)  # The number of set
    self.sets = [sets(way) for i in range(self.set_number)] # Create set_number cache sets in the cache
    self.hit_count = 0 # To trace the hit and miss
    self.miss_count = 0
    self.block_replacement =0
    self.block_placement = 0

    print("\n\n"+ str(self.way) + "-way associative cache, with " +str(self.set_number) + " sets.", file=f)
    logging.info("Tracing log for {0} -way associative  ".format(str(self.way)))

  # Check whether the data is in the cache
  def read_from_cache(self, address_in_decimal):
    # Converting decimal address to block address
    block_address = math.floor(address_in_decimal / self.size_of_block)
    # Calculate the corresponding set
    set_number = int(block_address % self.set_number)
    # Calculate the corresponding set
    tag = math.floor(block_address / self.set_number)

    if self.IsEmpty(set_number):
      logging.info("--Cache MISS! index {0} is not present inside cache".format(str(set_number)))
      self.miss_count += 1
      self.sets[set_number].cache_blocks[0].valid = False
      self.sets[set_number].cache_blocks[0].tag = tag
      # block placement
      self.block_placement +=1
      self.add_count(set_number)
    else:
      if not self.IsFull(set_number):
        logging.info("--Cache MISS! index present differnt tag value")
        hit = False
        for block in self.sets[set_number].cache_blocks:
          if not block.valid and block.tag == tag:
            logging.info("--Cache HIT!")
            hit = True
            self.hit_count += 1
            self.add_count(set_number)
            block.count = 1
            break

        if not hit:
          for block in self.sets[set_number].cache_blocks:
            if block.valid:
              logging.info("--Cache MISS!")
              self.miss_count += 1
              block.valid = False
              block.tag = tag
              # block placement
              self.block_placement += 1
              self.add_count(set_number)
              break

      else:  # the set is full, replace the least recent used block, by LRU algorithm.
        self.LRU(set_number, tag)

  def LRU(self, set_number, tag):
    hit = False
    for block in self.sets[set_number].cache_blocks:
      if block.tag == tag:  # cache hit, the wanted data is in cache, set count to 0
        logging.info("--Cache HIT!")
        hit = True
        self.hit_count += 1
        self.add_count(set_number)
        block.count = 1
        break
    if not hit:
      logging.info("--Cache MISS!")
      self.miss_count += 1
      max_count = 0  # the LRU block count，the larger the number -> the longer it has not been used
      LRU_index = -1
      for i in range(self.way):
        if self.sets[set_number].cache_blocks[i].count > max_count:
          max_count = self.sets[set_number].cache_blocks[i].count
          LRU_index = i
      self.sets[set_number].cache_blocks[LRU_index].tag = tag
      self.add_count(set_number)
      self.sets[set_number].cache_blocks[LRU_index].count = 1
      self.block_replacement += 1

  def add_count(self, set_number):
    for block in self.sets[set_number].cache_blocks:
      if not block.valid:
        block.count += 1

  def IsEmpty(self, set_number):
    for block in self.sets[set_number].cache_blocks:
      if block.valid == False:
        return False
    return True

  def IsFull(self, set_number):
    for block in self.sets[set_number].cache_blocks:
      if block.valid == True:
        return False
    return True

def cache_simulator_1_4_8_way():
  No_of_ways = [1,4,8]
  # cache configuration in configfile.ini
  config_obj = configparser.ConfigParser()
  config_obj.read(r"configfile.ini")
  for way in No_of_ways:  # Itearting the associative level to allocate the space
	########### Predefined block size and cache size###########
    type = config_obj[args.cache_config]
    size_of_block = (int)(type["blockSize"])
    size_of_cache = (int)(type["cacheSize"])
    ###############################################
    simulation = cache_intialize(size_of_block, size_of_cache, way)
    df = pd.read_csv(r"{0}".format(args.dinfile), sep=" ", header=None, names=["Accesstype", "Address", "size_or_data"])
    address=df['Address'].tolist()
    total_mem_reference = df['Accesstype'].value_counts().sum()
    read_count = df['Accesstype'].value_counts()[0]
    write_count = df['Accesstype'].value_counts()[1]
    inst_fetch_count = df['Accesstype'].value_counts()[2]

    for i in range(len(address)):
      # Converting Hex address in to decimal
      address_in_decimal = int(address[i], 16)
      # Call the main function to read the cache and predict the hit/miss
      simulation.read_from_cache(address_in_decimal)

    logging.info("Tracing log for {0} -way associative done!".format(str(way)))
    print("################### Cache Simulation Result ###################", file=f )
    print("Total memory references in trace:{0} (read:{1},write:{2},fetch instruction:{3})".format(total_mem_reference,read_count,write_count,inst_fetch_count), file=f)
    print("################### Cache parameters ###################", file=f)
    print("Cache size:{0}".format(size_of_cache), file=f)
    print("cache block size:{0}".format(size_of_block), file=f)
    print("################### Cache statistics ###################", file=f)
    print("Number of memory write events:{0}".format(write_count), file=f)
    print("Number of block placements:{0}".format(str(simulation.block_placement)), file=f)
    print("Number of block Replacements:{0}".format(str(simulation.block_replacement)), file=f)
    print("################### Total No of Hits ###################", file=f)
    print("Cache Hits:{0}".format(simulation.hit_count), file=f)
    print("################### Total No of Misses ###################", file=f)
    print("Cache Misses:{0}".format(simulation.miss_count), file=f)
    print("################### Overall ###################", file=f)
    cache_miss_ratio = ((1.0 - (simulation.hit_count) / len(address)) * 100)
    print("Cache miss ratio:{0} %".format(round(cache_miss_ratio, 2)), file=f)
    print("######### simulation done ##########", file=f)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Get trace filename and cache size type from user')
  parser.add_argument("-dinfile", "-f", type=str, required=True)
  parser.add_argument('-cache_config', type=str, help='Type1- 16BS,16384CS; Type2- 32BS,32768CS; Type3- 64BS,65536CS; Type4- 128BS,131072CS',required=True)
  args = parser.parse_args()
  # Logging to trace the data
  logging.basicConfig(filename="log.txt", level=logging.INFO,
                      format="%(asctime)s %(message)s", filemode="w")
  # write the console results to text file
  with open("cache_simulation_result.txt", "a") as f:
    start_time = time.time()
    print("################## Cache simulation started ##################")
    print("Memory Trace:{0}".format(str(args.dinfile)), file=f)
    cache_simulator_1_4_8_way()
    print("Time taken to trace the file--- %s seconds ---" % (time.time() - start_time))
    print("Find the output result --cache_simulation_result.txt")
    print("################## Cache simulation done ##################")
