## @package paco.util
# Various utilities
# @author Peter Wagener


import sys

## Command-line progress bar handler.
#
# Objects of this class are fed with a minimum and maximum and a current value.
# The current value is then incremented as a time-consuming process is 
# progressing. As the value moves from minimum to maximum, the current
# position within this interval is visualized by a string Image.
# Typical usage involves creating and initializing a progress bar, then
# entering it in a with statement and incrementing the current value from
# within:
#
#      with ProgressBar(0,100) as pb:
#        for i in range(100):
#          <code>
#          pb.increment()
#
# If multiple processes that do not know each other can be grouped together,
# a parenting progress bar can be used to symbolize the entire process.
# By assigning this progress bar as parent to the ones in child processes,
# only this parent gets re-drawn on progression.
class ProgressBar:
  ## Progress bar image outputting three dots and a digits for every 10 % of
  # progression
  Image10=["0",".",".",".","1",".",".",".","2",".",".",".","3",".",".",".","4",".",".",".","5",".",".",".","6",".",".",".","7",".",".",".","8",".",".",".","9",".",".",".","10"]
  
  ## Progress bar image outputting three dots and a two-digit number for each
  # percent of progression.
  #
  # This outputs one line for every ten percent of progression thus should be
  # used for very long-running processes only.
  Image100=["00",".",".",".","01",".",".",".","02",".",".",".","03",".",".",".","04",".",".",".","05",".",".",".","06",".",".",".","07",".",".",".","08",".",".",".","09",".",".",".","10\n10",".",".",".","11",".",".",".","12",".",".",".","13",".",".",".","14",".",".",".","15",".",".",".","16",".",".",".","17",".",".",".","18",".",".",".","19",".",".",".","20\n20",".",".",".","21",".",".",".","22",".",".",".","23",".",".",".","24",".",".",".","25",".",".",".","26",".",".",".","27",".",".",".","28",".",".",".","29",".",".",".","30\n30",".",".",".","31",".",".",".","32",".",".",".","33",".",".",".","34",".",".",".","35",".",".",".","36",".",".",".","37",".",".",".","38",".",".",".","39",".",".",".","40\n40",".",".",".","41",".",".",".","42",".",".",".","43",".",".",".","44",".",".",".","45",".",".",".","46",".",".",".","47",".",".",".","48",".",".",".","49",".",".",".","50\n50",".",".",".","51",".",".",".","52",".",".",".","53",".",".",".","54",".",".",".","55",".",".",".","56",".",".",".","57",".",".",".","58",".",".",".","59",".",".",".","60\n60",".",".",".","61",".",".",".","62",".",".",".","63",".",".",".","64",".",".",".","65",".",".",".","66",".",".",".","67",".",".",".","68",".",".",".","69",".",".",".","70\n70",".",".",".","71",".",".",".","72",".",".",".","73",".",".",".","74",".",".",".","75",".",".",".","76",".",".",".","77",".",".",".","78",".",".",".","79",".",".",".","80\n80",".",".",".","81",".",".",".","82",".",".",".","83",".",".",".","84",".",".",".","85",".",".",".","86",".",".",".","87",".",".",".","88",".",".",".","89",".",".",".","90\n90",".",".",".","91",".",".",".","92",".",".",".","93",".",".",".","94",".",".",".","95",".",".",".","96",".",".",".","97",".",".",".","98",".",".",".","99",".",".",".","100"]
  
  ## Constructor.
  #
  # @param min initial minimum value
  # @param max initial maximum value
  # @param image Progress bar image to be used. Defaults to Image10.
  # @param parent Parent progress bar to hand updates off to.
  def __init__(self,min,max, parent=None, image=None):
    self.image=image if image!=None else ProgressBar.Image10
    self.parent=parent
    self.min=min
    self.max=max
    self.next=self.min
    self.idx=0
    self.cur=self.min
  
  def __enter__(self):
    self.reset()
    return self
  
  def __exit__(self,a,b,c):
    self.finish()
  
  ## Resets the progress bar for re-use
  def reset(self,min=None,max=None):
    if min!=None: self.min=min
    if max!=None: self.max=max
    self.next=self.min
    self.idx=0
    self.cur=self.min
  
  ## Sets the current value to a specified value.
  #
  # Note that reducing the current value will not shrink the progress bar.
  def iterate(self,v):
    while self.next!=None and v>=self.next:
      sys.stdout.write(self.image[self.idx])
      self.idx=self.idx+1
      if self.idx>=len(self.image):
        self.next=None
        sys.stdout.write("\n")
      else:
        self.next=self.next+(self.max-self.min)/(len(self.image)-1)
      sys.stdout.flush()
    self.cur=v
  

  ## Advances the current value by a specified amount
  def increment(self,v=1):
    if self.parent!=None:
      self.parent.increment(v/(self.max-self.min))
      self.cur+=v
      return
    self.iterate(self.cur+v)
  

  ## Signals the completion of the underlying process.
  #
  # This will always fill the progress bar if it hasn't been filled already.
  def finish(self):
    if self.parent!=None:
      self.parent.increment((self.max-self.cur)/(self.max-self.min))
      self.cur=self.max
      self.next=None
      return
    
    if self.next!=None:
      while self.idx<len(self.image):
        sys.stdout.write(self.image[self.idx])
        self.idx=self.idx+1
      sys.stdout.write("\n")
      sys.stdout.flush()
      self.next=None
      self.cur=self.max

